# MBTA Arrival Time Display

This is a simple Python script that, given a CSV file representing train arrival times at South Station, parses, sorts, and displays the data.  The CSV file should formatted similarly to the one available here: http://developer.mbta.com/lib/gtrtfs/Departures.csv .

## Requirements

This script requires Python 3.4 or higher, as well as a virtual environment that includes the `arrow` package (for graceful handling of dates and times) and the `requests` package (for handling API requests).

## Usage

In an appropriate Python 3 virtual environment, run the following command:

```
python mbta-times.py
```

This will print a formatted schedule of the current arrival data from the MBTA.  For a live-update schedule, use:

```
watch python mbta-times.py
```

If you have a specific CSV file that you wish to test on, use:

```
python mbta-times.py -f path/to/file.csv
```
