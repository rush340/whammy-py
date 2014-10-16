import collections
import random


# TODO support changing pattern

class ArpeggiatorBase(object):
    '''
    Arpeggiates a numeric sequence
    '''

    name = None

    def __init__(self, notes):
        self.notes = list(collections.OrderedDict.fromkeys(notes))
        self.update_sequence()
        self._current_step = 0

    def __iter__(self):
        return self

    def next(self):
        note = self._sequence[self._current_step]
        self._current_step += 1
        if self._current_step >= len(self._sequence):
            self.pattern_reset()
            self._current_step = 0
        return note

    def update_sequence(self):
        raise NotImplementedError()

    def pattern_reset(self):
        pass
        

class UpArpeggiator(ArpeggiatorBase):
    name = 'UP'

    def update_sequence(self):
        self._sequence = sorted(self.notes)


class DownArpeggiator(ArpeggiatorBase):
    name = 'DOWN'

    def update_sequence(self):
        self._sequence = reversed(sorted(self.notes))


class UpDownArpeggiator(ArpeggiatorBase):
    name = 'UPDOWN'

    def update_sequence(self):
        self._sequence = sorted(self.notes) + list(reversed(sorted(self.notes)))[1:-1]


class RandomArpeggiator(ArpeggiatorBase):
    name = 'RANDOM'

    def update_sequence(self):
        self._sequence = self.notes[:]
        random.shuffle(self._sequence) 

    def pattern_reset(self):
        self.update_sequence()


class OrderArpeggiator(ArpeggiatorBase):
    name = 'ORDER'

    def update_sequence(self):
        self._sequence = self.notes


# map of arpeggiator names to their class
arpeggiators = {}
for cls in ArpeggiatorBase.__subclasses__():
    arpeggiators[cls.name] = cls