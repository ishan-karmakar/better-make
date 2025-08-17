import threading

class Step:
    def __init__(self):
        self.dependencies = []
        self.run = False
        self.changed = False

    def dependsOn(self, step):
        self.dependencies.append(step)
        return self
    
    def execute(self):
        pass

    def should_rerun(self) -> bool:
        return False

    def __call__(self):
        if self.run:
            return

        if self.dependencies:
            threads = []
            for i in range(1, len(self.dependencies)):
                thread = threading.Thread(target=self.dependencies[i])
                thread.start()
                threads.append(thread)
            self.dependencies[0]()
            for thread in threads:
                thread.join()

        # We consider this task changed if any of the dependencies had to rerun or step itself needs to rerun
        self.changed = any(dep.changed for dep in self.dependencies) or self.should_rerun()
        if self.changed:
            self.execute()
            self.run = True
