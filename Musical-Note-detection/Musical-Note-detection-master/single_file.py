import numpy as np
import wave
import struct
from flask import Flask

# Flask Constructor
app = Flask(__name__)

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

############################## Initialize ##################################


# Some Useful Variables
window_size = 2205    # Size of window to be used for detecting silence
beta = 1   # Silence detection parameter
max_notes = 100    # Maximum number of notes in file, for efficiency
sampling_freq = 44100	# Sampling frequency of audio signal
threshold = 600
array = [16.35,18.35,20.60,21.83,24.50,27.50,30.87,
         32.70,36.71,41.20,43.65,49.00,55.00,61.74,
         65.41,73.42,82.41,87.31,98.00,110.00,123.47,
         130.81,146.83,164.81,174.61,196.00,220.00,246.94,
         264.63,293.66,329.63,349.23,392.00,440.00,493.88,
         523.25,587.33,659.25,698.46,783.99,880.00,987.77,
    	 1046.50, 1174.66, 1318.51, 1396.91, 1567.98, 1760.00, 1975.53,
         2093.00, 2349.32, 2637.02, 2793.83, 3135.96, 3520.00, 3951.07,
         4186.01, 4698.63, 5274.04, 5587.65, 6271.93, 7040.00, 7902.13]

notes = ['C0','D0','E0','F0','G0','A0','B0',
         'C1','D1','E1','F1','G1','A1','B1',
         'C2','D2','E2','F2','G2','A2','B2',
         'C3','D3','E3','F3','G3','A3','B3',
         'C4','D4','E4','F4','G4','A4','B4',
         'C5','D5','E5','F5','G5','A5','B5',
         'C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6',
         'C7', 'D7', 'E7', 'F7', 'G7', 'A7', 'B7',
         'C8', 'D8', 'E8', 'F8', 'G8', 'A8', 'B8']
Identified_Notes = []

############################## Read Audio File #############################
print ('\n\nReading Audio File...')

sound_file = wave.open('C:/Users/hinslifesyles/Downloads/Musical-Note-detection-master/Musical-Note-detection-master/redemption_song.wav', 'r')
file_length = sound_file.getnframes()

sound = np.zeros(file_length)
mean_square = []
sound_square = np.zeros(file_length)
for i in range(file_length):
    data = sound_file.readframes(1)
    data = struct.unpack("<h", data)
    sound[i] = int(data[0])
    
sound = np.divide(sound, float(2**15))	# Normalize data in range -1 to 1


######################### DETECTING SCILENCE ##################################

sound_square = np.square(sound)
frequency = []
dft = []
i = 0
j = 0
k = 0    
# traversing sound_square array with a fixed window_size
while(i<=len(sound_square)-window_size):
	s = 0.0
	j = 0
	while(j<=window_size):
		s = s + sound_square[i+j]
		j = j + 1	
# detecting the silence waves
	if s < threshold:
		if(i-k>window_size*4):
			dft = np.array(dft) # applying fourier transform function
			dft = np.fft.fft(sound[k:i])
			dft=np.argsort(dft)

			if(dft[0]>dft[-1] and dft[1]>dft[-1]):
				i_max = dft[-1]
			elif(dft[1]>dft[0] and dft[-1]>dft[0]):
				i_max = dft[0]
			else :	
				i_max = dft[1]
# claculating frequency				
			frequency.append((i_max*sampling_freq)/(i-k))
			dft = []
			k = i+1
	i = i + window_size

print('length',len(frequency))
print("frequency")   
@app.route("/")
for i in frequency :
	print(i)
	idx = (np.abs(array-i)).argmin()
	Identified_Notes.append(notes[idx])
print(Identified_Notes)


if __name__ == "__main__":
  app.run(host="0.0.0.0")



