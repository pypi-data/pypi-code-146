from cpanlp.person.person import *
class AsymmetricInformation:
    def __init__(self, sender:Person, receiver:Person, message:str, hidden_information:str):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.hidden_information = hidden_information
    def reveal_hidden_information(self):
        print(f"{self.sender.name} reveals hidden information to {self.receiver.name}: {self.hidden_information}")
    def is_information_complete(self):
        return self.hidden_information is None
    def negotiate(self):
        if self.hidden_information is not None:
            print(f"{self.sender.name} and {self.receiver.name} are negotiating to resolve the asymmetric information problem...")
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
            print(f"{self.receiver.name} uses the information received from {self.sender.name} to make a decision")
        else:
            print("Not enough information to make a decision")
    def is_information_useful(self):
        return self.hidden_information is None
    def get_advantage(self):
        if self.hidden_information is not None:
            print(f"{self.sender.name} has an advantage over {self.receiver.name} due to asymmetric information")
        else:
            print("No advantage due to symmetric information")
if __name__ == '__main__':
    p1=Person("Alice",16)
    p2=Person("bob",23)
    info = AsymmetricInformation(p1, p2, "I'm interested in buying your car", "I have a limited budget")
    info.reveal_hidden_information()
    if info.is_information_complete():
         print("Information is complete")
    else:
         print("Information is not complete")
    info.negotiate()
    info.add_hidden_information("I also have a deadline to meet")
    info.use_information()