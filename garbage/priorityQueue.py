# Priority Queue Data Structure Class
import queue.PriorityQueue


class EnologPriorityQueue:
    # The lowest valued entries are retrieved first
    # (the lowest valued entry is the one returned by sorted(list(entries))[0]).
    # A typical pattern for entries is a tuple in the form: (priority_number, data).
    def __init__(self):
        self.queue = queue.PriorityQueue()

