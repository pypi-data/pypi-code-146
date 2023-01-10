class Entity:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.partners = []
    def add_partner(self, partner):
        self.partners.append(partner)
if __name__ == '__main__':
    partner1 = Entity("Partner Inc", "partner")
    partner2 = Entity("Partner Co", "partner")
    partner3 = Entity("Partner LLC", "partner")
    
    partner1.add_partner(partner2)
    partner1.add_partner(partner3)
    
    print(len(partner1.partners))  # Output: [partner2, partner3]