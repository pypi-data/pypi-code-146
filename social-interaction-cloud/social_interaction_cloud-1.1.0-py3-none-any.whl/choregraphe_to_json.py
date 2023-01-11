import re


class ChoregrapheToJson:

    def __init__(self):
        self.pattern = re.compile('names.append\\("(.+)"\\)\ntimes.append\\(\\[(.+)\\]\\)\nkeys.append\\(\\[(.+)]\\)')

    def parse(self, source: str, robot='nao', precision_factor_angles=1000, precision_factor_times=100):
        motion_file = {'motion': {},
                       'precision_factor_angles': precision_factor_angles,
                       'precision_factor_times': precision_factor_times,
                       'robot': robot}

        for match in self.pattern.finditer(source):
            times = [int(float(x)*precision_factor_times) for x in match.group(2).split(', ')]
            angels = [int(float(x)*precision_factor_angles) for x in match.group(3).split(', ')]

            motion_file['motion'][match.group(1)] = {'angles': angels, 'times': times}

        return motion_file
