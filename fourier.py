import numpy as np
import wave
import struct

width=1200
height=800

start = 0
r_samples = 168*16

w = wave.open("/home/nex/Downloads/sound/piano.wav", "rb")

channels = w.getnchannels()
sample_rate = w.getframerate()
samples = w.getnframes()
depth = w.getsampwidth()

print("Audio file has %d channels, was recorded at %dHz for %d samples at a depth of %d bytes." % (channels, sample_rate, samples/2, depth))

w.setpos(start)
st = w.tell()
raw = w.readframes(r_samples*2)

samples = []
for i in range(0, len(raw), 2):
	samples.append(struct.unpack("<h", raw[i:i+2])[0])

print("Read %d samples from %d to %d" % (len(samples)/2, st, w.tell()))

sample_c = []
for n in range(0, 88):
	f = 4186.01/2**(7.25*n/87)
	w = 1/f
	
	for s in range(0, len(samples)):
		t = s/44100
		
		r = 2*np.pi*(t%w)/w
		m = samples[s]
		
		x=np.cos(r)*m
		y=np.sin(r)*m
		
		sample_c.append( (x, y) )

	tx = 0
	ty = 0
	for i in range(0, len(sample_c)):
		tx += sample_c[i][0]
		ty += sample_c[i][1]
	
	avg = (tx/len(sample_c), ty/len(sample_c))
	print("f=%.2f, m=%.2f" % (f, (avg[0]*avg[0]+avg[1]*avg[1])**0.5))
		






