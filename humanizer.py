import time
import mido
import numpy as np
from scipy.stats import truncnorm
import multiprocessing
import threading
from multiprocessing import Queue
from multiprocessing.managers import SyncManager
import re
import math

MIDI_INPUT_PORT = 'humanizer 3'
MIDI_OUTPUT_PORT = 'loopMIDI Port 3'
counter = 0
BPM = 140
BEATS_PER_BAR = 4
BEAT_TIME = 60/BPM
BAR_TIME = BEAT_TIME * BEATS_PER_BAR
SIXTEENTH_NOTE_TIME = BAR_TIME / 16
MAX_MAIN_WORKERS = 50
MAX_OUTPUT_WORKERS = 20
#Input queue must be global for callback
in_queue = Queue()

def open_midi_ports(MIDI_INPUT_PORT, MIDI_OUTPUT_PORT):
    #Check if ports are available and set input port
    print('\n')
    print('INPUT PORTS: ')
    print (mido.get_input_names())
    print('\n')
    print('OUTPUT PORTS: ')
    print (mido.get_output_names())
    inport = mido.open_input(MIDI_INPUT_PORT)
    outport = mido.open_output(MIDI_OUTPUT_PORT)
    outport.close()
    print(f'Connected input to {MIDI_INPUT_PORT}')
    print(f'Connected output to {MIDI_OUTPUT_PORT}')
    return inport
    
                    
class Conductor:

    def __init__(self):
        pass
            
    def send_midi_message(self, message, outport):
        outport.send(message)   
        return 

    def add_to_send_queue(self, message, out_queue):
        out_queue.put(message, block=False)
        return
        
    def read_midi_message(self, msg, metronome_1, human_1, cpu_1, cpu_2, cpu_3, cpu_4, cpu_5, cpu_6, cpu_7, cpu_8, cpu_9, cpu_10, cpu_11, T0, timing_array, metronome_error, out_queue, metronome_timestamp):
        #Sort message and call relevant functions
        t1 = time.time()
        msg_type = msg.type
        channel = msg.channel
        msg_str = str(msg)
        if channel == 1 :
            if msg_type == 'note_on' and msg.velocity > 10:
                self.add_to_send_queue(msg, out_queue)
                human_1.record_timing(timing_array, T0)
                print('added timing')
                return
            if msg_type == 'note_off' :
                self.add_to_send_queue(msg, out_queue)
                return
        if msg_type == 'note_on' :
            if channel == 0 :
                metronome_error.value = metronome_1.beat_error(T0)
                metronome_timestamp.value = time.time()
                return
            if channel == 2 :
                timing = cpu_1.allocate_timing(timing_array, T0)
                cpu_1.time_message(timing, t1, metronome_error, metronome_timestamp)
                self.add_to_send_queue(msg, out_queue)
                return
            if channel == 3 :
                timing = cpu_2.allocate_timing(timing_array, T0)
                cpu_2.time_message(timing, t1, metronome_error, metronome_timestamp)
                self.add_to_send_queue(msg, out_queue)
                return
            if channel == 4 :
                timing = cpu_3.allocate_timing(timing_array, T0)
                cpu_3.time_message(timing, t1, metronome_error, metronome_timestamp)
                self.add_to_send_queue(msg, out_queue)
                return
            if channel == 5 :
                timing = cpu_4.allocate_timing(timing_array, T0)
                cpu_4.time_message(timing, t1, metronome_error, metronome_timestamp)
                self.add_to_send_queue(msg, out_queue)
                return
            if channel == 6 :
                timing = cpu_5.allocate_timing(timing_array, T0)
                cpu_5.time_message(timing, t1, metronome_error, metronome_timestamp)
                self.add_to_send_queue(msg, out_queue)
                return
            if channel == 7 :
                timing = cpu_6.allocate_timing(timing_array, T0)
                cpu_6.time_message(timing, t1, metronome_error, metronome_timestamp)
                self.add_to_send_queue(msg, out_queue)
                return
            if channel == 8 :
                timing = cpu_7.allocate_timing(timing_array, T0)
                cpu_7.time_message(timing, t1, metronome_error, metronome_timestamp)
                self.add_to_send_queue(msg, out_queue)
                return
            if channel == 9 :
                timing = cpu_8.allocate_timing(timing_array, T0)
                cpu_8.time_message(timing, t1, metronome_error, metronome_timestamp)
                self.add_to_send_queue(msg, out_queue)
                return
            if channel == 10 :
                timing = cpu_9.allocate_timing(timing_array, T0)
                cpu_9.time_message(timing, t1, metronome_error, metronome_timestamp)
                self.add_to_send_queue(msg, out_queue)
                return
            if channel == 11 :
                timing = cpu_10.allocate_timing(timing_array, T0)
                cpu_10.time_message(timing, t1, metronome_error, metronome_timestamp)
                self.add_to_send_queue(msg, out_queue)
                return
            if channel == 12 :
                timing = cpu_11.allocate_timing(timing_array, T0)
                cpu_11.time_message(timing, t1, metronome_error, metronome_timestamp)
                self.add_to_send_queue(msg, out_queue)
                return

    def multiprocess_init(self, T0, timing_array, metronome_error, out_queue, metronome_timestamp,):
        #Initialise multiprocessing for main workers and message publishers
        for _ in range(MAX_MAIN_WORKERS):
            p = multiprocessing.Process(target=self.worker_main, args=(T0, timing_array, metronome_error, out_queue, metronome_timestamp))
            p.start()
        for _ in range(MAX_OUTPUT_WORKERS):
            q = multiprocessing.Process(target=self.output_worker, args=(out_queue,))
            q.start()
        return 

    def worker_main(self, T0, timing_array, metronome_error, out_queue, metronome_timestamp):
        #Main worker initialisation and loop
        metronome_1 = Metronome(0)
        human_1 = Human(1)
        cpu_1 = CPU(2, 0.5, 0.5)
        cpu_2 = CPU(2, 0.5, 0.5)
        cpu_3 = CPU(2, 0.5, 0.5)
        cpu_4 = CPU(2, 0.5, 0.5)
        cpu_5 = CPU(2, 0.5, 0.5)
        cpu_6 = CPU(2, 0.5, 0.5)
        cpu_7 = CPU(2, 0.5, 0.5)
        cpu_8 = CPU(2, 0.5, 0.5)
        cpu_9 = CPU(2, 0.5, 0.5)
        cpu_10 = CPU(2, 0.5, 0.5)
        cpu_11 = CPU(2, 0.5, 0.5)
        while 1:
            msg = in_queue.get()
            self.read_midi_message(msg, metronome_1, human_1, cpu_1, cpu_2, cpu_3, cpu_4, cpu_5, cpu_6, cpu_7, cpu_8, cpu_9, cpu_10, cpu_11, T0, timing_array, metronome_error, out_queue, metronome_timestamp)
    
    def output_worker(self, out_queue,):
        #Publish output messages from main workers
        outport = mido.open_output(MIDI_OUTPUT_PORT)
        while 1:
                msg = out_queue.get()
                self.send_midi_message(msg, outt)
                
    def input_worker(self, msg):
        #Called when message arrives in midi input port
        in_queue.put(msg, block=False)
        return

                      
