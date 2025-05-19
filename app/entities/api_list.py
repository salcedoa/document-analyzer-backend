from .api_object import APIObject
import json

class APIList:
    def __init__(self):
        self.APIObjectsList = []
        # TODO: For now, only Python is supported.
        self.language = "python" 
        self.moduleNames = [] # List of the library's modules

    def recordAPIObject(self, apiObject: APIObject):
        self.APIObjectsList.append(apiObject)

    def addModuleName(self, moduleName: str):
        if moduleName not in self.moduleNames:
            self.moduleNames.append(moduleName)
    
    def getModuleNames(self):
        return self.moduleNames

    def getAPIObjectsList(self):
        return self.APIObjectsList
    
    # Check if class or method already exists in the list
    def hasAPIObject(self, name: str):
        for obj in self.APIObjectsList:
            if obj.getName() == name:
                return obj
        return None
    
    def hadAPIObectFullName(self, name: str):
        for obj in self.APIObjectsList:
            if obj.getFullName() == name:
                return obj
        return None
    
    # Increment the appearances of a class or method
    def incrementAPIObject(self, name: str):
        for obj in self.APIObjectsList:
            if obj.getName() == name or obj.getFullName() == name:
                obj.incrementAppearances()
                return True
        return False

    # For debugging purposes
    def to_json(self):
        return json.dumps({
            "APIObjectsList": [x.to_dict() for x in self.APIObjectsList]
        })
