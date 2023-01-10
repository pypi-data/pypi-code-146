import requests
from datetime import datetime
import json
import os
from applescript import run


def create_meeting(title, attendees, start, duration, notes=None):
    # osascript -e 'tell application "Microsoft Outlook"' -e 'set newMessage to make new outgoing message with properties {subject:"My Subject"}' -e 'make new recipient at newMessage with properties {email address:{name:"John Smith", address:"jsmith@example.com"}}' -e 'open newMessage' -e 'end tell'
    
    script = '''
    tell application "Microsoft Outlook"

    set currentTime to (the current date)

    set newEvent to make new calendar event with properties {location:"Dial In : +4319284090,  Conference code: 5270687926", start time:(currentTime + (60 * 60)), end time:(currentTime + (60 * 60) + (60 * 60) / 2), content:fileContents}

    set newMeeting to make new meeting message with properties {meeting:newEvent}
    open newMeeting

    end tell    
    '''
    
    exec_applescript(script)
    import ipdb; ipdb.set_trace()
    date = datetime.now()
    # date_of_meeting = date.strftime("%Y-%m-%d %H:%M:%S")
    # date_of_meeting = date.strftime("%d/%m/%Y")
    date_of_meeting = 'Monday, 10 October 2022 11:00:00'
    title = 'test title'
    location = 'room'
    
    # " -e 'set currentTime to (the current date)'" \
    import ipdb; ipdb.set_trace()
    
    
    cmd_str = "osascript -e 'tell application \"Microsoft Outlook\"' " \
        f"-e 'set newEvent to make new calendar event with properties {{location:\"{location}\", start time: (the current date), end time: (the current date + hours), content:\"{title}\"}}' " \
        "-e 'end tell'"
            
    print(cmd_str)
    
    os.system(cmd_str)

    
def print_all_cal_names():
    scripts = []

    for n in range(1,25):   
        script = f'''
        tell application "Microsoft Outlook"
            set theCalendar to calendar id {n}
            set calendarName to name of theCalendar
            return (calendarName, {n})
        end tell
        '''
        scripts.append(script)
    
    [ exec_applescript(s) for s in scripts ]
    
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
    
    # TODO: set time of todaysDate to 0 -> get the current time
    script_v0 = '''
    tell application "Microsoft Outlook"
        set out to ""
        set todaysDate to current date
        set time of todaysDate to 0
        repeat with c in (every calendar)
            if (count of c) > 0 then
                set theEvents to (every event of c whose start date ≥ todaysDate)
                repeat with current_event in theEvents
                    set out to out & summary of current_event & "\n"
                end repeat
            end if
        end repeat
        return out
    end tell

    '''
    
    working_script = '''
    tell application "Microsoft Outlook"
        set theCalendars to every calendar
        return theCalendars
    end tell
    '''
    
    old_script = '''
    tell application "Microsoft Outlook"
        set out to ""
        repeat with c in (every calendar)
            set theEvents to (every event of c)
            repeat with current_event in theEvents
                set out to out & summary of current_event & "\n"
            end repeat
        end repeat
        return out
    end tell

    '''
    # print_all_cal_names()
    script = '''
    var se = new Application("System Events");
    var process = se.applicationProcesses.byName("Microsoft Outlook");
    var theBrowser = process.windows.byName("Microsoft Outlook");
    theBrowser.entireContents();
    '''
    exec_applescript(script)
    
    
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
    
'''
SOURCE: 

https://github.com/netpappy/Outlook-AppleScript


(* The goal of this script is to create a new event with my WebEx (or other 
meeting information) automatically populated. Just edit the line below to 
include your meeting information. I then named my script mm, so I
can type CMD-SPACE and type mm to invoke the script

By Default it sets the meeting time for the next day at 12 PM *)

set eventLocation to "WebEx"


set theStartDate to (current date) + (1 * days)
set hours of theStartDate to 12
set minutes of theStartDate to 0
set seconds of theStartDate to 0
set theEndTime to theStartDate + (1 * hours)

# SET THE MEETING INFORMATION TEXT OR HTML FOR THE WEBEX INVITE SURROUNDED BY QUOTES
set theWebExInvite to "Put your text information for your meeting here, or use <html><h1>HTML Meeting Information </h1></html>"


tell application "Microsoft Outlook"
	activate
	set newMeeting to make new calendar event with properties {start time:theStartDate, end time:theEndTime, is private:false, location:eventLocation, content:theWebExInvite, has reminder:true}
	open newMeeting
end tell
'''
    
def ls_mtg():
    cmd_str = '''
    
    tell application "Microsoft Outlook"
	
        repeat with this_contact in contacts
            log "meeting room"
            log vcard data of this_contact as text
        end repeat
    end tell
    '''
    
    cmd = f"""osascript -e '{cmd_str}" to sleep'"""
    v = run(cmd)
    print(f"Result: {v}")
    
    # import ipdb; ipdb.set_trace()
    
def add_event():
    pass

def delete_event():
    pass

from subprocess import Popen

def exec_applescript(script):
    p = Popen(['osascript', '-e', script])

    
if __name__ == '__main__':
    # list_meetings()
    ls_mtg()

    # exec_applescript('say "I am singing la la la la" using "Alex" speaking rate 140 pitch 60')
    # exec_applescript('say "Still singing, hahaha" using "Alex" speaking rate 140 pitch 66')
    
    
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