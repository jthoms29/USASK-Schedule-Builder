from schedule import State
from schedule import Schedule
import random
import time

class stochasticSearch:

    def generateSchedule(self, termCSV:str, requiredCourses:list, softCourses:dict, totalCourseNum, latestTime):
        if totalCourseNum < len(requiredCourses):
            return ['0000']


        pool = Schedule().generateClassPool(termCSV, requiredCourses, softCourses, latestTime)
        return self.search(pool[0], len(requiredCourses), pool[1], totalCourseNum)


    # Just randomly apply possible classes to the current schedule until you can get 5. 
    def search(self, required, numReq, soft, totalCourseNum):
        start = time.time()
        sched = Schedule()
        while True:
            # if taking longer than 10 seconds, likely impossible
            if time.time() - start > 10:
                return ['0000']

            addedCourses = 0
            newState = State()
            # first of all, add all of the required courses
            while addedCourses != numReq:
                # pick a class from required
                possibleCourses = sched.generateLegalClasses(newState, required)

                if len(possibleCourses) == 0:
                    break

                pickedCourse = random.choice(list(possibleCourses.values()))
                sched.courseToState(newState, pickedCourse)
                
                # see if any lab sections
                if pickedCourse['links'][0] != '':
                    possibleLinks = []
                    for crn in pickedCourse['links']:
                        if crn in possibleCourses.keys() and not sched.scheduleOverlapCheck(possibleCourses[crn], newState):
                            possibleLinks.append(possibleCourses[crn])

                    # try again
                    if len(possibleLinks) == 0:
                        break

                    pickedLink = random.choice(possibleLinks)
                    sched.courseToState(newState, pickedLink)

                
                addedCourses +=1



            # required courses added. Now for possible courses. Much the same process
            if addedCourses == numReq:
                while addedCourses != totalCourseNum:

                    possibleCourses = sched.generateLegalClasses(newState, soft)

                    if len(possibleCourses) == 0:
                        break

                    pickedCourse = random.choice(list(possibleCourses.values()))
                    sched.courseToState(newState, pickedCourse)
                
                    # see if any lab sections
                    if pickedCourse['links'][0] != '':
                        possibleLinks = []
                        for crn in pickedCourse['links']:
                            if crn in possibleCourses.keys() and not sched.scheduleOverlapCheck(possibleCourses[crn], newState):
                                possibleLinks.append(possibleCourses[crn])

                        # try again
                        if len(possibleLinks) == 0:
                            break

                        pickedLink = random.choice(possibleLinks)
                        sched.courseToState(newState, pickedLink)

                    addedCourses +=1

                # got a full schedule
                if addedCourses == totalCourseNum:
                    
                    for day in newState.classes:
                        newState.classes[day].sort(key=lambda course: course['times'][0][0])

                    return newState

test = stochasticSearch()

# add csv for term, a list of required classes, and a dictionary of possibly wanted classes with ranges, and the total number of desired courses in the schedule
# returns ['0000'] upon failure
start = time.time()
#print(test.generateSchedule('2025_Fall_term.csv', [['CMPT','381'], ['CMPT', '423'], ['LING', '349'], ['GEOL', '121'], ['CMPT', '394']], {}, 5, -1))
#print(time.time()- start)

