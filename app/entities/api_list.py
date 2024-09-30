from .api_object import APIObject

class APIList:
    def __init__(self):
        self.APIObjectsList = []
        # TODO: For now, only Python is supported.
        self.language = "python" 

    def recordAPIObject(self, apiObject: APIObject):
        self.APIObjectsList.append(apiObject)
