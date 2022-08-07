# Qualifying-Offer-Calculation

## Table of Contents
* [Introduction](#Introduction)
* [Data Issues](#Data_Issues)
* [Technologies](#Technologies)
* [Dependencies](#Dependencies)
* [Running The Project](#Running_The_Project)

### Introduction

This project calculates the qualifying offer amount for Major League Baseball players based on salary data from the 2016 season. The results are then shown through a GUI using [PyQt5](https://pypi.org/project/PyQt5/) along with other relevant information.

### Data Issues
Throughout the construction of this project, I came across various issues and syntax cases in the provided data. Here is what I found in the 'salary' column of the data:

1. Some values are missing commas <br>
2. Some values are missing '\$' signs <br>
3. Some values have multiple '\$' signs <br>
4. Some values are missing entirely
5. Some values say 'no salary data' <br> 

### Technologies
* [Python](https://www.python.org/)
  

### Dependencies
* [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/)
* [PyQt5](https://pypi.org/project/PyQt5/)

### Running The Project

#### Run On Application
1. Download latest version of this project
2. Double click the 'calculations' app to open project
3. If the app has permissions issues, open a terminal and type:
    ```chmod -R 755 <path-to-application> ```, then right-click the app and press 'open'

#### Run Locally
1. Download latest version of this project
2. Open source code in a Python IDE
3. Download dependencies
3. Run calculations.py