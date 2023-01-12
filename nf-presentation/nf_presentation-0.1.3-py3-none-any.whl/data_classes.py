from .settings import (
                    EMPY_DESCRIPLION_REPLACEMENT,
                    EMPTY_TRAINER_NAME_REPLACEMENT,
                    UNKNOWN_GROUP_ID_NAME_REPLACEMENT)

class GroupInfo:
    """a class representing a position of exercise, in A1, A2, A3 B3 and others"""
    _group_names={
        1:'A',
        2:'B',
        3:'C'
    }
    def __init__(self, group_id:int, order:int):
        self._group_id=group_id
        self._order=order
    @property
    def id(self):
        return self._group_id
    @property
    def name(self):
        return self._group_names.get(self.id,UNKNOWN_GROUP_ID_NAME_REPLACEMENT)
    def __str__(self):
        return f'{self.name}{self._order}'

class AdditionalInfo:
    def __init__(self,data:dict):
        self.raw_data=data
    @property 
    def name(self):
        return self.raw_data.get('additional_name',{}).get('ru')
    @property
    def value(self):
        return self.raw_data.get('note')

class ExerciseInfo:
    def __init__(self, data:dict):
        self.raw_data : dict = data
        self._additionals : list[AdditionalInfo] = None
    @property
    def name(self):
        return self.raw_data.get('exercise_name',{}).get('ru')
    @property
    def scheme_main(self):
        return self.raw_data.get('exercise_scheme',{}).get('scheme_1')
    @property
    def description(self):
        description=self.raw_data.get('description')
        return description if description else EMPY_DESCRIPLION_REPLACEMENT
    @property
    def duration(self):
        return self.raw_data.get('duration')
    @property 
    def additionals(self) -> list[AdditionalInfo]:
        if self._additionals is None:
            # refactor!
            self._additionals=[AdditionalInfo(data) for data in self.raw_data.get('additional',[])]
            self._additionals.insert(0,AdditionalInfo({
                    "id": -1,
                    "additional_name": {
                        "en": "Duration",
                        "ru": "Длительность"
                    },
                    "training_exercise_id": -1,
                    "additional_id": -1,
                    "note": self.duration
                })) ##adding time
        return self._additionals
    @property
    def group(self) -> GroupInfo:
        return GroupInfo(
            group_id=self.raw_data.get('group'),
            order=self.raw_data.get('order'))



class TrainingInfo:
    def __init__(self,data:dict):
        self.raw_data=data
        self._exercises : list[ExerciseInfo] = None

    @property
    def exercises(self) -> list[ExerciseInfo]:
        if self._exercises is None:
            self._exercises= [ExerciseInfo(data) for data in self.raw_data.get('exercises_info')]
        return self._exercises

    @property
    def trainer_name(self):
        trainer_name =self.raw_data.get('trainer')
        return trainer_name if trainer_name else EMPTY_TRAINER_NAME_REPLACEMENT