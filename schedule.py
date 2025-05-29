

""""
Schedule State and Generation classes, will be used
in a tree-search algorithm to generate possible schedules
"""
import csv2dict

import re

import bisect

import sys


"""
Represents the state of a possible schedule
"""
class State:

    def __init__(self):
        ## A representation of the schedule for a week. Used to make sure none of the chosen courses conflict
        # with each other
        self.classes = {'Monday':[],
                'Tuesday':[],
                'Wednesday':[],
                'Thursday':[],
                'Friday':[],
                'Saturday':[],
                'Sunday':[],
                'None':[]}

        # a list of the CRNs in the above schedule.
        # makes state comparison and result retrieval
        # much easier
        self.crns = []

        # check for repeats
        self.classNames = set()

        # non required subjects. Should only be one of each
        self.nonReqSubject = set()


"""
Used for aiding in generation of possible schedules.
"""
class Schedule:

    def __init__(self):
        # used to convert date strings to integers
        self.monthDict = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Dec': '12'
        }
    """
    Helper function. Converts a class's time string to an array with the
    start and end times as 24-hour format integers. Makes
    time comparisons easier
    """
    def timeTranslate(self, timestr:str) -> tuple[int,int]:
    #print(timestr)
        if timestr == "":
            return (-1, -1)
        startEnd = timestr.split(' - ')
        return (startEnd[0], startEnd[1])


    def dateTranslate(self, rawStart, rawEnd):
        # no dates, online or special class
        if rawStart == '':
            return (-1, -1)

        startList = rawStart.split('-')
        endList = rawEnd.split('-')

        # formatted as day-month-year, I want year-month-day
        newStart = int(startList[2] + self.monthDict[startList[1]] + startList[0])
        newEnd = int(endList[2] + self.monthDict[endList[1]] + endList[0])

        return (newStart, newEnd)
    """
    Given sets of user-defined parameters:
      - semester
      - required - classes that MUST be a part of the generated schedule
        specified by subj+num
      - soft - general guidelines for what should be in the schedule, subject+numrange
    Goes through course database and collects all classes that pertain to these
    requirements. These will be considered in the generateLegalClasses function 
    """
    def generateClassPool(self, semesterFile:str, requiredParams:list, softParams:dict, latestTime):
        # will either use dictionary or sql requests.
        semesterDict = csv2dict.csv2dict().parseCsv(semesterFile)

        # required and possible classes
        req = {}
        pos = {}

        for data in semesterDict.values():
            # see if course in in soft parameter range
            soft = False
            if data['subject'] in softParams.keys():
                sub = data['subject']
                fullRange = softParams[sub].split('-')
                loRange = fullRange[0]
                hiRange = fullRange[1]

                if loRange <= data['course num'] < hiRange:
                    soft = True


            if [data['subject'], data['course num']] in requiredParams or soft:
                rawTimes = data['times']
                newTimes = []
                for time in rawTimes:
                    newTimes.append(self.timeTranslate(time))

                # see if class is early enough
                tooLate = False 
                for times in newTimes:
                    if latestTime != -1 and (times[0] > latestTime or times[1] > latestTime):
                        tooLate = True
                
                if tooLate:
                    continue

                rawDays = data['days']
                newDays = []
                for days in rawDays:
                    newDays.append(days.split(','))

                rawStarts = data['start dates']
                rawEnds = data['end dates']
                newDates = []
                for i in range(len(rawStarts)):
                    newDates.append(self.dateTranslate(rawStarts[i], rawEnds[i]))

                if [data['subject'], data['course num']] in requiredParams:
                    req[data['crn']] = {'crn': data['crn'], 'subject': data['subject'], 'title': data['title'], 'section': data['section'], 'num': data['course num'], 'days': newDays, 'times': newTimes, 'dates': newDates, 'links': data['links']}

                else:
                    pos[data['crn']] = {'crn': data['crn'], 'subject': data['subject'], 'title': data['title'], 'section': data['section'], 'num': data['course num'], 'days': newDays, 'times': newTimes, 'dates': newDates, 'links': data['links']}


        return (req, pos)


    """
    See if two sets of times for a course overlap
    """
    def timeOverlapCheck(self, times1:tuple, times2:tuple):
        # timeless online class
        if times1 == (-1,-1) or times2 == (-1,-1):
            return False

        overlap = (max(times1[0], times2[0]), min(times1[1], times2[1]))
        return overlap[0] < overlap[1]


    """
    See if two sets of start and end dates overlap
    """
    def dateOverlapCheck(self, dates1:tuple, dates2:tuple):

        if dates1 == (-1, -1) or dates2 == (-1, -1):
            return False
        
        overlap = (max(dates1[0], dates2[0]), min(dates1[1], dates2[1]))
        return overlap[0] <= overlap[1]
    


    """
    Checks if a class is able to fit into an existing schedule
    """
    def scheduleOverlapCheck(self, possibleCourse, state):
        # see if this course overlaps with any times in the schedule

        # this is an online course, won't overlap with anything
        if possibleCourse['days'][0][0] == '':
            return False


        ## look at all date ranges
        for i in range(len(possibleCourse['dates'])):
            # loot at individual days in this date range
            for j in range(len(possibleCourse['days'][i])):
                # time for this day of this course
                possibleDay = possibleCourse['days'][i][j]
                possibleTime = possibleCourse['times'][i]

                for stateCourse in state.classes[possibleDay]:
                    for k in range(len(stateCourse['dates'])):
                        if self.dateOverlapCheck(possibleCourse['dates'][i], stateCourse['dates'][k]):
                            if self.timeOverlapCheck(stateCourse['times'][k], possibleTime):
                                return True

        return False
        

    """
    Generates all legal classes from user-defined pool
    that can be added to the specified state object.
    """ 
    def generateLegalClasses(self, state:State, possibleClassPool:dict):


        legalClasses = {}
        for possibleCourse in possibleClassPool.values():
           # some courses that don't meet regularly have multiple sets of dates
           # and times. Need to make sure none overlap
            # check if an instance of this class is already in the state's schedule
            if possibleCourse['subject']+possibleCourse['num'] in state.classNames:
                continue

            # see if this course overlaps with any times in the schedule
            if not self.scheduleOverlapCheck(possibleCourse, state):
                legalClasses[possibleCourse['crn']] = possibleCourse
                
        return legalClasses


    def copyState(self, state:State):
        newState = State()

        for key in newState.classes:
            for course in state.classes[key]:
                newState.classes[key].append(course)


        for crn in state.crns:
            newState.crns.append(crn) 


        for name in state.classNames:
            newState.classNames.add(name)

        return newState
    

    """
    Applies given legal class to the given state
    """ 
    def courseToState(self, state:State, course:dict):
        bisect.insort_left(state.crns, course['crn'])
        state.classNames.add(course['subject']+course['num'])



        # online class, doesn't pertain to any day
        if course['days'][0][0] == '':
            state.classes['None'].append(course)
            return

        for daySet in course['days']:
            for day in daySet:
                state.classes[day].append(course)



    """
    Once a complete schedule is generated, the seat availability for each class will be checked using the seatChecker class. If any class
    doesn't have available seats, must continue.
    ** - required classes are checked immediately, as if there is no possible schedule involving these classes, there's no point in searching.
    """
    def checkSeats(self, state:State):
        x= 5

