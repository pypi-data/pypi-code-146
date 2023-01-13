from tqdm import tqdm
from colorama import Style, Fore
from time import sleep
import numpy as np
import time
from collections import deque
from sympy import simplify
from sympy import sympify


class Data(object):
    def __init__(self, keys, values):
        for (key, value) in zip(keys, values):
            self.__dict__[key] = value
        self.id = 0
        self.winner = ''
        self.usedCategorical = []
        self.predict = None


class Attribute:
    def __init__(self):
        self.name = None
        self.type = None
        self.new = False
        self.use = False
        self.unit = None


class Leaf:
    def __init__(self):
        self.rule = ''
        self.dataset = []
        self.terminateBuilding = False
        self.branch = 0
        self.parent = None
        self.id = None
        self.branchAttribute = None
        self.classes = None
        self.decision = []
        self.predict = None


class Chromosome:
    def __init__(self, attribute, data):
        self.string = []
        self.expression = ''
        self.attribute = attribute
        self.data = data

    def combine(self):
        s = deque()
        operation = ['+', '*', '-', '/', 'attr', 'BLANK']
        operation2 = ['+', '*', '-', '/']
        operation3 = ['attr']
        operation4 = ['BLANK']
        possible = None
        for e in self.string:
            if e not in operation:
                s.append(e)
            elif e in operation3:
                n1 = s.pop()
                s.append('obj.' + n1.name)
            elif e == operation4:
                pass
            elif e in operation2:
                n1 = s.pop()
                n2 = s.pop()

                if (type(n1) == Attribute) and (type(n2) == Attribute):
                    s.append('(obj.' + n2.name + e + 'obj.' + n1.name + ')')
                elif (type(n1) != Attribute) and (type(n2) == Attribute):
                    s.append('(' + n2.name + e + 'obj.' + n1 + ')')
                elif (type(n1) == Attribute) and (type(n2) != Attribute):
                    s.append('(obj.' + n2 + e + n1.name + ')')
                else:
                    s.append('(' + n2 + e + n1 + ')')

                if check_proper_calc(n1, e, n2, self.attribute):
                    possible = True
                else:
                    possible = False
                    return False
        if possible:
            try:
                list(map(lambda obj: eval(s[0]), self.data))
                self.expression = s[0]
                return True
            except:
                return False


class Population:
    def __init__(self):
        self.population = []


class DT:
    def __init__(self):
        self.leaf = list
        self.root = None
        self.test_data = None
        self.rule_decision = list
        self.accuracy = 0
        self.chromosome = None

    def fit(self):
        self.root.dataset = self.test_data
        decisions = sorted(list(set(map(lambda x: x.Decision, self.test_data))))
        num_of_decisions = []
        for i in decisions:
            num_of_decisions.append(list(map(lambda x: x.Decision, self.root.dataset)).count(i))
        self.root.decision = num_of_decisions
        # for _leaf in tqdm(self.leaf, desc=Fore.GREEN + Style.BRIGHT + "Fitting : ", mininterval=0.1, ncols=150):
        for _leaf in self.leaf:
            _leaf.dataset = []
            # for i in list(filter(lambda obj:eval(_leaf.rule), _leaf.parent.dataset)):
            #
            #     i.predict = _leaf.predict
            #     _leaf.dataset.append(i)

            for obj in _leaf.parent.dataset:
                if eval(_leaf.rule):
                    obj.predict = _leaf.predict
                    _leaf.dataset.append(obj)

            num_of_decisions = []
            for i in decisions:
                num_of_decisions.append(list(map(lambda x: x.Decision, _leaf.dataset)).count(i))
            _leaf.decision = num_of_decisions
            sleep(0.1)


def attribute_set(attribute, data):
    # attribute 의 데이터 타입(범주형 or 연속형)을 판단
    if len(set(map(lambda x: x.__getattribute__(attribute.name), data))) <= 8:
        attribute.type = 'Categorical'
        for _data in data:
            setattr(_data, attribute.name, str(_data.__getattribute__(attribute.name)))
    else:
        attribute.type = 'Continuous'