class Player:
    
    def __init__(self, midi_channel_number):
        self.midi_channel_number = midi_channel_number

    def check_time(self, T0):
        current_time = time.time() - T0.value
        return current_time

    def get_beat_number(self, T0):
        #Return current 16th note beat number
        beat_number = -1
        bar_time_passed = self.check_time(T0) - BAR_TIME * self.get_bar_number(T0)
        while bar_time_passed > 0:
            bar_time_passed = bar_time_passed - SIXTEENTH_NOTE_TIME
            beat_number = beat_number + 1
        return beat_number

    def get_bar_number(self, T0):
        #Return current bar number
        bar_number = -1
        track_time_passed = self.check_time(T0)
        while track_time_passed > 0:
            track_time_passed = track_time_passed - BAR_TIME
            bar_number = bar_number + 1
        return bar_number

    def get_beats_passed_time(self, T0):
        #Return length of bar passed so far
        beats_passed_time = (self.get_beat_number(T0))*SIXTEENTH_NOTE_TIME
        return beats_passed_time

    def get_bars_passed_time(self, T0):
        #Return bar time passed so far
        bars_passed_time = self.get_bar_number(T0)*BAR_TIME
        return bars_passed_time

    def get_timing(self, T0):
        #Identify current beat number and player offset from it
        beat_number = self.get_beat_number(T0)
        beat_offset = round(((self.check_time(T0)-self.get_bars_passed_time(T0)-self.get_beats_passed_time(T0))*1000), 1)
        if beat_offset > SIXTEENTH_NOTE_TIME * 1000 / 2 :
            beat_offset = beat_offset - SIXTEENTH_NOTE_TIME * 1000
            beat_number = beat_number + 1
        if beat_number == 16:
            beat_number = 0
        return beat_number, beat_offset


