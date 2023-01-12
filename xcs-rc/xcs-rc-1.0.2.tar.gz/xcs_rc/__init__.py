# -*- coding: utf-8 -*-
"""
Created on Mon Jul 1 10:13:54 2019
@author: Nugroho Fredivianus
"""

from os import path
from random import randrange, shuffle, random
from numpy import ndarray, int64, float64, array, max as npmax, sum as npsum
from pandas import Series, DataFrame

# TODO: polish feature selection

# initial values
cond_init = []
act_init = 0
pred_init = 50.0
prederr_init = 0.0
fit_init = 10.0


# Agent class
class Agent(object):

    def __init__(self, num_actions=2, pressure="HIGH", maxreward=100.0, proreward=50.0, maxpopsize=400, tcomb=50,
                 predtol=20.0, prederrtol=10.0, nout=0):

        # user-defined scenario
        self.num_actions = num_actions
        self.maxreward = maxreward
        self.proreward = proreward
        self.pressure = "LOW" if pressure.lower() == "low" else "MED" if pressure.lower() == "med" else "HIGH"
        self.nout = nout

        # xcs parameters
        self.maxpopsize = maxpopsize
        self.alpha = 0.1
        self.beta = 0.2
        self.gamma = 0.71
        self.delta = 0.1
        self.nu = 1.0
        self.epsilon_0 = 0.01
        self.theta_del = 20
        self.xmax = 0

        # rc parameters
        self.minexp = 1  # minimal experience to be combined
        self.tcomb = tcomb  # combining period T_comb
        self.predtol = predtol  # prediction tolerance, maximum difference allowed to be combined
        self.prederrtol = prederrtol  # prediction error tolerance, threshold for hasty combining detection

        # reinforcement cycle
        self.pop = ClassifierSet(owner=self, name="[Pop]")  # population
        self.mset = ClassifierSet(owner=self, name="[MatchSet]")  # match set
        self.pa = []  # prediction array
        self.aset = ClassifierSet(owner=self, name="[ActionSet]")  # action set
        self.state = None
        self.winner = 0
        self.reward = 0.0

        self.x = None
        self.y = None
        self.trials = None
        self.cl_counter = None
        self.binaries = None
        self.outliers = None
        self.pop_old = None
        self.filter = None

        self.reset()

    def reward_map(self, maxreward=None, projected=None):
        self.maxreward = maxreward if maxreward is not None else self.maxreward
        self.proreward = projected if maxreward is not None else self.proreward

    def build_matchset(self, state, covering=True):
        """
        Build a match set based on the input state.
        Perform covering as a default, in case any actions are not covered by available classifiers.
        :param state: XCS input state
        :param covering: determine whether covering is necessary
        :return: None
        """
        self.state = self.get_input(state)
        self.mset.cl = [cl for cl in self.pop.cl if cl.match(self.state)]
        covered = list(set([cl.act for cl in self.mset.cl]))

        if covering and len(covered) < self.num_actions:
            for i in range(self.num_actions):
                if i not in covered:
                    self.mset.add(Classifier(cond=floatify(self.state), act=i, pred=self.proreward, owner=self))

    def pick_action_winner(self, pick_method=1):
        """
        Pick an action as a winner based on classifiers existing in match set.
        :param pick_method: 0 = explore, 1 = exploit, 2 = explore_it (set priority to inexperienced classifiers)
        :return: winning action
        """
        pa = []
        exp = []
        inexp = []

        for act in range(self.num_actions):
            tset = [cl for cl in self.mset.cl if cl.act == act]
            pa.append(sum(cl.pred * cl.fit for cl in tset) / sum(cl.fit for cl in tset))
            exp.append(sum(cl.exp for cl in tset))
            inexp.append(len([cl for cl in tset if cl.exp < self.minexp]))

        pa_max = max(pa)
        self.pa = pa

        if max(inexp) > 0 and (pick_method == 0 or (pick_method == 2 and pa_max < self.proreward)):
            maxes = [i for i, v in enumerate(inexp) if v == max(inexp)]
            self.winner = maxes[randrange(len(maxes))]
        elif pick_method > 0:  # exploit or explore_it
            if pa.count(pa_max) > 1:
                maxes = [i for i, v in enumerate(pa) if v == pa_max]
                self.winner = maxes[randrange(len(maxes))]
            else:
                self.winner = pa.index(pa_max)
        elif pick_method == 0:  # explore
            if pa_max > 0.0:
                self.winner = choice(pa)[0]
            else:
                self.winner = randrange(len(pa))

        return self.winner

    def build_actionset(self, winner=None, reverse=False):
        """
        Build action set based on the winning action.
        :param winner: winning action
        :param reverse: if True, all actions enter action set except winner
        :return: None
        """
        if winner is None:
            winner = self.winner
        winner = [winner] if not reverse else [i for i in range(self.num_actions) if i != winner]
        self.aset.cl = [cl for cl in self.mset.cl if cl.act in winner]

        inexp = [cl for cl in self.aset.cl if cl.exp == 0]
        if len(inexp) > 0:
            size = self.pop.size() + len(inexp)
            if size > self.maxpopsize:
                self.del_oversize(size - self.maxpopsize)
            self.pop.add(inexp)

    def apply_reward(self, reward, add_trial=1):
        """
        Apply reward to classifiers in action set.
        :param reward: reward value in integer or float
        :param add_trial: default is 1, setting to 0 means do not consider as a trial (learning cycle)
        :return: list of removed classifiers due to prediction error exceeding tolerance
        """
        if self.aset.size() == 0:
            return []

        self.reward = reward
        cl_del = []
        cl_del_return = []

        for cl in self.aset.cl:
            prev = cl.prederr
            ori_cl = cl.copy()
            cl.exp += 1
            cl.update_prederr(reward)
            cl.update_pred(reward)

            if cl.prederr > self.prederrtol > prev and cl.prederr >= prev and cl.exp > 2 * self.minexp:
                cl_del.append(cl)

        if len(cl_del) > 0:
            self.pop.remove(cl_del)
            self.aset.remove(cl_del)
            cl_del_return.append(ori_cl)

        numsum = sum(cl.num for cl in self.aset.cl)
        for cl in self.aset.cl:
            cl.update_actsetsize(numsum)
        self.aset.update_fitset()
        self.aset.empty()

        self.trials += add_trial
        if self.tcomb > 0 and self.trials % self.tcomb == 0:
            start = 0 if self.pressure != "LOW" else (self.trials // self.tcomb - 1) % self.num_actions
            end = self.num_actions if self.pressure != "LOW" else start + 1

            for act in range(start, end):
                pop_check = sorted([cl.id for cl in self.pop.cl if
                                    cl.act == act and cl.exp >= self.minexp and cl.id not in self.outliers])
                if pop_check != self.pop_old[act]:
                    self.pop.combine_act(act)
                self.pop_old[act] = pop_check

        return cl_del_return

    def combine(self):
        """
        Combine population in the set.
        :return: None
        """
        self.pop.combine()

    def del_oversize(self, num_del):
        """
        Perform classifier deletions, e.g., when the size exceeds maximum allowed.
        :param num_del: number of classifiers to be deleted
        :return: None
        """
        inexps = [cl for cl in self.pop.cl if cl.exp == 0]
        if len(inexps) > 0:
            self.pop.remove(inexps)

        if num_del > len(inexps):
            store = [cl for cl in self.mset.cl if cl in self.pop.cl]
            dummy = [cl for cl in self.pop.cl if cl not in store]

            meanfit = sum(cl.fit for cl in dummy) / sum(cl.num for cl in dummy)
            points = [cl.get_delprop(meanfit) for cl in dummy]
            cl_del = [dummy[x] for x in choice(points, num_del - len(inexps))]
            if len(cl_del) > 0:
                for cl in cl_del:
                    if cl not in dummy:
                        continue
                    dummy.remove(cl)
                    del cl

            self.pop.cl = dummy + store

    def next_action(self, state, pick_method=1, force=-1, build_aset=True):
        """
        Pick an action after performing an RL cycle
        :param state: XCS input state
        :param pick_method: 0 = explore, 1 = exploit, 2 = explore_it (set priority to inexperienced classifiers)
        :param force: force an action to be picked
        :param build_aset: build an action set, set False if no learning should be performed
        :return: winning action
        """
        self.build_matchset(state)
        self.pick_action_winner(pick_method) if force < 0 else force
        if build_aset:
            self.build_actionset(self.winner)
        return self.winner

    def get_input(self, vals):
        """
        Modify input if necessary
        :param vals: various types of input value
        :return: input in list, if applicable
        """
        if isinstance(vals, str):
            return self.filter_cond(vals)

        self.binaries = False

        if isinstance(vals, list):
            return vals

        if isinstance(vals, (Series, DataFrame)):
            return vals.values.tolist()

        if isinstance(vals, ndarray):
            return vals.tolist()

        return None

    def load(self, fname, empty_first=True):
        """
        Load population of classifiers from a file.
        :param fname: file name
        :param empty_first: empty current population before loading
        :return: None
        """
        if isinstance(fname, str):
            if path.isfile(fname):
                with open(fname) as f:
                    cls = f.readlines()
            else:
                print("File " + fname + " does not exist. Load failed.")
                return False
        else:
            print("Not a filename. Load failed.")
            return False

        last_id = [i for i, s in enumerate(cls) if "id;" in s]
        if len(last_id) == 0:
            last_id.append(0)

        if empty_first:
            self.pop.empty()

        num = 0
        for cl in cls[last_id[-1]:]:
            if cl[0].isdigit():
                z = cl.count(";")
                if self.binaries and z > 8:
                    self.binaries = False
                val = cl.split(";")
                val_cond = ""
                for i in range(1, z - 6):
                    val_cond += val[i] + ","
                self.pop.add(Classifier(cond=floatify(val_cond[:-1]), act=int(val[z - 6]), pred=float(val[z - 5]),
                                        fit=float(val[z - 4]), prederr=float(val[z - 3]), num=int(val[z - 2]),
                                        exp=int(val[z - 1]), actsetsize=int(val[z]), owner=self))
                num += 1

        print(f"Loaded to {self.pop.name}: {num} classifiers.")

    def save(self, fname, title="", save_mode='w', feedback=False):
        """
        Save current population to a file.
        :param fname: file name
        :param title: title above the classifers data
        :param save_mode: w for write, a for append
        :param feedback: if True, print save status
        :return: None
        """
        self.pop.save(fname, title, save_mode, feedback=feedback)

    def filter_cond(self, cond):
        if len(self.filter) == 0:
            return cond

        for i in reversed(self.filter):
            cond = cond[:i] + cond[:-i - 1]

        return cond

    def check_feature(self, set_filter=False):
        if not self.binaries:
            return False

        conds = [cl.printable_cond() for cl in self.pop.cl if cl.exp > 0]
        lens = [len(cond) for cond in conds]
        if max(lens) != min(lens):
            return False

        irr = []
        for i in range(1, max(lens) - 1):
            check = [cond[i] for cond in conds]
            hashes = check.count('#')
            if hashes == len(conds):
                irr.append(i - 1)

        if set_filter and len(irr) > 0:
            if len(self.filter) == 0:
                self.filter = irr

            for cl in self.pop.cl:
                for i in reversed(irr):
                    cl.cond = cl.cond[:i] + cl.cond[:-i - 1]

        return irr

    def reset(self):
        """
        Reset learning agent.
        :return: None
        """
        self.pop.empty()
        self.mset.empty()
        self.pa = []
        self.aset.empty()

        self.x = 0
        self.y = 0

        self.trials = 0
        self.cl_counter = 1
        self.binaries = True
        self.outliers = [int(self.nout > 0) - 1]  # 0 for outlier detection, minus for no
        self.pop_old = [[-1] for _ in range(self.num_actions)]
        self.filter = []

    def train(self, X_train, y_train, show_progress=True):
        """
        Train XCS using input data
        :param X_train: state data
        :param y_train: action data
        :param show_progress: if True, print progress to console
        :return: size of population
        """
        self.nout = 100
        self.outliers = [0]
        X_train = self.get_input(X_train)
        y_train = self.get_input(y_train)
        self.num_actions = int(max(y_train)) + 1

        for i, (X, y) in enumerate(zip(X_train, y_train)):
            self.build_matchset(X)
            for j in range(2):
                self.build_actionset(y, j > 0)  # reversal factor: False = build y, True = build others
                reward = (1 - j) * self.maxreward
                self.apply_reward(reward, j)

            # simple visualization
            if show_progress:
                print('.', end='')
                if i % 100 == 99:
                    print(f" [{i + 1}/{self.pop.size()} cl.]")
                    # self.pop.print(per_action=True)

        self.pop.sort()
        return self.pop.cl

    def predict(self, data, norm=True, show_progress=False):
        data = self.get_input(data)
        if isinstance(data, list):
            if not isinstance(data[0], list):
                data = [data]
        else:
            print("Input for predict not supported.")
            return []

        outputs = []
        probs = []
        for i, X in enumerate(data):
            output = self.next_action(X, 1, build_aset=False)
            outputs.append(output)
            prob = softmax(self.pa) if norm else self.pa
            probs.append([round(p, 3) for p in prob])

            # simple visualization
            if show_progress:
                print('.', end='')
                if i % 100 == 99:
                    print(f" [{i + 1}]")

        if len(data) == 1:
            outputs = outputs[0]
            probs = probs[0]
        return outputs, probs

    def test(self, X_test, y_test, show_progress=True, keep_learning=False):
        X_test = self.get_input(X_test)
        y_test = self.get_input(y_test)
        cm = [[0 for _ in range(self.num_actions)] for __ in range(self.num_actions)]

        if not isinstance(X_test[0], list):
            X_test = [X_test]

        for i, (X, y) in enumerate(zip(X_test, y_test)):
            answer = self.next_action(X, 1, build_aset=keep_learning)
            cm[y][answer] += 1

            if keep_learning:
                self.apply_reward(int(answer == y) * self.maxreward)

            # simple visualization
            if show_progress:
                print('.', end='')
                if i % 100 == 99:
                    print(f" [{i + 1}]")

        return cm


# ClassifierSet class

class ClassifierSet(object):
    def __init__(self, owner=None, name="Set", cls=None):
        if cls is None:
            cls = []
        self.owner = owner
        self.name = name
        self.cl = cls

    def size(self):
        return len(self.cl)

    def add(self, cls):
        for cl in check_cls(cls):
            self.cl.append(cl)

    def remove(self, cls):
        cl_del = check_cls(cls)
        self.cl = [cl for cl in self.cl if cl not in cl_del]

    def empty(self):
        self.cl = []

    def copy(self):
        return ClassifierSet(name="[Temp]", owner=self.owner, cls=self.cl)

    def exist(self, cl_t):
        return [cl for cl in self.cl if cl.cond == cl_t.cond and cl.act == cl_t.act and cl.pred == cl_t.pred]

    def sort(self, keys=None):  # 0 exp, 1 pred, 2 act, 3 num
        if not keys:
            keys = [0]
        if isinstance(keys, int) or isinstance(keys, str):
            keys = [keys]
        for opt in reversed(keys):
            if opt in [1, "pred"]:
                for cls in self.cl:
                    cls.pred = round(cls.pred, 3)
                self.cl.sort(key=lambda cl: cl.pred, reverse=True)
            elif opt in [2, "act"]:
                self.cl.sort(key=lambda cl: cl.act, reverse=False)
            elif opt in [3, "num"]:
                self.cl.sort(key=lambda cl: cl.num, reverse=True)
            else:
                self.cl.sort(key=lambda cl: cl.exp, reverse=True)

    def update_fitset(self):
        acc = [cl.get_accuracy() for cl in self.cl]
        accsum = sum(ac * cl.num for ac, cl in zip(acc, self.cl))

        for idx, cl in enumerate(self.cl):
            cl.update_fitness(accsum, acc[idx])

    def combine_act(self, act):
        minexp = self.owner.minexp
        predtol = self.owner.predtol
        beta = self.owner.beta

        cset = ClassifierSet(name=f"[C:{act}]")
        cset.cl = [cl for cl in self.cl if cl.act == act]
        pressing = True
        while pressing:
            pressing = False
            cset.sort()
            parent1 = [cl for cl in cset.cl if cl.exp >= minexp]
            for p1 in parent1:
                parent2 = [cl for cl in parent1 if cl != p1 and abs(p1.pred - cl.pred) <= predtol]
                for p2 in parent2:
                    cl_star = Classifier(cond=combine_cond(p1.cond, p2.cond), act=act, owner=self.owner)
                    cl_star.pred = (p1.pred * p1.num + p2.pred * p2.num) / (p1.num + p2.num)

                    disproval = []
                    if (p1.cond != p2.cond or p1.act != p2.act or abs(p1.pred - p2.pred > predtol)) and \
                            not p1.subsumable_to(p2) and not p2.subsumable_to(p1):
                        disproval = [cl for cl in cset.cl if cl.exp > 0 and cl.overlap(cl_star) and not within_range(
                            cl_star.pred, cl.pred, predtol) and cl.id not in self.owner.outliers]

                    if self.owner.outliers[0] == 0 and len(disproval) > 0:
                        for cl in disproval:
                            pa = min(p1.id, p2.id)
                            pb = max(p1.id, p2.id)
                            if [pa, pb] not in cl.disproves:
                                cl.disproves.append([pa, pb])
                            if len(cl.disproves) / cl.exp >= cl.owner.nout:
                                self.owner.outliers.append(cl.id)
                                cl.disproves = []
                    elif len(disproval) == 0:
                        subsumptions = [cl for cl in cset.cl if cl.subsumable_to(cl_star) and (
                                abs(cl.pred - cl_star.pred) <= predtol or cl.exp == 0)]

                        cl_star.exp = sum(cl.exp for cl in subsumptions)
                        cl_star.num = min(self.owner.maxpopsize, sum(cl.num for cl in subsumptions if cl.exp > 0))
                        cl_star.pred = sum(cl.pred * cl.num for cl in subsumptions if cl.exp > 0) / cl_star.num
                        cl_star.calculate_prederr()
                        cl_star.fit = (fit_init - 1) * pow(1 - beta, cl_star.exp) + 1

                        cset.add(cl_star)
                        self.add(cl_star)

                        cset.remove(subsumptions)
                        self.remove(subsumptions)

                        if self.owner.pressure == "HIGH":
                            pressing = True
                            parent1.clear()
                            parent2.clear()

                        for cl in subsumptions:
                            if self.owner.pressure != "HIGH":
                                if cl in parent1:
                                    parent1.remove(cl)
                            del cl

                        break

    def combine(self):
        num = max([cl.act for cl in self.cl]) + 1
        for act in range(num):
            self.combine_act(act)

    def get_header(self):
        head = "id;cond;"
        if not self.owner.binaries:
            for i in range(len(self.cl[0].cond) - 1):
                head += ";"
        head += "act;pred;fit;prederr;num;exp;actsetsize"

        return head

    def print(self, title="", header=True, per_action=False):
        if per_action:
            counts = []
            for i in range(self.owner.num_actions):
                counts.append(sum(cl.act == i for cl in self.cl))
            print(counts, " - Sum:", sum(counts))
            return

        if title != "":
            print(".\n" + title)

        if len(self.cl) > 0:
            if header:
                print(self.get_header())
            i = 0
            for cl in self.cl:
                i += 1
                print(f"{i};{cl.printable()}")
        else:
            if title != "":
                print("[empty]")

    def save(self, fname, title="", save_mode='w', sort=None, feedback=False):
        if save_mode != 'a':
            save_mode = 'w'
        try:
            with open(fname, save_mode) as f:
                tset = self.copy()
                if sort is not None:
                    if not isinstance(sort, list):
                        sort = [sort]
                    tset.sort(*sort)

                if save_mode == 'a':
                    f.write(".\n")  # vertical separator
                if title != "":
                    f.write(title + "\n")
                f.write(tset.get_header() + "\n")
                for i, cl in enumerate(tset.cl):
                    f.write(f"{i + 1};{cl.printable()}\n")
            if feedback:
                print(f"{self.name} stored to {fname}: {tset.size()} classifiers.")
        except Exception as e:
            print("Failed to save population:", e)


# Classifier class

class Classifier(object):

    def __init__(self, cond=None, act=act_init, pred=pred_init, fit=fit_init, prederr=prederr_init, num=1, exp=0,
                 actsetsize=1, owner=None):
        if cond is None:
            cond = cond_init

        number = (int, float, complex)
        new_cond = []
        if cond != cond_init:
            if isinstance(cond, str):
                if not is_binarystr(cond):
                    return
                for c in cond:
                    el = [0.000, 0.000] if c == '0' else [1.000, 1.000]
                    new_cond.append(el)

            elif isinstance(cond, list):
                for c in cond:
                    el = []
                    if isinstance(c, list):
                        if len(c) != 2:
                            print("Cl cond: number of elements error.")
                            return

                        for c2 in c:
                            if not isinstance(c2, number):
                                print("Cl cond: value error.")
                                return

                        el = [min(c), max(c)]

                    elif isinstance(c, number):
                        el = [c, c]

                    new_cond.append(el)

        else:
            new_cond = cond

        if not isinstance(act, int):
            print("Cl act: not an integer.")
            return

        self.cond = new_cond
        self.act = act

        self.pred = pred
        self.prederr = prederr
        self.fit = fit
        self.num = num
        self.exp = exp
        self.actsetsize = actsetsize
        self.owner = owner

        self.disproves = []
        self.id = owner.cl_counter
        owner.cl_counter += 1

    def match(self, cl):
        if isinstance(cl, Classifier):
            if cl.act != self.act:
                return False
            state = cl.cond
        else:
            state = cl

        if len(state) != len(self.cond):
            return False
        if isinstance(state, str):
            if not is_binarystr(state):
                return False
            state = binarytolist(state)

        for sc, st in zip(self.cond, state):
            if st < sc[0] or st > sc[1]:
                return False

        return True

    def copy(self):
        cl = Classifier(cond=self.cond, act=self.act, pred=self.pred, prederr=self.prederr, fit=self.fit, num=self.num,
                        exp=self.exp, actsetsize=self.actsetsize, owner=self.owner)
        return cl

    def subsumable_to(self, cl):
        if not isinstance(cl, Classifier):
            return False
        if cl.act != self.act:
            return False
        if len(cl.cond) != len(self.cond):
            return False

        for sc, cc in zip(self.cond, cl.cond):
            if sc[0] < cc[0] or sc[1] > cc[1]:
                return False

        return True

    def can_subsume(self, cl):
        if not isinstance(cl, Classifier):
            return False
        if cl.act != self.act:
            return False
        if len(cl.cond) != len(self.cond):
            return False

        for sc, cc in zip(self.cond, cl.cond):
            if sc[0] > cc[0] or sc[1] < cc[1]:
                return False

        return True

    def resemblance(self, cl):
        if isinstance(cl, Classifier):
            val = cl.cond
        elif isinstance(cl, (str, list)):
            val = floatify(cl)
        else:
            return 0.0

        if len(val) != len(self.cond):
            return 0.0

        res = 0.0
        for sc, cc in zip(self.cond, val):
            if cc[0] == sc[0] or cc[1] == sc[1]:
                add = 0
                if cc[0] == sc[0]:
                    add += 0.5
                if cc[1] == sc[1]:
                    add += 0.5
                if add < 1.0:
                    add += 0.4
                res += add
            elif (cc[0] > sc[0] and cc[1] < sc[1]) or (cc[0] < sc[0] and cc[1] > sc[1]):
                res += 0.8
            elif cc[1] > sc[0] and cc[0] < sc[1]:
                res += 0.7
            else:
                res += 0.4

        return res / len(self.cond)

    def overlap(self, cl):
        if not isinstance(cl, Classifier):
            return False
        if len(self.cond) != len(cl.cond):
            return False

        for sc, cc in zip(self.cond, cl.cond):
            if cc[0] > sc[1] or sc[0] > cc[1]:
                return False
        return True

    def get_delprop(self, meanfit):
        if self.fit / self.num >= self.owner.delta * meanfit or self.exp < self.owner.theta_del:
            return self.actsetsize * self.num
        return self.actsetsize * self.num * meanfit / (self.fit / self.num)

    def update_pred(self, P):
        if self.exp < 1.0 / self.owner.beta:
            self.pred = (self.pred * (float(self.exp) - 1.0) + P) / float(self.exp)
        else:
            self.pred += self.owner.beta * (P - self.pred)

    def update_prederr(self, P):
        if self.exp < 1.0 / self.owner.beta:
            self.prederr = (self.prederr * float(self.exp - 1.0) + abs(P - self.pred)) / self.exp
        else:
            self.prederr += self.owner.beta * (abs(P - self.pred) - self.prederr)

    def get_accuracy(self):
        if self.prederr <= self.owner.epsilon_0:
            return 1.0
        else:
            return self.owner.alpha * pow(self.prederr / self.owner.epsilon_0, -self.owner.nu)

    def update_fitness(self, accsum, accuracy):
        self.fit += self.owner.beta * ((accuracy * self.num) / accsum - self.fit)

    def update_actsetsize(self, numsum):
        if self.exp < 1. / self.owner.beta:
            self.actsetsize = int((self.actsetsize * (self.exp - 1) + numsum) / self.exp)
        else:
            self.actsetsize += int(self.owner.beta * (numsum - self.actsetsize))

    def calculate_prederr(self):
        beta = self.owner.beta
        exp_lim = 1 / beta
        if self.exp <= int(exp_lim):
            self.prederr = abs(self.pred - pred_init) / self.exp
        else:
            self.prederr = (abs(self.pred - pred_init) / exp_lim) * pow(1 - beta, self.exp - int(exp_lim))

    def printable_cond(self):
        str_cond = ""
        if self.owner.binaries:
            str_cond = '"'
            for sc in self.cond:
                str_cond += "#" if sc[0] != sc[1] else "0" if sc[0] == 0.0 else "1"
            str_cond += '"'
        else:
            for c in self.cond:
                if isinstance(c, list):
                    if isinstance(c[0], int):
                        c0 = f"[{c[0]}"
                        c1 = f", {c[1]}"
                    elif c[0].is_integer():
                        c0 = f"[{int(c[0])}"
                        c1 = f", {int(c[1])}"
                    else:
                        c0 = f"[{c[0]:.3f}"
                        c1 = f", {c[1]:.3f}"
                    str_cond += c0
                    if c[0] != c[1]:
                        str_cond += c1
                    str_cond += "];"
                else:
                    str_cond += f"{c:.3f}"
            str_cond = str_cond[:-1]

        return str_cond

    def printable(self):
        return f"{self.printable_cond()};{self.act};{self.pred:.3f};{self.fit:.3f};{self.prederr:.3f};{self.num};" + \
               f"{self.exp};{self.actsetsize}"

    def print(self, title=False):
        if title:
            print("Cond:Act->Pred | Fit, PredErr, Num, Exp, ActSetSize")
        print(f"{self.printable_cond()}:{self.act}->{self.pred:.3f} | {self.fit:.3f}, {self.prederr:.3f}, " +
              f"{self.num}, {self.exp}, {self.actsetsize}")


# Markov Environment class

class MarkovEnv(object):

    def __init__(self, env='maze4', markov_map=None):
        if markov_map is None:
            markov_map = []
        self.agents = []
        self.map = markov_map

        self.wall = ('O', 'Q')
        self.food = ('F', 'G')
        self.empty = ('*', '.')

        if path.isfile(env):
            with open(env) as f:
                lines = f.readlines()
                for line in lines:
                    self.map.append(line.rstrip('\n'))
        else:
            env = 'maze4'

        if env.lower() == 'maze4':  # average: 3.5 steps
            self.map.append("OOOOOOOO")  # _ _ _ _ _ _ _ _
            self.map.append("O**O**FO")  # _ 5 4 _ 2 1 F _
            self.map.append("OO**O**O")  # _ _ 4 3 _ 1 1 _
            self.map.append("OO*O**OO")  # _ _ 4 _ 2 2 _ _
            self.map.append("O******O")  # _ 5 4 3 3 3 3 _
            self.map.append("OO*O***O")  # _ _ 4 _ 4 4 4 _
            self.map.append("O****O*O")  # _ 5 5 5 5 _ 5 _
            self.map.append("OOOOOOOO")  # _ _ _ _ _ _ _ _

        print("Env initialized:", env)
        for m in self.map:
            print(m)

    def add_agents(self, num, tcomb, xmax, num_actions=8, pressure="HIGH", maxreward=1000.0, proreward=50.0,
                   maxpopsize=400, predtol=50.0, prederrtol=5.0):
        for i in range(num):
            agent = Agent(num_actions=num_actions, pressure=pressure, maxreward=maxreward, maxpopsize=maxpopsize,
                          tcomb=tcomb, predtol=predtol, prederrtol=prederrtol)
            agent.beta = 0.75
            agent.gamma = 0.71
            agent.reward_map(projected=proreward)
            agent.xmax = xmax
            agent.x, agent.y = self.reset_pos()
            self.agents.append(agent)

    def reset_pos(self):
        max_x = len(self.map[0])
        max_y = len(self.map)

        y = -1
        while y < 0 or self.map[y].count('*') + self.map[y].count('.') == 0:
            y = randrange(0, max_y)

        x = -1
        while x < 0 or self.map[y][x] not in self.empty:
            x = randrange(0, max_x)

        return x, y

    def get_state(self, x, y):
        val = ""
        for i in range(8):
            val += decode(self.map[y + add_y(i)][x + add_x(i)])
        return val

    def move(self, x, y, move):
        xx = x + add_x(move)
        yy = y + add_y(move)
        zz = self.map[yy][xx]
        if zz == 'O' or zz == 'Q':
            return x, y, self.map[y][x]
        return xx, yy, zz

    def one_episode(self, pick_method=1):
        agents_steps = []
        for agent in self.agents:
            agent.x, agent.y = self.reset_pos()
            steps = agent.xmax

            for i in range(steps):
                agent.build_matchset(self.get_state(agent.x, agent.y))
                agent.pick_action_winner(pick_method)

                if i > 0:
                    agent.apply_reward(agent.gamma * max(agent.pa))

                agent.build_actionset()
                agent.x, agent.y, agent_now = self.move(agent.x, agent.y, agent.winner)

                if agent_now in self.food:
                    agent.apply_reward(agent.maxreward)
                    steps = i + 1
                    break

            agents_steps.append(steps)

        return agents_steps


def decode(char):
    if not isinstance(char, str):
        return ""
    elif len(char) != 1:
        return ""
    elif char == '*' or char == '.':
        return "000"
    elif char == 'O':
        return "010"
    elif char == 'Q':
        return "011"
    elif char == 'F':
        return "110"
    elif char == 'G':
        return "111"

    return ""


def add_x(move):
    x = 0 if move % 4 == 0 else 1 if move < 4 else -1
    return x


def add_y(move):
    y = -1 if move % 7 < 2 else 0 if move % 4 == 2 else 1
    return y


def is_binarystr(str_cond):
    for s in str_cond:
        if s not in "01":
            print("Cl cond: binary error.")
            return False
    return True


def binarytolist(val):
    cond = []
    for v in val:
        c = 0.000 if v == '0' else 1.000
        cond.append(c)
    return cond


def floatify(state):
    number = (int, int64, float, float64, complex)
    cond = []
    if isinstance(state, str):
        if state[0] == '[':
            states = state.split('],[')
            for s in states:
                s = s.replace('[', '').replace(']', '')
                a = [0, 0]
                if s.count(',') == 1:
                    a = s.split(',')
                else:
                    a[0] = s
                    a[1] = s
                cond.append([float(a[0]), float(a[1])])
        else:
            for s in state.replace('"', ''):
                if s not in "01#":
                    print("Cl cond: not a binary string.")
                    return False
                if s == "0":
                    cond.append([0.00, 0.00])
                elif s == "1":
                    cond.append([1.00, 1.00])
                else:
                    cond.append([0.00, 1.00])

    elif isinstance(state, list):
        for s in state:
            if isinstance(s, number):
                s = int(s) if isinstance(s, int64) else float(s) if isinstance(s, float64) else s
                cond.append([s, s])
            elif isinstance(s, list):
                cond.append(s)

    return cond


def within_range(val1, val2, tol):
    return val2 + tol >= val1 and val2 <= val1 + tol


def combine_cond(cond1, cond2):
    dummy = [[-1.0, -1.0] for _ in range(len(cond1))]
    for i in range(len(cond1)):
        dummy[i] = [min(cond1[i][0], cond2[i][0]), max(cond1[i][1], cond2[i][1])]
    return dummy


def choice(ar, times=1):
    arr = ar.copy()

    if times > len(arr):
        return []
    elif times == len(arr):
        picks = list(range(times))
        shuffle(picks)
        return picks

    sums = 0.0
    sum_array = []
    for a in arr:
        sums += a
        sum_array.append(sums)

    picks = []
    for i in range(times):
        val = random() * sum(arr)
        chosen = next(k for k, v in enumerate(sum_array) if v >= val)
        arr[chosen] = 0
        picks.append(chosen)

    return picks


def check_cls(cls):
    if isinstance(cls, list):
        if len(cls) == 0:
            return []
        for cl in cls:
            if not isinstance(cl, Classifier):
                return []
        return cls
    elif isinstance(cls, Classifier):
        return [cls]
    else:
        return []


def softmax(x):
    x = array(x, dtype='float64')
    e_x = exp(x - npmax(x))
    prob = (e_x / npsum(e_x)).tolist()
    return prob
