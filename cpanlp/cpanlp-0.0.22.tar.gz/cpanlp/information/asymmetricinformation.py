class AsymmetricInformation:
    def __init__(self, sender, receiver, message, hidden_information=None):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.hidden_information = hidden_information
    def reveal_hidden_information(self):
        print(f"{self.sender} reveals hidden information to {self.receiver}: {self.hidden_information}")
    def is_information_complete(self):
        return self.hidden_information is None
    def negotiate(self):
        if self.hidden_information is not None:
            print(f"{self.sender} and {self.receiver} are negotiating to resolve the asymmetric information problem...")
            self.hidden_information = None
            print("Asymmetric information problem resolved")
        else:
            print("No asymmetric information to resolve")
    def add_hidden_information(self, new_hidden_information):
        if self.hidden_information is None:
            self.hidden_information = new_hidden_information
        else:
            self.hidden_information += "; " + new_hidden_information
    def get_hidden_information(self):
        return self.hidden_information
    def use_information(self):
        if self.hidden_information is not None:
            print(f"{self.receiver} uses the information received from {self.sender} to make a decision")
        else:
            print("Not enough information to make a decision")
    def is_information_useful(self):
        return self.hidden_information is None
    def get_advantage(self):
        if self.hidden_information is not None:
            print(f"{self.sender} has an advantage over {self.receiver} due to asymmetric information")
        else:
            print("No advantage due to symmetric information")
if __name__ == '__main__':
    info = AsymmetricInformation("Alice", "Bob", "I'm interested in buying your car", "I have a limited budget")
    info.reveal_hidden_information()
    if info.is_information_complete():
         print("Information is complete")
    else:
         print("Information is not complete")
    info.negotiate()
    info.add_hidden_information("I also have a deadline to meet")
    info.use_information()