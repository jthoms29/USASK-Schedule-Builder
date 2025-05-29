
from stochasticSearch import stochasticSearch
from schedule import State
import requests
import scraper
import time
from datetime import datetime


# a cache that holds the number of seats for every class chosen
# for the generated schedule. This cache limits the num of requests 
# that need to be made.
seatCache = {}

"""
get completely up to date seating info for some class. Gets seats for every
version of the given class, if the user generates multiple schedules it's likely
# that they'll need seating info for more than one section.
"""
def checkSeats(session:requests.Session, uid:str, sem:str, subj:str, num:str):
    # for some reason when I don't create a new session for each specific class search
    # it just returns the same json as the first class you search every time.
    session = requests.Session()
    uid = str(int(time.time() * 100000000))
    scraper.getSemester(session, uid, sem)

    # get seating info
    resp = scraper.courseSearchExact(session, uid, sem, subj, num)

    for courseInfo in resp:
        seatCache[courseInfo['courseReferenceNumber']] = courseInfo['seatsAvailable']


def toAmPm(twentFourHour:str):
    if twentFourHour == 'None':
        return 'None'
        
    return datetime.strptime(twentFourHour, "%H%M").strftime("%I:%M %p")

def toCalendar(date:int):
    # rearrange order
    dateStr = str(date)
    dateStr = dateStr[4:6] + '/' + dateStr[6:8] + '/' + dateStr[0:4]
    return dateStr

"""
Takes the time info (date, meeting times, days) from a class and puts it
into a readable format
"""
def formatTimes(course:dict) -> str:
    timeStr = ""
    for i in range(len(course['dates'])):
        timeStr += f"Meeting time {i+1}:\n"
        timeStr += "  " + toAmPm(course['times'][i][0]) + " - " + toAmPm(course['times'][i][1]) + "\n"
        timeStr += "  " + toCalendar(course['dates'][i][0]) + " - " + toCalendar(course['dates'][i][1]) + "\n"
    return timeStr


"""
Generate a visual represenation of the generated schedule
"""
def generateScheduleString(sched:State, session, uid, sem):
    sString = "\n\nNew Schedule:\n"
    for day in sched.classes:
        sString += f"================\n{day}:\n\n"
        for course in sched.classes[day]:
            sString += f"{course['subject']} {course['num']} - {course['title']} - section {course['section']}\n"
            sString += formatTimes(course)
            if course['crn'] not in seatCache:
                checkSeats(session, uid, sem, course['subject'], course['num'])

            sString += f"{seatCache[course['crn']]} seats available\n\n"

    sString += "\nCRNS: "
    for crn in sched.crns:
        sString += f"{crn}, "

    # get rid of the last unneeded comma
    return sString[0:-2] + "\n\n"



def runHelper():
    # start up a new request session. Used for getting up-to-date seating info
    session = requests.Session()
    uid = str(int(time.time() * 100000000))

    search = stochasticSearch();

    sem = ""
    while sem not in ('1', '2'):
        print("Input a semester ( (1) 2025 Fall Term, (2) 2026 Winter Term): ")
        sem = input()
        if sem not in ('1', '2'):
            print("Invalid input. Type 1 or 2")

        if sem == '1':
            sem = '2025 Fall Term'
            break
        elif sem == '2':
            sem = '2026 Winter Term'
            break

    scraper.getSemester(session, uid, sem)

    num_classes = - 1
    while num_classes < 1:
        print("Input total number of classes you want: ")
        num_classes_string = input()
        try:
            num_classes = int(num_classes_string)
            if num_classes < 1:
                print("Invalid input.")
        except:
            print("Invalid input.")


    required_class_list = None
    while required_class_list == None:
        print("Input a list of classes you require.")
        print(" Example input: \n  CMPT 353, CMPT 332, ENG 102, HIST 208")
        required_class_string = input()
        required_class_list = required_class_string.split(', ')
        required_class_list = [course.split(" ") for course in required_class_list]


    possible_class_dict = {}
    while possible_class_dict == None:
        print("Input a list of classes you possibly want - subjects with ranges")
        print("  Exmpale input:  \n  HIST 100-200, GEOG 200-300, MATH 100-400")


    filename = sem.replace(" ", "_") + ".csv"
    sched = search.generateSchedule(filename, required_class_list, possible_class_dict, num_classes, -1)
    print(generateScheduleString(sched, session, uid, sem))

    reroll = True
    while reroll:
        print("Generate another?: ('n' to stop, anything else to continue)")
        resp = input()
        if resp == 'n':
            break

        sched = search.generateSchedule(filename, required_class_list, possible_class_dict, num_classes, -1)
        print(generateScheduleString(sched, session, uid, sem))

runHelper()