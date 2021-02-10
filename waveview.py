from PIL import Image, ImageDraw

import wave
import struct

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

width = 1200
height = 800

start = 0
r_samples = 1000

#w = wave.open("/home/nex/Downloads/out.wav", "rb")
w = wave.open("/home/nex/Downloads/aud.wav", "rb")

channels = w.getnchannels()
sample_rate = w.getframerate()
samples = w.getnframes()
depth = w.getsampwidth()

print("Audio file has %d channels, was recorded at %dHz for %d samples at a depth of %d bytes." % (channels, sample_rate, samples, depth))

w.setpos(start)
st = w.tell()
raw = w.readframes(r_samples)

samples = []
for i in range(0, len(raw), 2):
	samples.append(struct.unpack("<h", raw[i:i+2])[0])

#o = openwave("/home/nex/Downloads/sound/piano.wav", 44100, 44100)
#savewave(o, samples)

print("Read %d samples from %d to %d" % (len(samples)/2, st, w.tell()))

img = Image.new("L", (width, height), 255)
drw = ImageDraw.Draw(img)

M = -40000
m = 40000

for i in range(0, len(samples)):
	M = max(M, samples[i])
	m = min(m, samples[i])

spacing = (M-m)*0.1

m -= spacing
M += spacing

diff = M-m

print("Min: %d Max: %d Diff: %d" % (m, M, diff))

for i in range(1, len(samples)):
	px = int((i-1)/(len(samples)-1)*width)
	py = height - int(((samples[i-1]-m)/diff)*height)
	cx = int( i   /(len(samples)-1)*width)
	cy = height - int(((samples[i  ]-m)/diff)*height)
	
	drw.line((px, py, cx, cy), fill=0)

img.save("out.png")
