
import mido
import time
import arpeggiator as arp


class WhammyInterface(object):
    '''
    Interface for sending notes to the Whammy pedal

    SEMITONES_TO_POSITION maps # of semitones above root to a pedal position MIDI CC 
    value (0-127) for octave up mode.
    For example, if E is played, SEMITONES_TO_POSITION[3] will be G

    I determined these values by playing an open E string into the Whammy
    into a strobe turner.

    Some notes may be slightly flat or sharp because of the low 127 step resolution.
    '''
    SEMITONES_TO_POSITION = [0, 10, 21, 31, 42, 53, 63, 74, 84, 95, 105, 116, 127]
    PEDAL_POSITION_CC = 11

    def __init__(self, outport, channel=0):
        '''
        Arguments:
        outport: mido MIDI output port for the Whammy V
        channel: MIDI channel number (int) for the Whammy V
        '''
        self.outport = outport
        self.channel = channel

    def reset(self):
        '''Resets pedal position to 0 (heel down, toe up)'''
        pass # TODO

    def prepare(self):
        '''Prepare pedal for sequence (change to single octave up mode)'''
        pass # TODO

    def send_note(self, note):
        '''
        Set the Whammy to a note

        note: note in semitones above root (0-12, where 0 is the root and 12 is an octave up)
        '''
        position = self.SEMITONES_TO_POSITION[note]
        midi_msg = mido.Message('control_change', control=self.PEDAL_POSITION_CC, value=position)
        self.outport.send(midi_msg)


class WhammyArp(object):
    def __init__(self, interface, notes, pattern_name, bpm):
        '''
        interface: A WhammyInterface object for the pedal you want to control.
        notes: notes to be played, defined as a list of unique semitones from the root (0-12)
        bpm: Beats per minute. Notes will be played as quarter notes.
        '''
        self.interface = interface
        self.notes = notes
        self.arp = arp.arpeggiators[pattern_name](notes)
        self.bpm = bpm

    @staticmethod
    def bpm_to_seconds_per_quarter(bpm):
        return 15.0 / bpm

    @staticmethod
    def quarter_seconds_to_bpm(seconds):
        return 15.0 / seconds

    @property
    def bpm(self):
        return self.quarter_seconds_to_bpm(self.step_time)

    @bpm.setter
    def bpm(self, value):
        self.step_time = self.bpm_to_seconds_per_quarter(value)
    
    def play_next_step(self):
        self.interface.send_note(self.arp.next())
        time.sleep(self.step_time)
