# USASK SCHEDULE BUILDER

A Python script to aid in choosing classes for the upcoming fall 2025 and winter 2026 semesters
at the University of Saskatchewan.

## Instructions

Clone this repository and run main.py. From there, follow the on-screen instructions. If a valid schedule
can be created from the given input parameters, it will be printed out, along with a list of the courses'
crns. Just copy this crn list use it to choose the classes for your schedule on the university's
registration site. The generation algorithm is very fast, so you can quickly generate a new possible
schedule if you're not happy with the one you are given.

The output for a successfully generated schedule will look something like this:

``` cmd

New Schedule:
================
Monday:

MATH 110 - Calculus I - section 27
Meeting time 1:
  09:30 AM - 10:20 AM
  09/03/2025 - 12/05/2025
125 seats available

CMPT 332 - Operating Systems Concepts - section 01
Meeting time 1:
  04:30 PM - 05:20 PM
  09/03/2025 - 12/05/2025
120 seats available

================
Tuesday:

LING 111 - Structure of Language - section 01
Meeting time 1:
  10:00 AM - 11:20 AM
  09/03/2025 - 12/05/2025
160 seats available

================
Wednesday:

MATH 110 - Calculus I - section 27
Meeting time 1:
  09:30 AM - 10:20 AM
  09/03/2025 - 12/05/2025
125 seats available

CMPT 332 - Operating Systems Concepts - section 01
Meeting time 1:
  04:30 PM - 05:20 PM
  09/03/2025 - 12/05/2025
120 seats available

================
Thursday:

LING 111 - Structure of Language - section 01
Meeting time 1:
  10:00 AM - 11:20 AM
  09/03/2025 - 12/05/2025
160 seats available

MATH 110 - Calculus I - section L24
Meeting time 1:
  01:00 PM - 02:20 PM
  09/03/2025 - 12/05/2025
125 seats available

================
Friday:

MATH 110 - Calculus I - section 27
Meeting time 1:
  09:30 AM - 10:20 AM
  09/03/2025 - 12/05/2025
125 seats available

CMPT 332 - Operating Systems Concepts - section T07
Meeting time 1:
  01:30 PM - 02:20 PM
  09/03/2025 - 12/05/2025
30 seats available

CMPT 332 - Operating Systems Concepts - section 01
Meeting time 1:
  04:30 PM - 05:20 PM
  09/03/2025 - 12/05/2025
120 seats available

================
Saturday:

================
Sunday:

================
None:


CRNS: 80038, 80228, 80678, 81917, 87167
```

This shows a week with each class in their respective days. The 'None' day corresponds to asynchronous online classes.
The CRN list at the end allows you to easily search these courses on the university's registration website.

## How it works

Using the input parameters given by the user, every viable course from the given semester is gathered
from the corresponding semester's csv. One of these viable courses is chosen at random and added to the
schedule (if this course has a lab section, one of these is added as well). From there, the selection of
viable courses is recomputed, removing all of the courses that would overlap in time with the one
already added to the schedule. One of these new viable courses is then added. This process is repeated
until a schedule is created with the requested number of classes.

The number of available seats is retrieved from the school's registration site using
the webscraper I wrote in scraper.py. This just uses http requests, so it is also very fast.
