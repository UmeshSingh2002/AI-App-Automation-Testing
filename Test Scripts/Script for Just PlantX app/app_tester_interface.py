from abc import ABC, abstractmethod

class AppTesterInterface(ABC):
    @abstractmethod
    def initializeDriver(self):
        pass

    @abstractmethod
    def analyzeImage(self, driver, index):
        pass