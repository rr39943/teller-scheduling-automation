# Teller scheduling automation

[![codebeat badge](https://codebeat.co/badges/76ec6b44-1336-4034-9ec9-b9ea390a0985)](https://codebeat.co/projects/github-com-rr39943-teller-scheduling-automation-master)

This repository create a timetable with schedules of persons regarding given constraints. This software was developed to improve teller scheduling in a library.


## Prerequisites

You need a standard version of python 3.6 with the following libraries:
* pandas >= 0.20.3
* numpy >= 1.13.3

## Usage

1. Deposit Excel files (with the appropriate data) in the data folder. More information about the Excel sheet in the wiki.
2. Run the preprocessing script to build the pickle intermediate data (preprocessing.py).
3. Run the building schedules script (build_timetable.py) to create a Excel file with the timetable (folder result).

## Running the tests

You can run the tests with python -m unittest. The tests use the example data located in test folder to verify the output of the different parts of the software.

## Authors

* **Raphaël Rey:** [raphael.rey@epfl.ch](mailto:raphael.rey@epfl.ch)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
