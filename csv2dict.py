
import csv
# it doesn't work unless I do this
import re as re


class csv2dict:

    def parseCsv(self, filename):
        f = open(filename, 'r')
        dict = {}
        for line in csv.reader(f):

            # formatting, unessesary quotations because of nested commas and lists
            title = line[2].strip('"')


            # convert day collections to list. Extract single quotes from double with regex
            days = line[7].split(', ')
            days = [el.strip("'") for el in days]

            # start dates to list
            starts = line[8].split(', ') 
            starts = [el.strip("'") for el in starts]

            # end dates to list
            ends = line[9].split(', ')
            ends = [el.strip("'") for el in ends]

            # times to list
            times = line[10].split(', ')
            times = [el.strip("'") for el in times]

            links = line[11].split(',')

           # key is crn 
            dict[line[0]] = {'crn': line[0],
                            'subject': line[1],
                            'title': title,
                            'course num': line[3],
                            'credits': line[4],
                            'section': line[5],
                            'campus': line[6],
                            'days': days,
                            'start dates': starts,
                            'end dates': ends,
                            'times': times,
                            'links': links}

        #for key in dict:
        #   print(dict[key])
        return dict
""""
test = csv2dict()
test.parseCsv('2025_Summer_Term.csv')
"""