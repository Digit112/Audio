import math
import numpy as np
import struct
import time
import wave

note_f = [27.50, 29.14, 30.87, 32.70, 34.65, 36.71, 38.89, 41.20, 43.65, 46.25, 49.00, 51.91, 55.00, 58.27, 61.74, 65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.67, 311.13, 329.63, 349.23, 369.99, 392.00, 415.31, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.26, 698.46, 739.99, 784.00, 830.61, 880.00, 932.33, 987.77, 1046.50, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.00, 1864.66, 1975.53, 2093.00, 2217.46, 2349.32, 2489.02, 2637.02, 2793.83, 2959.96, 3235.96, 3322.44, 3520.00, 3729.31, 3951.07, 4186.01]

note_n = {"A0":0, "A#0":1, "Bb0":1, "B0":2, "C1":3, "C#1":4, "Db1":4, "D1":5, "D#1":6, "Eb1":6, "E1":7, "F1":8, "F#1":9, "Gb1":9, "G1":10, "G#1":11, "Ab1":11, "A1":12, "A#1":13, "Bb1":13, "B1":14, "C2":15, "C#2":16, "Db2":16, "D2":17, "D#2":18, "Eb2":18, "E2":19, "F2":20, "F#2":21, "Gb2":21, "G2":22, "G#2":23, "Ab2":23, "A2":24, "A#2":25, "Bb2":25, "B2":26, "C3": 27, "C#3":28, "Db3":28, "D3":29, "D#3":30, "Eb3":30, "E3":31, "F3":32, "F#3":33, "Gb3":33, "G3":34, "G#3":35, "Ab3":35, "A3":36, "A#3":37, "Bb3":37, "B3":38, "C4":39, "C#4":40, "Db4":40, "D4":41, "D#4":42, "Eb4":42, "E4": 43, "F4":44, "F#4":45, "Gb4":45, "G4":46, "G#4":47, "Ab4":47, "A4":48, "A#4":49, "Bb4":49, "B4":50, "C5":51, "C#5":52, "Db5":52, "D5":53, "D#5":54, "Eb5":54, "E5":55, "F5":56, "F#5":57, "Gb5":57, "G5":58, "G#5":59, "Ab5":59, "A5":60, "A#5":61, "Bb5":61, "B5":62, "C6":63, "C#6":64, "Db6":64, "D6":65, "D#6":66, "Eb6":66, "E6":67, "F6":68, "F#6":69, "Gb6":69, "G6":70, "G#6":71, "Ab6":71, "A6":72, "A#6":73, "Bb6":73, "B6":74, "C7":75, "C#7":76, "Db7":76, "D7":77, "D#7":78, "Eb7":78, "E7":79, "F7":80, "F#7":81, "Gb7":81, "G7":82, "G#7":83, "Ab7":83, "A7":84, "A#7":85, "Bb7":85, "B7":86, "C8":87}

piano_f = [1.54, 1.17, 1.37, 0.93, 0.62, 0.76, 0.69, 1.09, 1.30, 1.53, 1.64, 1.56, 1.43, 1.55, 1.54, 1.85, 2.03, 1.95, 2.03, 2.09, 2.75, 2.9, 2.45, 2.07, 2.99, 3.08, 3.4, 4.24, 4.58, 6.94, 7.53, 7.91, 10.41, 10.6, 10.51, 10.66, 17.22, 17, 17.3, 17.82, 18.26, 20.29, 19.12, 19.86, 19.67, 19.57, 20.66, 22.85, 22.89, 22.45, 22.78, 22.33, 22.23, 21.7, 22.17, 22.43, 21.45, 21.8, 22.14, 24.85, 27.99, 26.61, 23.29, 20.46, 20.02, 20.13, 18.33, 17.92, 17.52, 16.62, 16.62, 15.53, 15.44,14.92, 14.56, 14.47, 13.45, 13.14, 12.83, 12.01, 11.73, 11.71, 11.24, 10.72, 10.66, 10.73, 10.43, 9.87]



















def note(n):
	return note_f[note_n[n]]

def openwave(fn, sample_rate, samples):
	w = wave.open(fn, "wb")

	w.setnchannels(1)
	w.setsampwidth(2)
	w.setframerate(sample_rate)
	w.setnframes(samples)
	
	return w

def savewave(w, buff):
	for i in range(0, len(buff), 32):
		num = min(i+32, len(buff))
		w.writeframes(struct.pack("<%dh" % (num-i), *map(lambda a : int(a), buff[i:num])))
	
	w.close()

def sine(w, frequency, amplitude, duration):
	x = np.arange(w.getframerate()*duration)
	f = frequency/w.getframerate()
	out = np.sin(2*np.pi*x*f)
	return out*32767*amplitude

def saw(w, frequency, amplitude, duration):
	x = np.arange(w.getframerate()*duration)
	f = frequency/w.getframerate()
	out = ((x*f) % 1) * 2 - 1
	return out*32767*amplitude

def tri(w, frequency, amplitude, duration):
	x = np.arange(w.getframerate()*duration)
	f = frequency/w.getframerate()
	out = -np.abs((x*f) % 1 - 0.5)*4+1
	return out*32767*amplitude


def square(w, frequency, amplitude, duration):
	x = np.arange(w.getframerate()*duration)
	f = frequency/w.getframerate()
	out = np.sign((x*f) % 1 - 0.5)
	return out*32767*amplitude

def sympathetic(w, frequency, amplitude, duration):
	x = np.arange(w.getframerate()*duration)
	f = frequency/w.getframerate()
	out = piano_f[0]*np.sin(8372.02*np.pi*x)/600
	for i in range(1, len(piano_f)):
		out += piano_f[i]*np.sin(2*np.pi*4186.01/(2**(7.25*i/87))*x)/600
	return out*32767*amplitude

sample_rate = 44100
duration = 3

samples = sample_rate*duration

w = openwave("/home/nex/Downloads/aud.wav", sample_rate, samples)

out = (sine(w, note("C1"), 0.8, 1) + sine(w, note("C2"), 0.8, 1)*2 + sine(w, note("C3"), 0.8, 1)*4 + sine(w, note("C4"), 0.8, 1)*8 + sine(w, note("C5"), 0.8, 1)*4 + sine(w, note("C6"), 0.8, 1)*2 + sine(w, note("C7"), 0.8, 1))/22

savewave(w, out)




















