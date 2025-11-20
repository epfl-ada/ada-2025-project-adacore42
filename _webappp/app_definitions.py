from enum import Enum

class TabData:
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id

class MainTabs(Enum):
    HOME = TabData("Home", 0)
    AXIS_1 = TabData("Axis 1", 1)
    AXIS_2 = TabData("Axis 2", 2)
    ABOUTUS = TabData("About Us", 3)


