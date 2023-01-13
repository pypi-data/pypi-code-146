import os, yaml

# Channels are expected to be named <major>.<minor>-{candidate,fast,release}
PACKAGE_FILE_FORMAT = {
    'channels': [
            {'name': '{}-candidate',
            'currentCSV': ''},
            {'name': '{}-fast',
            'currentCSV': ''},
            {'name': '{}-stable',
            'currentCSV': ''}
    ],
    'defaultChannel': '{}-{}',
    'packageName': ''
}

class Package:
    PACKAGE_FILE_FORMAT = {
        'channels': [],
        'defaultChannel': '{}-{}',
        'packageName': ''
    }

    def __init__(self, package=None, operator=None, default_channel=None):
        if package is not None:
            self.operator = package['packageName']
            self.channels = []
            self.default_channel = package['defaultChannel']
            for c in package['channels']:
                ch = Channel(c['name'], c['currentCSV'])
                self.channels.append(ch)
        else:
            self.channels = []
            self.operator = operator if operator is not None else ''
            self.default_channel = default_channel if default_channel is not None else ''

    def __str__(self):
        return 'Package class for {} operator'.format(self.operator)

    def get_channel(self, name):
        for c in self.channels:
            if c.get_name() == name:
                return c

    def get_channels(self):
        channels = []
        for c in self.channels:
            channels.append(c)
        return channels

    def create_channel(self, name, current_csv, default=False):
        ch = Channel(name, current_csv)
        self.channels.append(ch)
        if default:
            self.default_channel = name

    def get_formatted(self):
        f = self.PACKAGE_FILE_FORMAT
        f['packageName'] = self.operator
        f['defaultChannel'] = self.default_channel
        f['channels'] = []
        for c in self.channels:
            f['channels'].append({'name': c.get_name(), 'currentCSV': c.get_current_csv()})
        return f

    def set_default_channel(self, default_channel):
        self.default_channel = default_channel

    def set_operator(self, operator):
        self.operator = operator

    def update_channel(self, channel, new_csv):
        for c in self.channels:
            if c.get_name() == channel:
                c.set_current_csv(new_csv)

    def promote_channel(self, promote_from, promote_to):
        self.update_channel(promote_to, self.get_channel(promote_from).get_current_csv())

class Channel:
    def __init__(self, name, currentCSV):
        self.name = name
        self.currentCSV = currentCSV

    def get_current_csv(self):
        return self.currentCSV

    def set_current_csv(self, new_csv):
        self.currentCSV = new_csv

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name