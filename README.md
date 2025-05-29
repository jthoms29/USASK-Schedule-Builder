# USASK SCHEDULE BUILDER

A Python script to aid in choosing classes for the upcoming fall 2025 and winter 2026 semesters
at the University of Saskatchewan.

## Instructions

Clone this repository and run main.py. From there, follow the on-screen instructions. If a valid schedule
can be created from the given input parameters, it will be printed out, along with a list of the courses'
crns. Just copy this crn list use it to choose the classes for your schedule on the university's
registration site. The generation algorithm is very fast, so you can quickly generate a new possible
schedule if you're not happy with the one you are given.

## How it works

Using the input parameters given by the user, every viable course from the given semester is gathered
from the corresponding semester's csv. One of these viable courses is chosen at random and added to the
schedule (if this course has a lab section, one of these is added as well). From there, the selection of
viable courses is recomputed, removing all of the courses that would overlap in time with the one
already added to the schedule. One of these new viable courses is then added. This process is repeated
until a schedule is created with the requested number of classes.

The number of available seats is retrieved from the school's registration site using
the webscraper I wrote in scraper.py. This just uses http requests, so it is also very fast.
