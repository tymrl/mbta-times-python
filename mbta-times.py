import argparse
import csv
from io import StringIO
from operator import itemgetter

import arrow
import requests


def calculate_expected_arrival(train):
    """
    Given an dictionary representing information about the arrival of a train,
    calculate its expected arrival time, convert it to a readable string, and
    add it to the train dictionary.
    """
    scheduled_time = arrow.get(train['ScheduledTime'])
    lateness = int(train['Lateness'])
    expected_time = scheduled_time.replace(seconds=lateness)

    # Convert to string for consistency with the other timestamp fields
    train['ExpectedTime'] = str(expected_time.timestamp)
    train['ExpectedTimeReadable'] = expected_time.format('hh:mm a')


def clean_dict(raw_dictionary):
    """
    Given a dictionary, return a new dictionary with whitespace stripped from
    both the keys and the values.  Also calculate the expected arrival time.
    """
    train = {}
    for key, value in raw_dictionary.items():
        train[key.strip()] = value.strip()

    calculate_expected_arrival(train)

    return train


def request_csv():
    """
    Requests an up-to-date CSV file using the MBTA API.
    """
    response = requests.get(
        'http://developer.mbta.com/lib/gtrtfs/Departures.csv'
    )
    if not response.ok:
        raise RuntimeError('HTTP Request did not succeed')
    
    return [
        row for row
        in csv.DictReader(StringIO(response.content.decode('utf-8')))
    ]


def read_csv(filepath):
    """
    Reads a CSV file located at `filepath` and returns a list of dictionaries
    keyed by the header row of the CSV.  Also does some basic cleaning.
    """
    with open(filepath, encoding='utf-8') as f:
        return [row for row in csv.DictReader(f)]


def print_schedule(rows):
    """
    Given a list of raw train dictionaries, calculate their expected arrival
    times, order them by expected arrival time, and print them all in a nicely
    formatted schedule.
    """

    trains = [clean_dict(row) for row in rows]
    trains.sort(key=itemgetter('ExpectedTime'))

    format_string = (
        '{ExpectedTimeReadable:10}'
        '{Destination:30}'
        '{Trip:10}'
        '{Track:10}'
        '{Status}'
    )

    header = {
        'ExpectedTimeReadable': 'Time',
        'Destination': 'Destination',
        'Trip': 'Train #',
        'Track': 'Track',
        'Status': 'Status'
    }

    print(format_string.format(**header))
    for train in trains:
        if train['Origin'] == 'South Station':
            print(format_string.format(**train))


def run():
    """
    Make a CLI to run our script.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--filepath',
        help='Path to input file.  Should be UTF-8 encoded (or compatible).'
    )

    args = parser.parse_args()

    rows = read_csv(args.filepath) if args.filepath else request_csv()
    
    print_schedule(rows)


if __name__ == '__main__':
    run()
