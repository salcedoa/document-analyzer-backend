class APIObject:
    def __init__(self, name: str, objectType: str, appearances: int, link: str):
        self.name = name
        self.type = objectType
        self.appearances = appearances
        self.link = link
