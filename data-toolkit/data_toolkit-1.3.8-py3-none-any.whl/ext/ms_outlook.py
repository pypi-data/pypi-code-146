import requests
from datetime import datetime
import json
import os
from applescript import run


def create_meeting(attendees, location, title, notes):
    '''
    tell application "Microsoft Outlook"

    set currentTime to (the current date)

    set newEvent to make new calendar event with properties {location:"Dial In : +4319284090,  Conference code: 5270687926", start time:(currentTime + (60 * 60)), end time:(currentTime + (60 * 60) + (60 * 60) / 2), content:fileContents}

    set newMeeting to make new meeting message with properties {meeting:newEvent}
    open newMeeting

    end tell    
    
    osascript -e 'tell application "Microsoft Outlook"' -e 'set newMessage to make new outgoing message with properties {subject:"My Subject"}' -e 'make new recipient at newMessage with properties {email address:{name:"John Smith", address:"jsmith@example.com"}}' -e 'open newMessage' -e 'end tell'
    '''
    date = datetime.now()
    # date_of_meeting = date.strftime("%Y-%m-%d %H:%M:%S")
    # date_of_meeting = date.strftime("%d/%m/%Y")
    date_of_meeting = 'Monday, 10 October 2022 11:00:00'
    title = 'test title'
    location = 'room'
    
    # " -e 'set currentTime to (the current date)'" \
    
    
    cmd_str = "osascript -e 'tell application \"Microsoft Outlook\"' " \
        f"-e 'set newEvent to make new calendar event with properties {{location:\"{location}\", start time: (the current date), end time: (the current date + hours), content:\"{title}\"}}' " \
        "-e 'end tell'"
            
    print(cmd_str)
    
    os.system(cmd_str)
    
def list_events():
    # TODO 
    ''' Some thoughts: Use JavaScript 
    https://developer.apple.com/library/archive/documentation/AppleApplications/Conceptual/CalendarScriptingGuide/Calendar-LocateanEvent.html
    http://blog.hakanserce.com/post/outlook_automation_mac/

    var outlook = Application("Microsoft Outlook");

    var selectedMessageSubject = outlook.selectedObjects()[0].subject();


    var app = Application.currentApplication();
    app.includeStandardAdditions = true;

    app.displayNotification(selectedMessageSubject);
    '218:351: execution error: Calendar got an error: Can’t get every event whose start date ≥ date "Sunday, 9 October 2022 at 01:00:00" and end date ≤ date "Sunday, 9 October 2022 at 01:00:00". (-1728)'
    
    tell (current date) to get (it's month as integer) & "-" & day & "-" & (it's year as integer)
    '''
    
    cmd_str = '''
    set theStartDate to current date
    set hours of theStartDate to 1
    set minutes of theStartDate to 0
    set seconds of theStartDate to 0
    set theEndDate to (theStartDate + (1 * days) - 1)
    
    tell application "Calendar"
        every event where its start date is greater than or equal to theStartDate and end date is less than or equal to theEndDate
    end tell
    '''
    # os.system(cmd_str)
    v = run(cmd_str)
    import ipdb; ipdb.set_trace()
    
def new_email():
    # https://gist.github.com/gourneau/5946401
    pass
    
    
orig_str = '''
    tell application "iCal"
    set out to ""
    set todaysDate to current date
    set time of todaysDate to 0
    repeat with c in (every calendar)
        set theEvents to (every event of c whose start date ≥ todaysDate)
        repeat with current_event in theEvents
            set out to out & summary of current_event & "\n"
        end repeat
    end repeat
    return out
    end tell
    '''
    
def ls_mtg():
    cmd_str = '''
    tell application "Microsoft Outlook"
    set out to ""
    set todaysDate to current date
    set time of todaysDate to 0
    repeat with c in (every calendar)
        set theEvents to (every event of c whose start date ≥ todaysDate)
        repeat with current_event in theEvents
            set out to out & summary of current_event & "\n"
        end repeat
    end repeat
    return out
    end tell
    '''
    v = run(cmd_str)
    import ipdb; ipdb.set_trace()
    
def add_event():
    pass

def delete_event():
    pass
    
# if __name__ == '__main__':
#     # list_meetings()
#     ls_mtg()
#     # create_meeting('','','','')
'''
    tell application "Microsoft Outlook"
    set out to ""
    set todaysDate to current date
    set time of todaysDate to 0
    repeat with c in (every calendar)
        set theEvents to (every event of c whose start date ≥ todaysDate)
        repeat with current_event in theEvents
            set out to out & summary of current_event & "\n"
        end repeat
    end repeat
    return out
    end tell

'''