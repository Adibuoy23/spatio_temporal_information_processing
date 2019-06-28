#!/usr/bin/python

from datetime import datetime
import sys, cgi, cgitb, os

# log any errors in /pylogs/
cgitb.enable(display=0, logdir='pylogs')

# get form data from JavaScript
formdata = cgi.FieldStorage()

# get subjectID and dataString (JSON stringified array)
subjectID = formdata.getvalue('subjectID', 'subjectID_NULL')
dataString = formdata.getvalue('dataString', 'dataString_NULL')

# get string of current date and time
now = str(datetime.now())[:19].replace(":","_")

# write file in /data/ as 'A1GTK5ODM5JYA2 2018-07-09 11_56_41.txt
outputFilename = 'data/' + subjectID + ' ' + now + '.txt'
with open(outputFilename, 'w') as outputFile:
    outputFile.write(dataString)

# print header and 'Done.' message
sys.stdout.write('Content-type: text/plain; charset=UTF-8\n\n')
sys.stdout.write('Done.')
