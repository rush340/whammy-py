import random
import pytest
import arpeggiator


def test_arp_up():
    pattern = 'UP'
    notes = [0, 1, 2]
    arp = arpeggiator.arpeggiators[pattern](notes)

    result = []
    for i in range(6):
        result.append(arp.next())

    expected = [0, 1, 2, 0, 1, 2]
    assert result == expected

def test_arp_dupe():
    pattern = 'UP'
    notes = [0, 1, 2, 1]
    arp = arpeggiator.arpeggiators[pattern](notes)

    result = []
    for i in range(6):
        result.append(arp.next())

    expected = [0, 1, 2, 0, 1, 2]
    assert result == expected

def test_arp_random():
    pattern = 'RANDOM'
    notes = [0, 1, 2, 3]
    random.seed(1234567890)
    arp = arpeggiator.arpeggiators[pattern](notes)

    result = []
    for i in range(6):
        result.append(arp.next())

    expected = [2, 0, 1, 3, 0, 1]
    assert result == expected