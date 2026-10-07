# EarthquakePuller

A Python script I built to automatically collect worldwide earthquake information for Force 13's live earthquake coverage.

The script was fully developed and working, but was ultimately never implemented into Force 13's live production workflow. It was intended to automate a process that otherwise involved much more manual checking and formatting of earthquake information, along with a hardcoded lookup table of locations around the world.

The script regularly checks EMSC for the newest reported earthquake, pulls the event's information, formats it into a consistent output, and sends it to a web endpoint designed for use by the livestream system.

## What it does

For each new earthquake, the script pulls information including:

- Magnitude
- Latitude and longitude
- Time
- Geographic region
- Nearby population/location information when available

It then formats that information into a predictable string for the livestream system to use.

The script also keeps track of the most recently processed earthquake. That prevents the same event from being repeatedly sent each time EMSC is checked.

Earthquake data also gets revised fairly often, especially magnitude estimates shortly after an event. Because of that, the script separately checks whether the newest event is actually new or whether an existing earthquake has received an updated magnitude.

For earthquakes near populated areas, the output can describe the event relative to a nearby city. More remote earthquakes instead use their broader geographic region.

## Running it

Install the dependencies:

```bash
pip install requests beautifulsoup4
```

Then run:

```bash
python EarthquakePuller.py
```

This repository contains the version of the script developed for the original Force 13 workflow. Although the script itself was completed and functional, it was never incorporated into the production livestream system. The EMSC pages and Force 13 infrastructure it depended on have also changed since then, so it should be treated as an archived implementation rather than something that can necessarily be dropped into the current system unchanged.
