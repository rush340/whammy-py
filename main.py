#!/usr/bin/env python

import argparse
import mido
import whammy
import sys
import errno

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('notes')
    #parser.add_argument('pattern') # TODO
    #parser.add_argument('bpm') # TODO
    args = parser.parse_args()

    notes = [int(note) for note in args.notes.split(',')]

    # ask which interface to use
    outputs = mido.get_output_names()
    if len(outputs) < 1:
        sys.stderr.write("Error: No MIDI output interfaces detected.\n")
        exit(errno.ENODEV)

    print "MIDI Output Interfaces:"
    for i, interface in enumerate(outputs):
        print "\t{}) {}".format(i + 1, interface)
    print "Enter the number of the interface your Whammy is connected to"
    output_index = int(raw_input()) - 1
    outport = mido.open_output(outputs[output_index])

    whammy_interface = whammy.WhammyInterface(outport)

    # arpeggiate
    pattern = whammy.WhammyArpPattern.UPDOWN
    whammy_arp = whammy.WhammyArp(whammy_interface, notes, pattern, 150)

    while (True):
        whammy_arp.play_next_step()

if __name__ == "__main__":
    main()