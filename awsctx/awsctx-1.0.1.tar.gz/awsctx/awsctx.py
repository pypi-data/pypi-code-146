import re
import shutil
from pathlib import Path

def parseCredentialsFile(creds):

    # DECLARING VARIABLES

    data = {} ## used to hold the creds file data in json format
    pattern = "\[.*]" ## pattern to find different sections
    hold =""
    previous = ""
    count = 0 ## used for counting the line number

    rePattern = re.compile(pattern, re.IGNORECASE)
    last_used = ""

    # for currently used
    used_pattern = "^#current_profile=.*$"
    reUsedPattern = re.compile(used_pattern,re.IGNORECASE)
    lines = creds.split("\n")
    for line in lines:
        if re.match(reUsedPattern,line):
            last_used = line.split("#current_profile=")[1]

        elif re.match(rePattern,line):
            previous = hold
            hold = line.split("\n")[0].replace("[","").replace("]","")
            data[hold] = {}
            data[hold]['text'] = ""
            data[hold]['start'] = count
            data[hold]['end'] = -1
            if len(previous) == 0:
                pass
            else:
                data[previous]['end'] = count - 1

        else:
            line = line.strip()
            if len(line)>0:
                data[hold]['text']+=line + "\n"
        count+=1

    return data, last_used


def printParsedFile(data,last_used):
    found = False
    for line in data.keys():
        if line == last_used and len(last_used)>0:
            print('\x1b[6;30;42m' + line + '\x1b[0m')
            found = True
        else:
            print(line)
    if not found and len(last_used)>0:
        print('\033[91m'+f'Profile {last_used} not found'+'\033[0m')


def getDataAndRemoveDefault(creds,data,last_used):
    lines = creds.split("\n")
    if 'default' in data.keys():
        del lines[int(data['default']['start']):int(data['default']['end'])+1]
        if len(last_used) > 0:
            del lines[0:1]
        del data['default']
        creds = '\n'.join(lines)
    
    return creds


def generateNewCredsFile(data,current_used):
    creds = f'#current_profile={current_used}\n'+'[default]\n'

    # Get default setup
    creds+=data[current_used]['text']+"\n"

    # setup rest of the creds
    for key in data.keys():
        creds+=f"[{key}]\n{data[key]['text']}\n"

    creds = re.sub(r'\n+', '\n', creds).strip()

    return creds

def ctxmanager(option):
    home = str(Path.home())
    WORKING_DIRECTORY = f"{home}/.aws/"

    # Get the credentials file
    file_name = WORKING_DIRECTORY+'credentials'
    backup_file_name = WORKING_DIRECTORY+'credentials.bk'
    f = open(file_name, "r")
    creds = f.read()
    f.close()

    if option == 'configure':
        option = None
        data_entry = True
    else:
        data_entry = False

    if not data_entry:
        data, last_used = parseCredentialsFile(creds)
        creds = getDataAndRemoveDefault(creds,data,last_used)
        if option:
            if option in data.keys():
                creds = f'#current_profile={option}\n'+'[default]\n'+data[option]['text']+'\n'+creds
                creds = re.sub(r'\n+', '\n', creds).strip()
                # Create a backup
                shutil.copy(file_name,backup_file_name)
                # Write file
                f = open(file_name, "w")
                f.write(creds)
                f.close()
            else:
                print(f"Invalid Option: {option}. Following are the available profiles:")
                print("-------------------")
                printParsedFile(data,last_used)
        else:
            printParsedFile(data,last_used)
    else:
        new_profile_data = ''
        print("Paste data to add a profile to your AWS credentials file.\n[Press Double Enter After Pasting]")
        while True:
            dummy = input()+'\n'
            if dummy=='\n':
                break
            new_profile_data += dummy
        data, last_used = parseCredentialsFile(creds)
        creds = getDataAndRemoveDefault(creds,data,last_used)
        # data configuring
        new_split = new_profile_data.split("\n")
        profile_name = new_split[0].replace("[","").replace("]","")
        if profile_name in data.keys():
            data[profile_name]['text'] = '\n'.join(new_split[1:])
        else:
            data[profile_name] = {}
            data[profile_name]['text'] = '\n'.join(new_split[1:])

        creds = generateNewCredsFile(data,profile_name)
        # Create a backup
        shutil.copy(file_name,backup_file_name)
        # Write file
        f = open(file_name, "w")
        f.write(creds)
        f.close()
        print('New Profile: '+'\x1b[6;30;42m' + profile_name + '\x1b[0m' + ' imported successfully and is currently active.')