def get_PASTEUR_unit(attr_name):
    if attr_name == "MIXA_PASTEUR_STATE":
        return None
    elif attr_name == "MIXB_PASTEUR_STATE":
        return None
    elif attr_name == "MIXA_PASTEUR_TEMP":
        return 'C'
    elif attr_name == "MIXB_PASTEUR_TEMP":
        return 'C'

def get_Molding_unit(attr_name):
    if attr_name == "Injection_Time":
        return 's'
    elif attr_name == "Filling_Time":
        return 's'
    elif attr_name == "Plasticizing_Time":
        return 's'
    elif attr_name == "Cycle_Time":
        return 's'
    elif attr_name == "Clamp_Close_Time":
        return 'mm'
    elif attr_name == "Cushion_Position":
        return 'mm'
    elif attr_name == "Switch_Over_Position":
        return 'mm'
    elif attr_name == "Plasticizing_Position":
        return 'mm'
    elif attr_name == "Clamp_Open_Position":
        return 'mm'
    elif attr_name == "Max_Injection_Speed":
        return 'mm/s'
    elif attr_name == "Max_Screw_RPM":
        return 'mm/s'
    elif attr_name == "Average_Screw_RPM":
        return 'mm/s'
    elif attr_name == "Max_Injection_Pressure":
        return 'MPa'
    elif attr_name == "Max_Switch_Over_Pressure":
        return 'MPa'
    elif attr_name == "Max_Back_Pressure":
        return 'MPa'
    elif attr_name == "Average_Back_Pressure":
        return 'MPa'
    elif attr_name == "Barrel_Temperature_1":
        return 'C'
    elif attr_name == "Barrel_Temperature_2":
        return 'C'
    elif attr_name == "Barrel_Temperature_3":
        return 'C'
    elif attr_name == "Barrel_Temperature_4":
        return 'C'
    elif attr_name == "Barrel_Temperature_5":
        return 'C'
    elif attr_name == "Barrel_Temperature_6":
        return 'C'
    elif attr_name == "Barrel_Temperature_7":
        return 'C'
    elif attr_name == "Hopper_Temperature":
        return 'C'
    elif attr_name == "Mold_Temperature_3":
        return 'C'
    elif attr_name == "Mold_Temperature_4":
        return 'C'

