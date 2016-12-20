import queue

"""
See http://stackoverflow.com/questions/8196254/iterating-queue-queue-items for more information
"""


class ImprovedQueue(queue.Queue):
    def to_list(self):
        """
        Returns a copy of all items in the queue without removing them.
        """

        with self.mutex:
            return list(self.queue)

    def clear(self):
        """
        Clears all elements of the queue
        """
        with self.mutex:
            self.queue.clear()
