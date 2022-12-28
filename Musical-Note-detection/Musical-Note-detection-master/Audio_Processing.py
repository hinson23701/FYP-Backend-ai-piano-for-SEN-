#############################################################################
#									    #
#			Musical Note Identification			    #
#									    #
#############################################################################

import numpy as np
import wave
import struct


sampling_freq = 44100	#Sampling frequency of audio signal
window = 2205           #Size of window to be used for detecting silence
threshold = 600         #threshold value
dft = []                #array to store dtf value
start = []              #array holding start indices of each note
end = []                #array holding end   indices of each note
Identified_Notes = []   #list of identified notes

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


def play(sound_file):

    Identified_Notes[:] = []                #Clear the list every time play() is called
    start[:] = []
    end[:] = []
    
    file_length = sound_file.getnframes()   #Decode Audio File       
    sound = np.zeros(file_length)

    for i in range(file_length):
        data = sound_file.readframes(1)
        data = struct.unpack("<h", data)
        sound[i] = int(data[0])

    sound = np.divide(sound, float(2**15))

    sound_square = np.square(sound)         #square each element of sound[]
    
    i = 0
    j = 0
    f = 0
    t = 0
    
    while(i<(file_length) - window):
        s = 0.00
        j = 0
        if(t==0):
            start.append(i)                 #store start point of note
            f = 0
            t = 1 
        while(j<=window):
            s = s + sound_square[i + j]
            j = j + 1
        if(s<=threshold):
            if(f==0):
                end.append(i)               #store end point of note
                f = 1
        else:
            if(f==1):
                f = 0
                t = 0
        i = i + window

    i = 0
    
    while(i<len(end)):                      #Identify Notes
        dft = np.array(np.fft.fft(sound[start[i]:end[i]]))  # applying fourier transform function
        dft = np.argsort(dft)
        if(dft[0]>dft[-1] and dft[1]>dft[-1]):
            i_max = dft[-1]
        elif(dft[1]>dft[0] and dft[-1]>dft[0]):
            i_max = dft[0]
        else:
            i_max = dft[1]
        fr = (i_max*sampling_freq)/((end[i]) - (start[i]))   # claculating frequency
        idx = (np.abs(array-fr)).argmin()
        Identified_Notes.append(notes[idx])
        i = i + 1
        
    print(Identified_Notes)


############################## Read Audio File #############################

if __name__ == "__main__":
    
    #code for checking output for single audio file
    #Reading audio file
    
    sound_file = wave.open('redemption_song.wav', 'r')
    
    #call play() to identify notes
    print("Notes in File 1 = ")
    play(sound_file)

    #code for checking output for remaining all audio files
    for file_number in range(2,6):
        file_name = "Audio_files/Audio_" + str(file_number) + ".wav"
        sound_file = wave.open(file_name)
        print("Notes in File " + str(file_number) + " = ")
        play(sound_file)