def get_CNC_unit(attr_name):
    if attr_name == "X_ActualPosition":
        return 'mm'
    elif attr_name == "X_ActualVelocity":
        return 'mm/s'
    elif attr_name == "X_ActualAcceleration":
        return 'mm/s/s'
    elif attr_name == "X_SetPosition":
        return 'mm'
    elif attr_name == "X_SetVelocity":
        return 'mm/s'
    elif attr_name == "X_SetAcceleration":
        return 'mm/s/s'
    elif attr_name == "X_CurrentFeedback":
        return 'A'
    elif attr_name == "X_DCBusVoltage":
        return 'V'
    elif attr_name == "X_OutputCurrent":
        return 'A'
    elif attr_name == "X_OutputVoltage":
        return 'V'
    elif attr_name == "X_OutputPower":
        return 'kw'


    elif attr_name == "Y_ActualPosition":
        return 'mm'
    elif attr_name == "Y_ActualVelocity":
        return 'mm/s'
    elif attr_name == "Y_ActualAcceleration":
        return 'mm/s/s'
    elif attr_name == "Y_SetPosition":
        return 'mm'
    elif attr_name == "Y_SetVelocity":
        return 'mm/s'
    elif attr_name == "Y_SetAcceleration":
        return 'mm/s/s'
    elif attr_name == "Y_CurrentFeedback":
        return 'A'
    elif attr_name == "Y_DCBusVoltage":
        return 'V'
    elif attr_name == "Y_OutputCurrent":
        return 'A'
    elif attr_name == "Y_OutputVoltage":
        return 'V'
    elif attr_name == "Y_OutputPower":
        return 'kw'

    elif attr_name == "Z_ActualPosition":
        return 'mm'
    elif attr_name == "Z_ActualVelocity":
        return 'mm/s'
    elif attr_name == "Z_ActualAcceleration":
        return 'mm/s/s'
    elif attr_name == "Z_SetPosition":
        return 'mm'
    elif attr_name == "Z_SetVelocity":
        return 'mm/s'
    elif attr_name == "Z_SetAcceleration":
        return 'mm/s/s'
    elif attr_name == "Z_CurrentFeedback":
        return 'A'
    elif attr_name == "Z_DCBusVoltage":
        return 'V'
    elif attr_name == "Z_OutputCurrent":
        return 'A'
    elif attr_name == "Z_OutputVoltage":
        return 'V'

    elif attr_name == "S_ActualPosition":
        return 'mm'
    elif attr_name == "S_ActualVelocity":
        return 'mm/s'
    elif attr_name == "S_ActualAcceleration":
        return 'mm/s/s'
    elif attr_name == "S_SetPosition":
        return 'mm'
    elif attr_name == "S_SetVelocity":
        return 'mm/s'
    elif attr_name == "S_SetAcceleration":
        return 'mm/s/s'
    elif attr_name == "S_CurrentFeedback":
        return 'A'
    elif attr_name == "S_DCBusVoltage":
        return 'V'
    elif attr_name == "S_OutputCurrent":
        return 'A'
    elif attr_name == "S_OutputVoltage":
        return 'V'
    elif attr_name == "S_OutputPower":
        return 'kw'
    elif attr_name == "S_SystemInertia":
        return 'kg*m*m'

    elif attr_name == "M_CURRENT_PROGRAM_NUMBER":
        return 'C'
    elif attr_name == "M_sequence_number":
        return 'C'
    elif attr_name == "M_CURRENT_FEEDRATE":
        return 'C'
    elif attr_name == "Machining_Process":
        return 'C'


def check_proper_calc(attr1, oper, attr2, attribute):
    def check_unit(attr):
        if type(attr) == Attribute:
            return attr.unit
        elif (attr.count('obj.') == 1) or (attr.count('obj.') == 0):
            attr = attr.replace('(', '').replace(')', '').replace('obj.', '')
            try:
                unit = list(filter(lambda x: x.name == attr, attribute))[0].unit
            except:
                unit = ' '
                print()
            return unit
        else:
            attr = attr.replace('(', '').replace(')', '').replace('obj.', '')
            if '+' in attr:
                attr = attr.split('+')[0]
                unit = list(filter(lambda x: x.name == attr, attribute))[0].unit
                return unit
            elif '-' in attr:
                attr = attr.split('-')[0]
                unit = list(filter(lambda x: x.name == attr, attribute))[0].unit
                return unit
            elif '*' in attr:
                attr = attr.split('*')
                attr1, attr2 = attr[0], attr[1]
                unit1 = check_unit(attr1)
                unit2 = check_unit(attr2)
                unit = str(sympify(unit1 + '*' + unit2))
                return unit
            elif '/' in attr:
                attr = attr.split('/')
                attr1, attr2 = attr[0], attr[1]
                unit1 = check_unit(attr1)
                unit2 = check_unit(attr2)
                unit = str(sympify(unit1 + '/' + unit2))
                return unit

    if oper == "+" or oper == "-":  # Unit Conversion Not Needed - Just Check Valid Operation
        if check_unit(attr1) != check_unit(attr2):
            return False  # Invalid Operation
        else:
            return True  # Valid Operation

    else:  # Unit Conversion Needed (* or /)
        # new_unit = simplify("(" + check_unit(attr1) + ")" + oper + "(" + check_unit(attr2) + ")")
        return True
