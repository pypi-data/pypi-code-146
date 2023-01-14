import yaml
from casadi import heaviside


def cubicBrezierCurve(s, P, breakpt):
    t = (s - breakpt[0]) / (breakpt[1] - breakpt[0])
    return (
        (1 - t) ** 3 * P[0]
        + 3 * (1 - t) ** 2 * t * P[1]
        + 3 * (1 - t) * t ** 2 * P[2]
        + t ** 3 * P[3]
    )


class Track:
    def __init__(self):
        # self.track_name = "scurve.yaml"
        self.track_name = "ltom/scurve.yaml"
        # self.track_name = "ltom/circle_inv.yaml"
        with open(self.track_name, "r") as f:
            self.track = yaml.load(f, Loader=yaml.FullLoader)
        self.goal = self.track["goal"]

    def get_track(self, s):
        s_start = self.track["d"]["breakpoints"][0]
        s_stop = self.goal

        n_d = len(self.track["d"]["ctrlpoints"])
        n_theta = len(self.track["theta"]["ctrlpoints"])

        d = 0
        for i in range(n_d):
            d += cubicBrezierCurve(
                s,
                self.track["d"]["ctrlpoints"][i],
                self.track["d"]["breakpoints"][i : i + 2],
            ) * (
                heaviside(s - self.track["d"]["breakpoints"][i] + 1e-4)
                - heaviside(s - self.track["d"]["breakpoints"][i + 1])
            )

        theta = 0
        for i in range(n_theta):
            theta += cubicBrezierCurve(
                s,
                self.track["theta"]["ctrlpoints"][i],
                self.track["theta"]["breakpoints"][i : i + 2],
            ) * (
                heaviside(s - self.track["theta"]["breakpoints"][i] + 1e-4)
                - heaviside(s - self.track["theta"]["breakpoints"][i + 1])
            )

        curv = 0
        for i in range(n_theta):
            curv += cubicBrezierCurve(
                s,
                self.track["curv"]["ctrlpoints"][i],
                self.track["curv"]["breakpoints"][i : i + 2],
            ) * (
                heaviside(s - self.track["curv"]["breakpoints"][i] + 1e-4)
                - heaviside(s - self.track["curv"]["breakpoints"][i + 1])
            )

        return (d, theta, curv)
