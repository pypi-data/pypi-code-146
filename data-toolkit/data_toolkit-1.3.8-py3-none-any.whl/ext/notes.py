'''
Creates a note class with a folder, location, attachments, and a body

This is then used from the command line to create a note or add attachments to a note
eg, dt nt add -p 0 (adds latest screenshot to note in project 0)
'''
import pandas 
import os


def is_screenshot(file:str):
    # check if file is a screenshot
    # screenshots must match pattern Screen Shot 2022-05-15 at 12.13.04*.png
    # or '.Screen Shot 2020-07-06 at 20.02.05.png.icloud'
    if file.startswith('.Screen Shot') and file.endswith('.png.icloud'):
        return True
    elif file.startswith('Screen Shot') and file.endswith('.png'):
        return True
    else:
        return False

class Note:
    def __init__(self, project: str):
        self.project = project
        # self.attachments = attachments
        text = f"<body> <h1>Notes Notes for {project}</h1> </body> </html>"
        self.body = '''<html> <head> <style> body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 14px; line-height: 1.42857143; color: #333; background-color: #fff; } </style> </head> ''' + text

    def __str__(self):
        return f'{self.project} {self.location} {self.attachments} {self.body}'

    def __repr__(self):
        return f'{self.project} {self.location} {self.attachments} {self.body}'

    def create_project(self, project, text):
        # create a file in the project with the body of the note
        # create a project for each attachment
        # move the attachment to the project
        
        # check if path exists
        proj_p = os.path.join(os.path.expanduser('~'), 'notes', project)
        if not os.path.exists(proj_p):
            os.mkdir(proj_p)
            print('Created project {}'.format(project))
            
        # check if md file exists at proj_p
        md_file = os.path.join(proj_p, 'notes.md')
        if not os.path.exists(md_file):
            # create the file
            with open(md_file, 'w') as f:
                f.write(self.body)
                print('Created notes.md file at {}'.format(md_file))
        
        screen_p = os.path.join(os.path.expanduser('~'), 'notes',project, 'screenshots')
        if not os.path.exists(screen_p):
            os.mkdir(screen_p)
            print('Created screenshots folder at {}'.format(screen_p))
        
        
    # def add_note(self, project):
        
            
    def add_attachment(self, project):
        # add an attachment to the note in the given project
        p = os.path.join(os.path.expanduser('~'), 'notes', project, 'screenshots')

        # get all screenshots from the Desktop folder 
        screenshots = [os.path.join(os.path.expanduser('~'), 'Desktop', f) for f in os.listdir(os.path.expanduser('~') + '/Desktop') if is_screenshot(f)]

        # get the latest screenshot
        latest_screenshot = max(screenshots, key=os.path.getctime)

        # move the latest screenshot to the project folder
        tar_path = os.path.join(p, os.path.basename(latest_screenshot.replace(' ','_')))
        os.rename(latest_screenshot, tar_path)
        print('Moved {} screenshot to {}'.format(os.path.basename(latest_screenshot), p))
        
        
        notes_path = os.path.join(os.path.expanduser('~'), 'notes', project)
         
        with open(os.path.join(p, 'notes.md'), 'a') as f:
            f.write(f'![]({os.path.basename(latest_screenshot)})')
            
        print(f"Added {os.path.basename(latest_screenshot)} to {notes_path}")
        