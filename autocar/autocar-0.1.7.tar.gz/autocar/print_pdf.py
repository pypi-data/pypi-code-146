try:
    import PyPDF2
    import os
    import warnings
    import time
    import datetime
    import subprocess
    import configparser
    import sys
    import extract_msg
except ModuleNotFoundError:
    print('Ensure all dependencies are installed.')
    print('Run the following command:')
    print('pip install -r requirements.txt --upgrade')
    _ = input('Press Enter to exit')
    exit()

# Dependency: Ghostscript 9.52 for Windows (64 bit)
# https://www.ghostscript.com/download/gsdnld.html

APPNAME = 'printpdf'

# Disable warnings
warnings.filterwarnings('ignore')


def _print_progress_bar(iteration, total, prefix='', suffix='', decimals=0, length=100, fill='█', printEnd='\r'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def read_user_settings():
    config = configparser.ConfigParser()

    if sys.platform == 'win32':
        dir_appdata = os.path.join(os.environ['APPDATA'], APPNAME)
    else:
        dir_appdata = os.path.expanduser(os.path.join("~", "." + APPNAME))

    try:
        config.read_file(open(os.path.join(dir_appdata, 'print_pdf_userdata.ini')))
        rv_allowed_pages = int(config['UserData']['allowed_pages'])
        rv_printer = config['UserData']['printer']
        rv_printfolder = config['UserData']['printfolder']
        return rv_allowed_pages, rv_printer, rv_printfolder
    except FileNotFoundError:
        print('First time setup....')
        print('Enter user settings:')

        # User input
        while True:
            rv_printfolder = input('Enter the print folder\n')
            if not rv_printfolder:
                print('No entry')
                continue
            else:
                break

        while True:
            rv_printer = input('Enter the printer name\n')
            if not rv_printer:
                print('No entry')
                continue
            else:
                break

        while True:
            try:
                rv_allowed_pages = int(input('Enter the maximum allowed pages to print per file\n'))
                if not rv_allowed_pages:
                    print('No entry')
                    continue
            except ValueError:
                print('Please enter a number')
                continue
            else:
                break

        config['UserData'] = {}
        config['UserData']['allowed_pages'] = str(rv_allowed_pages)
        config['UserData']['printer'] = rv_printer
        config['UserData']['printfolder'] = rv_printfolder

        if not os.path.isdir(dir_appdata):
            os.makedirs(os.path.join(dir_appdata))
        with open(os.path.join(dir_appdata, 'print_pdf_userdata.ini'), 'w') as configfile:
            config.write(configfile)

        return rv_allowed_pages, rv_printer, rv_printfolder


def set_user_settings():
    config = configparser.ConfigParser()
    if sys.platform == 'win32':
        dir_appdata = os.path.join(os.environ['APPDATA'], APPNAME)
    else:
        dir_appdata = os.path.expanduser(os.path.join("~", "." + APPNAME))

    config.read_file(open(os.path.join(dir_appdata, 'print_pdf_userdata.ini')))
    allowed_pages = int(config['UserData']['allowed_pages'])
    printer = config['UserData']['printer']
    printfolder = config['UserData']['printfolder']

    # User input
    print(f'Print folder: {printfolder}')
    args = input('Enter "Y" to change the print folder\n')
    if args == 'Y' or args == 'y':
        while True:
            printfolder = input('Enter the print folder\n')
            if not printfolder:
                print('No entry')
                continue
            else:
                break

    print(f'Printer: {printer}')
    args = input('Enter "Y" to change the printer\n')
    if args == 'Y' or args == 'y':
        while True:
            printer = input('Enter the printer name\n')
            if not printer:
                print('No entry')
                continue
            else:
                break

    print(f'Maximum allowed pages to print per file: {allowed_pages}')
    args = input('Enter "Y" to change the maximum allowed pages\n')
    if args == 'Y' or args == 'y':
        while True:
            try:
                allowed_pages = int(input('Enter the maximum allowed pages to print per file\n'))
                if not allowed_pages:
                    print('No entry')
                    continue
            except ValueError:
                print('Please enter a number')
                continue
            else:
                break

    config['UserData'] = {}
    config['UserData']['allowed_pages'] = str(allowed_pages)
    config['UserData']['printer'] = printer
    config['UserData']['printfolder'] = printfolder

    if not os.path.isdir(dir_appdata):
        os.makedirs(dir_appdata)
    with open(os.path.join(dir_appdata, 'print_pdf_userdata.ini'), 'w') as configfile:
        config.write(configfile)


def extract_pdf_pages(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PyPDF2.PdfFileReader(f, strict=False)
        nr_pages = pdf.getNumPages()

    return nr_pages


def createcsv(file_name, columns):
    if not os.path.isfile(file_name):
        try:
            with open(file_name, 'a') as csv_file:
                csv_file.write(columns + '\n')
        except Exception:
            print(f'{file_name} file is open. Cannot write to it. Please close the file', '\n')


def main():
    print("""
██████╗░██████╗░██╗███╗░░██╗████████╗  ██████╗░██████╗░███████╗
██╔══██╗██╔══██╗██║████╗░██║╚══██╔══╝  ██╔══██╗██╔══██╗██╔════╝
██████╔╝██████╔╝██║██╔██╗██║░░░██║░░░  ██████╔╝██║░░██║█████╗░░
██╔═══╝░██╔══██╗██║██║╚████║░░░██║░░░  ██╔═══╝░██║░░██║██╔══╝░░
██║░░░░░██║░░██║██║██║░╚███║░░░██║░░░  ██║░░░░░██████╔╝██║░░░░░
╚═╝░░░░░╚═╝░░╚═╝╚═╝╚═╝░░╚══╝░░░╚═╝░░░  ╚═╝░░░░░╚═════╝░╚═╝░░░░░""")
    # Read user settings
    try:
        ALLOWED_PAGES, GHOSTSCRIPT_PRINTER, PRINTFOLDER = read_user_settings()
    except Exception:
        print('Error: unable to read user settings. Using default settings')
        PRINTFOLDER = os.path.dirname(os.path.realpath(__file__))
        ALLOWED_PAGES = 30
        GHOSTSCRIPT_PRINTER = '\\\\gvwac91\\GVWACP82'

    # Print user settings
    print('Print Settings:')
    print('--------------------')
    print(f'Print folder: {PRINTFOLDER}')
    print(f'Printer: {GHOSTSCRIPT_PRINTER}')
    print(f'Maximum allowed pages to print per file: {ALLOWED_PAGES}')
    print('--------------------')

    # Prompt
    args = input('Press Enter to print and "C" to change settings\n')
    while args == 'C' or args == 'c':
        try:
            set_user_settings()
            # Read user settings
            try:
                ALLOWED_PAGES, GHOSTSCRIPT_PRINTER, PRINTFOLDER = read_user_settings()
            except Exception:
                print('Error: unable to read user settings. Using default settings')
                PRINTFOLDER = os.path.dirname(os.path.realpath(__file__))
                ALLOWED_PAGES = 30
                GHOSTSCRIPT_PRINTER = '\\\\gvwac91\\GVWACP82'
            print('Print Settings:')
            print('--------------------')
            print(f'Print folder: {PRINTFOLDER}')
            print(f'Printer: {GHOSTSCRIPT_PRINTER}')
            print(f'Maximum allowed pages to print per file: {ALLOWED_PAGES}')
            print('--------------------')
            args = input('Press Enter to print and "C" to change settings\n')
        except Exception:
            print('Error: unable to set user settings.')
            print('Default settings:')
            print('--------------------')
            print(f'Print folder: {PRINTFOLDER}')
            print(f'Printer set: {GHOSTSCRIPT_PRINTER}')
            print(f'Maximum allowed pages to print per file: {ALLOWED_PAGES}')
            print('--------------------')
            args = input('Press Enter to print with default settings')

    # Ghostscript path
    ghostscript_path = r'gs\gs9.53.3\bin\gswin64c.exe'

    try:
        GHOSTSCRIPT_ARGS = '"' + ghostscript_path + '" ' \
            '-sDEVICE=mswinpr2 ' \
            '-dBATCH ' \
            '-dNOPAUSE ' \
            '-dFitPage ' \
            '-dNoCancel ' \
            '-dNORANGEPAGESIZE ' \
            '-sOutputFile="%printer%' + GHOSTSCRIPT_PRINTER + '" '
    except UnboundLocalError:
        print('Please ensure that Ghostscript is installed to the "Program Files" directory')
        _ = input('Press Enter to exit')
        exit()

    # Declarations
    too_many_pg_files = []
    printed_files = []
    corrupt_files = []
    bool_too_many = False
    bool_corrupt_pdf = False
    time_now = time.time()

    # Create csv file if does not exist
    createcsv(os.path.join(PRINTFOLDER, 'data_printed.csv'), 'Time,Files Printed,Files Not Printed')

    # Get print directory
    cur_dir_path = PRINTFOLDER
    list_cur_dir_path = list(cur_dir_path)
    list_cur_dir_path[0] = list_cur_dir_path[0].upper()
    cur_dir_path = ''.join(list_cur_dir_path)

    # Extract all attachments from msg
    # Get list of all files in print directory for extract_msg
    try:
        all_files_extr_msg = [f for f in os.listdir(cur_dir_path) if os.path.isfile(os.path.join(cur_dir_path, f))]
    except OSError:
        print('Ensure the print folder is a valid path')
        _ = input('Press Enter to exit')
        exit()

    all_file_paths_extr_msg = [cur_dir_path + '\\' + _ for _ in all_files_extr_msg]

    bool_email_files = False
    for file_path in all_file_paths_extr_msg:
        if file_path.endswith('.msg') or file_path.endswith('.MSG'):
            bool_email_files = True

    if bool_email_files:
        args = input('There are email files. Press Enter to extract attachments from email files and "N" to skip\n')
        args = args.lower()
        if args != 'n':
            counter = 1
            finished_counter = 1
            attachments_counter = 1
            for file_path in all_file_paths_extr_msg:
                if file_path.endswith('.msg') or file_path.endswith('.MSG'):
                    _print_progress_bar(counter, len(all_file_paths_extr_msg))
                    try:
                        msg = extract_msg.openMsg(file_path)
                        for msg_attachment in msg.attachments:
                            msg_filename = msg_attachment.longFilename
                            now_time = datetime.datetime.today().strftime('%H-%M-%S-%f')
                            msg_filename = 'From_Email-' + msg_filename[:-4] + '-' + now_time + msg_filename[-4:]
                            msg_attachment.save(customPath=cur_dir_path, customFilename=msg_filename)
                            attachments_counter += 1
                        finished_counter += 1
                    except Exception:
                        print('Error extracting attachment of file: ' + msg.filename)
                counter += 1
            print(f'Completed extracting {attachments_counter} attachments from {finished_counter} email files')
            _ = input('Press Enter to print\n')
    # End Extract all attachment from msg

    # Start Print
    # Get list of all files in print directory
    try:
        cur_dir_all_files = [f for f in os.listdir(cur_dir_path) if os.path.isfile(os.path.join(cur_dir_path, f))]
    except OSError:
        print('Ensure the print folder is a valid path')
        _ = input('Press Enter to exit')
        exit()

    all_file_paths = [cur_dir_path + '\\' + _ for _ in cur_dir_all_files]

    print('----START PRINT----')
    for file_path in all_file_paths:
        file_name = os.path.basename(file_path)
        if file_path.endswith('.pdf') or file_path.endswith('.PDF'):
            try:
                nr_pages = extract_pdf_pages(file_path)

                if nr_pages < ALLOWED_PAGES:
                    print('Printing file: ', file_name,)
                    print('Number of pages: ', nr_pages, '\n')

                    # PRINT FILE
                    sub_pro_ghostscript = GHOSTSCRIPT_ARGS + \
                        '"' + file_path + '"'
                    subprocess.call(sub_pro_ghostscript, shell=True)

                    # Write printed file to csv
                    time_now = time.time()
                    print_time = datetime.datetime.fromtimestamp(time_now).strftime('%m/%d/%y %H:%M:%S')
                    try:
                        with open(os.path.join(PRINTFOLDER, 'data_printed.csv'), 'a') as csv_file:
                            csv_file.write(print_time + ',' + file_name + '\n')
                    except Exception:
                        print('data_printed.csv file is open. Cannot write to it. Please close the file', '\n')

                    # Append to printed files to list
                    printed_files.append(file_name)
                else:
                    bool_too_many = True

                    time_now = time.time()
                    print_time = datetime.datetime.fromtimestamp(time_now).strftime('%m/%d/%y %H:%M:%S')
                    try:
                        with open(os.path.join(PRINTFOLDER, 'data_printed.csv'), 'a') as csv_file:
                            csv_file.write(print_time + ',,' + file_name + '\n')
                    except Exception:
                        print('data_printed.csv file is open. Cannot write to it. Please close the file', '\n')
                    too_many_pg_files.append(file_name)

            except Exception:
                bool_corrupt_pdf = True

                time_now = time.time()
                print_time = datetime.datetime.fromtimestamp(time_now).strftime('%m/%d/%y %H:%M:%S')
                try:
                    with open(os.path.join(PRINTFOLDER, 'data_printed.csv'), 'a') as csv_file:
                        csv_file.write(print_time + ',,' + file_name + '\n')
                except Exception:
                    print('data_printed.csv file is open. Cannot write to it. Please close the file', '\n')
                corrupt_files.append(file_name)

    # Show the files printed
    print('The following files were printed: ', len(printed_files))
    print(*printed_files, sep='\n')
    print('\n')

    if bool_too_many:
        print(f'The following files had > {ALLOWED_PAGES} pages and were not printed: ', len(too_many_pg_files))
        print(*too_many_pg_files, sep='\n')
        print('\n')

    if bool_corrupt_pdf:
        print('The following files were corrupt and could not print. Try printing manually: ', len(corrupt_files))
        print(*corrupt_files, sep='\n')
        print('\n')

    print('----END PRINT----')
    _ = input('Press Enter to exit')


if __name__ == '__main__':
    main()
