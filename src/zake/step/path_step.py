from ._step import Step
import abc

# Specialization of a Step that outputs a file
class PathStep(Step):
    @abc.abstractmethod
    def get_path(self) -> str:
        pass
