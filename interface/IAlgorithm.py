
from abc import ABC, abstractmethod
class IAlgorithm(ABC):
    @abstractmethod
    def is_allowed(self, user, limit):
        pass
    
class IResettable(ABC):
        @abstractmethod
        def reset(self, user):
            pass
        
class IStatTracker(ABC):
        @abstractmethod
        def get_stats(self, user) -> dict:
            pass