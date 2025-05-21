class APIObject:
    def __init__(self, fullName: str, objectType: str, appearances: int, link: str):
        self.fullName = fullName
        self.name = self.fullName.split('.')[-1] # class or method name on it's own
        self.type = objectType # Either class or method
        self.appearances = appearances
        self.link = link # Link to class/method info documentation

    def getFullName(self):
        return self.fullName
    
    def getName(self):
        return self.name

    def getType(self):
        return self.type
    
    def getAppearances(self):
        return self.appearances 
    
    def getLink(self):
        return self.link
    
    def incrementAppearances(self):
        self.appearances += 1

    # For debugging purposes
    def to_dict(self):
        return {
            "name": self.fullName,
            "type": self.type,
            "appearances": self.appearances,
            "link": self.link
        }
