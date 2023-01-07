import os
import json
import bunzbar.infos
import tsv_calendar

available = ["infos.battery",
             "infos.clck",
             "tsv.current.all",
             "tsv.current.name",
             "tsv.current.description",
             "tsv.current.start_time",
             "tsv.current.start_timer",
             "tsv.current.end_time",
             "tsv.current.end_timer",
             "tsv.next.all",
             "tsv.next.name",
             "tsv.next.description",
             "tsv.next.start_time",
             "tsv.next.start_timer",
             "tsv.next.end_time",
             "tsv.next.end_timer"]

options = ["tsv_path",
           "info_len"]

available.sort()
options.sort()


class config:
    def __init__(self):
        self.CFGPATH = os.path.join(os.path.expanduser('~'), ".config/bunzbar/")
        self.CONFIGFILE = os.path.join(self.CFGPATH, "config.json")

        self.update()
        if self.exists("tsv_path"):
            self.tsv = tsv_calendar.TSV_Read(self.getv("tsv_path"))

    def update(self):
        if not os.path.exists(self.CFGPATH):  # Create config folder
            os.makedirs(self.CFGPATH, exist_ok=True)

        if not os.path.exists(self.CONFIGFILE):  # Create config file
            data = json.loads('{"available":["infos.clck"],"active":["infos.clck"]}')
            open(self.CONFIGFILE, 'w').write(json.dumps(data, indent=4))

        config = json.load(open(self.CONFIGFILE, 'r'))
        config["available"] = available

        if "active" in config:
            for info in config["active"]:
                if info not in available:
                    config["active"].remove(info)
        else:
            config["active"] = []

        open(self.CONFIGFILE, 'w').write(json.dumps(config, indent=4))

    def available(self, list):
        if list == "info":
            return (available)
        elif list == "config":
            return (options)
        else:
            return ("<error>")

    def active(self):
        config = json.load(open(self.CONFIGFILE, 'r'))
        return (config["active"])

    def exists(self, name):
        config = json.load(open(self.CONFIGFILE, 'r'))
        return (name in config)

    def setc(self, key, value):
        config = json.load(open(self.CONFIGFILE, 'r'))
        if key in options:
            config[key] = value
        open(self.CONFIGFILE, 'w').write(json.dumps(config, indent=4))

    def getv(self, name):
        config = json.load(open(self.CONFIGFILE, 'r'))
        return (config[name])

    def toggle(self, arr):
        data = json.load(open(self.CONFIGFILE))
        for info in arr:
            if info in data["active"]:
                data["active"].remove(info)
            else:
                if info in data["available"]:
                    data["active"].append(info)
        open(self.CONFIGFILE, 'w').write(json.dumps(data, indent=4))

    def getf(self, name):
        info = bunzbar.infos.infos()
        if name == "infos.battery":
            return (str(info.battery()))
        elif name == "infos.clck":
            return (str(info.clck()))

        if self.exists("tsv_path"):
            match name:
                case "tsv.current.all":
                    return str(self.tsv.current(tsv_calendar.GET.ALL))
                case "tsv.current.name":
                    return str(self.tsv.current(tsv_calendar.GET.NAME))
                case "tsv.current.description":
                    return str(self.tsv.current(tsv_calendar.GET.DESCRIPTION))
                case "tsv.current.start_time":
                    return str(self.tsv.current(tsv_calendar.GET.START_TIME))
                case "tsv.current.start_timer":
                    return str(self.tsv.current(tsv_calendar.GET.START_TIMER))
                case "tsv.current.end_time":
                    return str(self.tsv.current(tsv_calendar.GET.END_TIME))
                case "tsv.current.end_timer":
                    return str(self.tsv.current(tsv_calendar.GET.END_TIMER))

                case "tsv.next.all":
                    return str(self.tsv.next(tsv_calendar.GET.ALL))
                case "tsv.next.name":
                    return str(self.tsv.next(tsv_calendar.GET.NAME))
                case "tsv.next.description":
                    return str(self.tsv.next(tsv_calendar.GET.DESCRIPTION))
                case "tsv.next.start_time":
                    return str(self.tsv.next(tsv_calendar.GET.START_TIME))
                case "tsv.next.start_timer":
                    return str(self.tsv.next(tsv_calendar.GET.START_TIMER))
                case "tsv.next.end_time":
                    return str(self.tsv.next(tsv_calendar.GET.END_TIME))
                case "tsv.next.end_timer":
                    return str(self.tsv.next(tsv_calendar.GET.END_TIMER))

        else:
            return ("<error>")
