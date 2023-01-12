import requests, datetime

class PythonNotifications():
    def __init__(self, token, id, appName):
        self.appName = appName
        self.errors = []
        self.warnings = []
        self.info = []
        self.url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text="

    def addMessage(self, msg, level='info'):
        now = datetime.datetime.now()
        if level == 'info':
            self.info.append(str(now).split('.')[0][:-3] + '\t' + msg)
        elif level == 'warning':
            self.warnings.append(str(now).split('.')[0][:-3] + '\t' + msg)
        elif level == 'error':
            self.errors.append(str(now).split('.')[0][:-3] + '\t' + msg)
        else:
            return '[ERROR] Level not found'
        
    def sendMessage(self, minLevel='info'):
        messageHeader = f'--------- {self.appName} app: SUMMARY ---------\n'
        errors = '\n'.join(self.errors) + '\n' if len(self.errors) > 0 else ''
        warnings = '\n'.join(self.warnings) + '\n' if len(self.warnings) > 0 else ''
        info = '\n'.join(self.info) + '\n' if len(self.info) > 0 else ''

        if minLevel == 'error':
            message = f'{messageHeader}\n[ERRORS]\n{errors}'
        elif minLevel == 'warning':
            message = f'{messageHeader}\n[WARNING]\n{warnings}\n[ERRORS]\n{errors}'
        elif minLevel == 'info':
            message = f'{messageHeader}\n[INFO]\n{info}\n[WARNINGS]\n{warnings}\n[ERRORS]\n{errors}'
        else:
            return '[ERROR] Level not found'
        
        return requests.get(self.url + message).json()