"""
# tests
if __name__ == '__main__':     
    test = Schedule()
    time2 = (1500, 1600)
    time1 = (1200, 1500)
    print(test.timeOverlapCheck(time1, time2))
    pool = test.generateClassPool('2025_Winter_Term.csv', [['CMPT', '141'], ['CMPT', '145'], ['CMPT', '370']], {'HIST': '(10[0-9]|1[1-9][0-9]|[23][0-9]{2}|400)'})
    stateTest = State()
    set1 = test.generateLegalClasses(stateTest, pool)
    keys = list(pool.keys())
    test.courseToState(stateTest, pool[keys[0]])

    set2 = test.generateLegalClasses(stateTest, pool)
    keys = list(set2.keys())
    test.courseToState(stateTest, set2[keys[0]])

    set3 = test.generateLegalClasses(stateTest, pool)
    keys = list(set3.keys())
    test.courseToState(stateTest, set3[keys[0]])

    set4 = test.generateLegalClasses(stateTest, pool)
    keys = list(set4.keys())
    test.courseToState(stateTest, set4[keys[0]])

    set5 = test.generateLegalClasses(stateTest, pool)
    #test.courseToState(stateTest, set5[0])

    for course in set4.values():
        print(course)

    print(len(set1), len(set2), len(set3), len(set4), len(set5))
    print(stateTest.crns)
    print(test.timeTranslate('12:30 AM - 1:55 PM'))


    o
    print(overlap)
    if overlap[0] < overlap[1]:
        print('overlap')"
    """