import requests
import json
import time

termDict = {'2025 Spring Term': '202505',
            '2025 Summer Term': '202507',
            '2025 Fall Term': '202509', 
            '2026 Winter Term': '202601'}



def getSemester(session:requests.Session, uid:str, sem:str):
    url = 'https://banner.usask.ca/StudentRegistrationSsb/ssb/term/search?mode=search'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    payload = {
        'term': termDict[sem],
        'studyPath': "",
        'studyPathText': "",
        'startDatepicker': "",
        'endDatePicker': "",
        'uniqueSessionId': uid
    }

    response = session.post(url, headers=headers, params=payload)



def linkedSectionSearch(session:requests.Session, sem, crn):
    url = "https://banner.usask.ca/StudentRegistrationSsb/ssb/searchResults/fetchLinkedSections"

    querystring = {"term":termDict[sem],"courseReferenceNumber":crn}

    payload = ""
    headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.5",
    }

    response = session.request("GET", url, data=payload, headers=headers, params=querystring)
    return json.loads(response.text)


def courseSearch(session:requests.Session, sem, uid, pageOffset, pageMaxSize) -> dict:
    url = "https://banner.usask.ca/StudentRegistrationSsb/ssb/searchResults/searchResults"

    payload = ""
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
    }

    querystring = {"txt_term":termDict[sem],"startDatepicker":"","endDatepicker":"","uniqueSessionId":uid,"pageOffset":pageOffset,"pageMaxSize":pageMaxSize,"sortColumn":"subjectDescription","sortDirection":"asc"}
    response = session.request("GET", url, data=payload, headers=headers, params=querystring)
    return json.loads(response.text);



def courseSearchExact(session:requests.Session, uid:str, sem:str, subject:str, courseNum:str, crn=None):
    url = "https://banner.usask.ca/StudentRegistrationSsb/ssb/searchResults/searchResults"

    payload = ""
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
    }

    querystring = {
        "txt_subject": subject,
        "txt_courseNumber": courseNum,
        "txt_term":termDict[sem],
        "startDatepicker":"",
        "endDatepicker":"",
        "uniqueSessionId":uid,
        "pageOffset":'0',
        "pageMaxSize":'50',
        "sortColumn":"subjectDescription",
        "sortDirection":"asc"
    }

    resp = session.request("GET", url, data=payload, headers=headers, params=querystring)
    respText = json.loads(resp.text)
    # if a crn was specified, return data for that exact course only
    if crn != None:
        for course in respText['data']:
            if course['courseReferenceNumber'] == crn:
                return course

    # otherwise, return a list with each course
    return respText['data'];




def semesterScrape(sem):
    session = requests.Session()

    # the unique session id needed for most requests seems to just be a random 18 character string
    uid = str(int(time.time() * 100000000))

    # need to choose a semester before anything can be searched
    getSemester(sem, session, uid)

    # make an initial request to get the total number of courses in the semester
    resp = courseSearch(session, sem, uid, 0, 0)
    totalCourses = resp['totalCount']
    scrapedCourses = 0

    # this dictionary will hold the scraped data for each course
    courseData = {}
    # this list will hold the CRN of each course with a linked section. The linked sections for each course will be gathered separately
    coursesWithLinks = []

    # STEP ONE: GET MAJOR INFO FOR ALL COURSES
    while scrapedCourses < totalCourses:
        resp = courseSearch(session, sem, uid, scrapedCourses, 70)
        
        for courseInfo in resp['data']:
            day_chunks = []
            start_dates = []
            end_dates = []
            times = []

            # get meeting times for this course 
            for meeting in courseInfo['meetingsFaculty']:
                meet_days = []

                if meeting['meetingTime']['sunday']:
                    meet_days.append('Sunday')
                if meeting['meetingTime']['monday']:
                    meet_days.append('Monday')
                if meeting['meetingTime']['tuesday']:
                    meet_days.append('Tuesday')
                if meeting['meetingTime']['wednesday']:
                    meet_days.append('Wednesday')
                if meeting['meetingTime']['thursday']:
                    meet_days.append('Thursday')
                if meeting['meetingTime']['friday']:
                    meet_days.append('Friday')
                if meeting['meetingTime']['saturday']:
                    meet_days.append('Saturday')

                day_chunks.append(",".join(meet_days))
                start_dates.append(meeting['meetingTime']['startDate'])
                end_dates.append(meeting['meetingTime']['endDate'])
                times.append(f"{meeting['meetingTime']['beginTime']} - {meeting['meetingTime']['endTime']}")

            # add scraped course data to the full dictionary
            courseData[courseInfo['courseReferenceNumber']] = {
                'crn': courseInfo['courseReferenceNumber'],
                'subject': courseInfo['subject'],
                'title': courseInfo['courseTitle'].replace("\n",""),
                'course_num': courseInfo['courseNumber'],
                'credits': courseInfo['creditHours'],
                'section': courseInfo['sequenceNumber'],
                'campus': courseInfo['campusDescription'],
                'days': str(day_chunks)[1:-1],
                'start_dates': str(start_dates)[1:-1],
                'end_dates': str(end_dates)[1:-1],
                'times': str(times)[1:-1],
                'links': ""
            }

            if courseInfo['isSectionLinked']:
                coursesWithLinks.append(courseInfo['courseReferenceNumber'])

            scrapedCourses += 1


    # STEP TWO: GET LINKED SECTIONS FOR EACH COURSE
    total=0
    # associates each crn with a list of its linked sections
    linkedDict = {}
    for crn in coursesWithLinks:
        total+=1

        # courses added to dict both ways - if already in there don't need to process again
        if crn in linkedDict:
            continue

        linkedDict[crn] = []
        resp = linkedSectionSearch(session, sem, crn)

        # add linked crns to dict, both ways
        for course in resp['linkedData']:
            linkedCRN = course[0]['courseReferenceNumber']
            linkedDict[crn].append(linkedCRN)

        if linkedCRN in linkedDict:
            linkedDict[linkedCRN].append(crn)
        else:
            linkedDict[linkedCRN] = [ crn ]

    
    # add all of this new linked section data to the original dict
    for key in linkedDict:
        courseData[key]['links'] = ','.join(linkedDict[key])

    # STEP 3: WRITE ALL OF THIS DATA TO A CSV
    filename = sem.replace(" ", "_")
    csv = open(f"{filename}.csv", "w")
    csv.write("crn,subject,title,course_num,credits,section,campus,days,start_dates,end_dates,times,linked\n")

    for key in courseData:
        entry = courseData[key]
        csv.write(f'{entry["crn"]},{entry["subject"]},"{entry["title"]}",{entry["course_num"]},{entry["credits"]},{entry["section"]},"{entry["campus"]}","{entry["days"]}","{entry["start_dates"]}","{entry["end_dates"]}","{entry["times"]}","{entry["links"]}"\n')

    csv.close()


