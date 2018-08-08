import subprocess

# START = 250000
START = 600000
nSamples = 100000
batchSize = 10000
for start, end in zip(range(0, nSamples+1, batchSize), range(batchSize, nSamples+1, batchSize)):
	start += 1 + START
	end += START
	subprocess.Popen('python coord2loc.py --s %d --e %d' % (start, end), shell=True)
