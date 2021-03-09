import math
from engine.constants import HAULER_CAPACITY


class GameTask:
    def __init__(self, priority, weight):
        self.priority = priority
        self.weight = weight
        self.is_active = False

    def weighted_priority(self):
        return self.priority * self.weight


class Haul(GameTask):
    def __init__(self, priority, weight, resource_type, amount, requester, origin=None):
        super().__init__(priority, weight)
        self.resource_type = resource_type
        self.resource_amount = amount
        self.requester = requester
        self.origin = origin
        self.hauler_list = []
        required_haulers_raw = float(amount) / float(HAULER_CAPACITY)
        self.required_haulers = math.ceil(required_haulers_raw)


class Build(GameTask):
    def __init__(self, priority, weight, construction):
        super().__init__(priority, weight)
        self.requested_construction = construction
        self.builder_list = []
        self.working_builders = 0


class TaskManager:
    def __init__(self):
        self.task_list = []

    def run_tasks(self):
        for task in self.task_list:
            if task is Haul:
                self.run_haul_task(task)
            if task is Build:
                self.run_build_task(task)

    def create_haul_task(self, priority, weight, resource_type, amount, requester, origin=None):
        haul = Haul(priority, weight, resource_type, amount, requester, origin)
        self.task_list.append(haul)

    def create_build_task(self, priority, weight, construction):
        build = Build(priority, weight, construction)
        self.task_list.append(build)

    def run_haul_task(self, task):
        pass

    def run_build_task(self, task):
        pass
