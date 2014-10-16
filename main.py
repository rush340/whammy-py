#!/usr/bin/env python

import argparse
import mido
import whammy
import sys
import errno
from arpeggiator import arpeggiators


class PrintPort(mido.ports.BaseOutput):
    '''
    A mido Port that just prints MIDI messages to console
    '''
    def _send(self, message):
        print message


def main():
    pattern_options = ', '.join(arpeggiators.keys())

    parser = argparse.ArgumentParser()
    parser.add_argument('pattern',
        help='Arpeggiator pattern to apply to notes. options: {}'.format(pattern_options))
    parser.add_argument('bpm', type=int,
        help='Beats Per Minute to run arpeggio.  Notes are played as quarter notes.')
    parser.add_argument('notes', 
        help='Comma separated list of semitones up to an octave above the root (0-12)')
    parser.add_argument('--fakeoutport', dest='fakeoutport', action='store_true',
        help='No output port. Print MIDI messages to console for debugging.')
    args = parser.parse_args()

    # TODO validate
    pattern_name = args.pattern

    notes = [int(note) for note in args.notes.split(',')]

    bpm = args.bpm

    if args.fakeoutport:
        outport = PrintPort()
    else:
        # ask which interface to use
        outputs = mido.get_output_names()
        if len(outputs) < 1:
            sys.stderr.write("Error: No MIDI output interfaces detected.\n")
            exit(errno.ENODEV)

        print "MIDI Output Interfaces:"
        for i, interface in enumerate(outputs):
            print "\t{}) {}".format(i + 1, interface)
        print "Enter the number of the interface your Whammy is connected to:",
        raw_value = raw_input()
        output_index = int(raw_value) - 1
        outport = mido.open_output(outputs[output_index])

    whammy_interface = whammy.WhammyInterface(outport)
    whammy_arp = whammy.WhammyArp(whammy_interface, notes, pattern_name, bpm)

    while (True):
        whammy_arp.play_next_step()


if __name__ == "__main__":
    main()