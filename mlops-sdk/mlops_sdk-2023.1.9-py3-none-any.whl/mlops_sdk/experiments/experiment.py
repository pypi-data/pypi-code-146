from dateutil import parser


class Experiment:
    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) 실험 고유 ID


        ## Returns
        `mlops_sdk.experiments.Experiment`
        """
        self.id = kwargs.get("id")

        try:
            self.created_at = parser.parse(kwargs.get("created_at"))
        except TypeError:
            self.created_at = None
        try:
            self.updated_at = parser.parse(kwargs.get("updated_at"))
        except TypeError:
            self.updated_at = None

    def __str__(self) -> str:
        return self.name

    def get(self) -> dict:
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
