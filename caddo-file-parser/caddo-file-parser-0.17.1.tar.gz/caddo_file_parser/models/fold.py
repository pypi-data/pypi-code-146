class Fold:
    def __init__(self, number: int, train_indexes: [int], test_indexes: [int], seed: int):
        self.number = number
        self.train_indexes = train_indexes
        self.test_indexes = test_indexes
        self.seed = seed
