import random_scene_generator as rsg
import time

MIDI_INPUT_PORT = 'humanizer 2'
MIDI_OUTPUT_PORT = 'loopMIDI Port 2'

def read_midi_messages(inport):
    for msg in inport.iter_pending() :
        print(msg)
        outport.send(msg)
    return
        
def write_midi_message(msg):
    return
    
    
if __name__ == "__main__":
    inport, outport = rsg.open_midi_ports(MIDI_INPUT_PORT, MIDI_OUTPUT_PORT)
    while 1:
        read_midi_messages(inport)

