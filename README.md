# USASK SCHEDULE BUILDER

A Python script to aid in choosing classes for the upcoming fall 2025 and winter 2026 semesters
at the University of Saskatchewan.

## Installation

### Windows

Make sure you have python3 installed on your PC.

[Download Python 3](https://www.python.org/)

Click the green button that says 'Code' near the top of this page. Press 'download ZIP'
Once downloaded unzip the folder.

If you don't have pip installed go to this link, download the file, and move it to the folder.
Pip is a package manager that allows you to add extra functionality to python.
[Download pip](https://bootstrap.pypa.io/get-pip.py)

Then, in the folder, click on the search bar. While
it's blue, type 'cmd' and press enter.

Now, type the following command

`py get-pip.py`

After that, type `py -m pip install requests`. \

This installs the requests module, which lets this script check how many seats are
available for any given class.

After that, type `py main.py` to run the script.

## Instructions

Clone this repository and run main.py. From there, follow the on-screen instructions. If a valid schedule
can be created from the given input parameters, it will be printed out, along with a list of the courses'
crns. Just copy this crn list use it to choose the classes for your schedule on the university's
registration site. The generation algorithm is very fast, so you can quickly generate a new possible
schedule if you're not happy with the one you are given.

The output for a successfully generated schedule will look something like this:

``` text
New Schedule:
================
Monday:

GEOL 121 - Earth Processes - section 01
CRN: 80194
Meeting time 1:
  11:30 AM - 12:20 PM
  09/03/2025 - 12/05/2025
240 seats available

CMPT 381 - Implementation of Graphical User Interfaces - section 03
CRN: 89392
Meeting time 1:
  12:30 PM - 01:20 PM
  09/03/2025 - 12/05/2025
80 seats available

CMPT 381 - Implementation of Graphical User Interfaces - section T07
CRN: 88334
Meeting time 1:
  03:30 PM - 04:20 PM
  09/03/2025 - 12/05/2025
40 seats available

================
Tuesday:

CMPT 394 - Simulation Principles - section 01
CRN: 84444
Meeting time 1:
  11:30 AM - 12:50 PM
  09/03/2025 - 12/05/2025
30 seats available

CMPT 423 - Machine Learning - section 01
CRN: 88327
Meeting time 1:
  01:00 PM - 02:20 PM
  09/03/2025 - 12/05/2025
20 seats available

LING 349 - Computational Linguistics - section 01
CRN: 83918
Meeting time 1:
  04:00 PM - 05:20 PM
  09/03/2025 - 12/05/2025
30 seats available

================
Wednesday:

GEOL 121 - Earth Processes - section 01
CRN: 80194
Meeting time 1:
  11:30 AM - 12:20 PM
  09/03/2025 - 12/05/2025
240 seats available

CMPT 381 - Implementation of Graphical User Interfaces - section 03
CRN: 89392
Meeting time 1:
  12:30 PM - 01:20 PM
  09/03/2025 - 12/05/2025
80 seats available

GEOL 121 - Earth Processes - section L05
CRN: 80198
Meeting time 1:
  02:30 PM - 05:20 PM
  09/03/2025 - 12/05/2025
40 seats available

================
Thursday:

CMPT 394 - Simulation Principles - section 01
CRN: 84444
Meeting time 1:
  11:30 AM - 12:50 PM
  09/03/2025 - 12/05/2025
30 seats available

CMPT 423 - Machine Learning - section 01
CRN: 88327
Meeting time 1:
  01:00 PM - 02:20 PM
  09/03/2025 - 12/05/2025
20 seats available

LING 349 - Computational Linguistics - section 01
CRN: 83918
Meeting time 1:
  04:00 PM - 05:20 PM
  09/03/2025 - 12/05/2025
30 seats available

================
Friday:

GEOL 121 - Earth Processes - section 01
CRN: 80194
Meeting time 1:
  11:30 AM - 12:20 PM
  09/03/2025 - 12/05/2025
240 seats available

CMPT 381 - Implementation of Graphical User Interfaces - section 03
CRN: 89392
Meeting time 1:
  12:30 PM - 01:20 PM
  09/03/2025 - 12/05/2025
80 seats available

================
Saturday:

================
Sunday:

================
None:


CRNS: 80194, 80198, 83918, 84444, 88327, 88334, 89392
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
