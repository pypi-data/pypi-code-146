from busy.busyqueue import BusyQueue
from ..plugins.todo.task import Task
from ..plugins.todo.task import Plan
from ..plugins.todo.task import DoneTask
from busy import dateparser


def is_today_or_earlier(plan):
    return plan.date <= dateparser.today()


class TodoQueue(BusyQueue):
    itemclass = Task
    key = 'tasks'

    def __init__(self, manager=None, items=[]):
        super().__init__(manager, items)
        self._plans = None
        self._done = None

    @property
    def plans(self):
        if not self._plans:
            if self.manager:
                self._plans = self.manager.get_queue(PlanQueue.key)
            else:
                self._plans = PlanQueue()
        return self._plans

    @property
    def done(self):
        if not self._done:
            if self.manager:
                self._done = self.manager.get_queue('done')
            else:
                self._done = DoneQueue()
        return self._done

    def defer(self, date, *criteria):
        indices = self.select(*(criteria or [1]))
        plans = [self.get(i+1).as_plan(date) for i in indices]
        self.plans.add(*plans)
        self.delete_by_indices(*indices)

    def activate(self, *criteria, today=False):
        if today:
            indices = self.plans.select(is_today_or_earlier)
        elif criteria:
            indices = self.plans.select(*criteria)
        else:
            return
        tasks = [self.plans.get(i+1).as_todo() for i in indices]
        self.add(*tasks, index=0)
        self.plans.delete_by_indices(*indices)

    def finish(self, *indices, date=None):
        if not date:
            date = dateparser.today()
        donelist, keeplist = self._split_by_indices(*indices)
        self._items = keeplist
        self.done.add(*[t.as_done(date) for t in donelist])
        self.add(*filter(None, [t.as_followon() for t in donelist]))
        self.plans.add(*filter(None, [t.as_repeat() for t in donelist]))
        return "Finished " + " ".join([str(i) for i in indices])

    def resource(self, index=1):
        return self._items[index-1].resource if self._items else None

    def get_without_resource(self, index=1):
        return self._items[index-1].without_resource if self._items else None


BusyQueue.register(TodoQueue, default=True)


class PlanQueue(BusyQueue):
    itemclass = Plan
    key = 'plans'


BusyQueue.register(PlanQueue)


class DoneQueue(BusyQueue):
    itemclass = DoneTask
    key = 'done'


BusyQueue.register(DoneQueue)
