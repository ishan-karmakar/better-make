import abc


class Step:
    def __init__(self):
        self.dependencies = []
        self.run = False

    def dependsOn(self, step):
        self.dependencies.append(step)
        return self
    
    def execute(self):
        pass

    def __call__(self):
        for dep in self.dependencies:
            dep()
        if not self.run:
            self.execute()
            self.run = True

class PathStep(Step):
    @abc.abstractmethod
    def get_path(self) -> str:
        pass