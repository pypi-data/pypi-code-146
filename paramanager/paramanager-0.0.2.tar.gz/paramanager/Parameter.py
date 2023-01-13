class Parameter:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name}: {self.value}"

    def __call__(self):
        return self.name, self.value
