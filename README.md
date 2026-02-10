
# European Airport Data Analysis System

## Overview

This project is a Python-based data analysis application developed as part of the Software Development I coursework.
The system processes air traffic departure data from European airports and provides statistical summaries and visualisations.

Users can select an airport and year, load the corresponding dataset, and view calculated results such as flight counts, airline performance, delays, and weather-related statistics.

---

## Features

* User input validation for airport codes and years
* CSV file loading and processing
* Flight statistics calculation
* Automatic result saving to a text file
* Histogram visualisation of airline departures
* Program loop to analyse multiple datasets

---

## Technologies Used

* Python
* CSV file handling
* graphics.py module (for histogram visualisation)

---

## How It Works

1. The user enters:

   * A three-letter airport code
   * A year (2000–2025)
2. The program loads the corresponding CSV dataset.
3. It calculates various statistics, including:

   * Total number of flights
   * Flights from specific terminals
   * Short-distance flights
   * Airline-specific statistics
   * Delay percentages
   * Weather-related data
4. Results are:

   * Displayed in the console
   * Saved to a `results.txt` file
5. A histogram is generated for a selected airline.
6. The user can choose to analyse another dataset.

---

## Example Outputs

The program generates:

* Text-based statistical summaries
* A histogram showing hourly departures for a selected airline
* A results text file containing saved analysis data



## Requirements

* Python 3.x
* `graphics.py` module
* CSV dataset files in the same directory as the Python script

---

## How to Run

1. Place the Python file, CSV files, and `graphics.py` in the same folder.
2. Open the folder in IDLE or a Python-compatible IDE.
3. Run the Python script.
4. Follow the on-screen prompts.

---

## Learning Outcomes

This project demonstrates:

* Input validation
* File handling
* Data processing
* Use of functions and loops
* Basic graphical visualisation
* Structured program design


Sethuli Tinara Harischandra
Software Development I Coursework
University of Westminster