class Metronome(Player):

    def __init__(self, midi_channel_number):
        super().__init__(midi_channel_number)

    def count_in(self):
        #Count in to sync program with ableton
        counter = 0
        bars = int(input('Enter number of count in bars: '))
        total_beats = bars * 16 + 1
        for msg in inport:
            msg_str = str(msg)
            channel = int(re.search(r'channel=(.*?) ', msg_str).group(1))
            if channel == 0 and bool(re.search(r'note_on', msg_str)):
                counter = counter + 1
                if counter % 4 == 0:
                    print((((total_beats - counter)-1)/4)+1)
            if counter >= total_beats:
                return
                    
    def beat_error(self, T0):
        #Find how out of sync ableton is 
        metronome_error = round(((self.get_bars_passed_time(T0)+self.get_beats_passed_time(T0)+SIXTEENTH_NOTE_TIME-self.check_time(T0))*1000), 1)
        if self.get_beat_number(T0) % 4 == 0:
            if metronome_error > (SIXTEENTH_NOTE_TIME * 1000 / 2):
                metronome_error = metronome_error - (SIXTEENTH_NOTE_TIME * 1000)   
        return metronome_error
        
    
class Human(Player):

    def __init__(self, midi_channel_number):
        super().__init__(midi_channel_number)
               
    def record_timing(self, timing_array, T0):
        #Add player timing to shared array object
        beat_number, beat_offset = self.get_timing(T0)
        timing_array_line = timing_array[beat_number]
        timing_array_line[3] += 1
        if beat_offset > timing_array_line[1] or timing_array_line[1]==0 :
            timing_array_line[1] = beat_offset
        if beat_offset < timing_array_line[0] or timing_array_line[0]==0 :
            timing_array_line[0] = beat_offset
        new_mean = (timing_array_line[2] * (timing_array_line[3]-1) + beat_offset)/timing_array_line[3]
        timing_array_line[2] = new_mean
        sd = timing_array_line[4]
        new_sd = math.sqrt((((sd * sd) * (timing_array_line[3] - 1)) + (beat_offset - new_mean)**2) / timing_array_line[3])
        timing_array_line[4] = new_sd
        timing_array[beat_number] = timing_array_line
        print(timing_array)
        return timing_array


class CPU(Player):

    previous_mean = 0
    
    def __init__(self, midi_channel_number, listening, consistency):
        super().__init__(midi_channel_number)
        self.listening = listening
        self.consistency = consistency

    def get_truncated_normal(self, mean, sd, low, upp):
        #Create truncated normal object
        if sd == 0 :
            sd = 2
            low = low - 5
            upp = upp + 5
        return truncnorm(
            (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
        

    def allocate_timing(self, timing_array, T0):
        #Return random timing based on distribution
        beat_number, beat_offset = self.get_timing(T0)
        mean = timing_array[beat_number][2]
        self.previous_mean = mean + self.previous_mean * self.listening
        sd = timing_array[beat_number][4]
        low = timing_array[beat_number][0]
        upp = timing_array[beat_number][1]
        timing_dist = self.get_truncated_normal(self.previous_mean, sd, low, upp)
        timing = timing_dist.rvs()
        return timing

    def time_message(self, timing, t1, metronome_error, metronome_timestamp):
        #Adjust timing of midi message according to calculations
        t2 = time.time()   
        wait_time = BAR_TIME + (timing / 1000) - t2 + t1 + (metronome_error.value / 1000)
        time.sleep(wait_time)
        return    

    
if __name__ == "__main__":
    inport = open_midi_ports(MIDI_INPUT_PORT, MIDI_OUTPUT_PORT)
    print('initialising class instances...')
    metronome_1 = Metronome(0)
    conductor_1 = Conductor()
    out_queue = Queue()
    print('Setting up process manager...')
    manager = SyncManager()
    manager.start()
    scalar_timing_array = np.ndarray.tolist(np.zeros((16,5)))
    timing_array = manager.list(scalar_timing_array)
    metronome_error = manager.Value('f', 0)
    T0 = manager.Value('f', time.time())
    metronome_timestamp = manager.Value('f', 0)
    print('Initialising multiprocessing...')
    conductor_1.multiprocess_init(T0, timing_array, metronome_error, out_queue, metronome_timestamp,)
    metronome_1.count_in()
    inport.callback = conductor_1.input_worker
    print('program starting...') 
    while 1:
        time.sleep(5)
            

    
            
        


