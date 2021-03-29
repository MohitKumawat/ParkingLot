import abc

class Strategy(abc.ABC):

    @abc.abstractmethod
    def get_slot(self):
        pass

    @abc.abstractmethod
    def vacant_slot(self):
        pass
