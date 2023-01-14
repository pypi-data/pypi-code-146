class Incentive:
    def __init__(self, type, amount, recipients):
        self.type = type
        self.amount = amount
        self.recipients = recipients
if __name__ == '__main__':
    financial_incentive = Incentive("financial", 5000, "employees")