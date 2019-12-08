from typing import MutableSequence, Optional
CellType = Optional[MutableSequence]
TableType = MutableSequence[CellType]


class HashTable:
    INITIAL_SIZE = 8
    FILL_RATIO = 3 / 4
    SHRINK_RATIO = 1 / 2

    def __init__(self, seed=None):
        # seed are elements in hash table
        self._size = self.INITIAL_SIZE
        self._items: TableType = [None for _ in range(self._size)]
        if seed is not None:
            for value in seed:
                self.add(value)

    @property
    def size(self):
        return self._size

    def add(self, value):
        if (len(self) + 1) / self._size >= self.FILL_RATIO:
            self._resize()
        # counting indexes where we want to insert data , if the cell is in this index we add the value
        index = hash(value) % self._size
        if self._items[index] is None:
            self._items[index] = []
        elif value in self._items[index]:
            return
        self._items[index].append(value)

    def remove(self, value):
        index = hash(value) % self._size
        if self._items[index] is None:
            raise ValueError()
        if value not in self._items[index]:
            raise ValueError()
        self._items[index].remove(value)
        if not self._items[index]:
            self._items[index] = None
        if (len(self) + 1) / self._size <= self.SHRINK_RATIO:
            self._resize()

    def _resize(self, count=None):
        values = list(self)
        count = len(values) if count is None else count
        self._size = max(3 * count, 8)
        self._items = [None for _ in range(self._size)]
        for value in values:
            self.add(value)

    def __contains__(self, value):
        index = hash(value) % self._size
        if self._items[index] is None:
            return False
        if value in self._items[index]:
            return True
        return False

    def __len__(self):
        return sum([len(cell) for cell in self._items if cell is not None])

    def __iter__(self):
        return self.Iterator(self._items)

    class Iterator:
        def __init__(self, items):
            # global number for iterator's index
            self._items = items
            self._i = 0
            self._j = 0
            self._sublist = False

        def __iter__(self):
            return self

        def __next__(self):
            # checking if iterator is on the list inside cell
            if self._sublist is False:
                # if not then we are looking for the closest not empty cell
                while self._items[self._i] is None:
                    self._i += 1
                    # if we are at the end of the table, stop iteration
                    if self._i >= len(self._items):
                        raise StopIteration
                # if we found not empty cell, start iteration
                self._sublist = True
            # we are getting data from list inside a cell on the self._j
            value = self._items[self._i][self._j]
            self._j += 1
            # if self._j is out of scope of the list inside a cell
            # return to the iteration of cells not of a list
            if self._j >= len(self._items[self._i]):
                self._sublist = False
                self._j = 0
                self._i += 1
            # returning value
            return value
