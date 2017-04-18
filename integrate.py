import mpi4py
from mpi4py import MPI
import subprocess
from subprocess import PIPE
import sys
import os
import twitter_track
from datetime import datetime
import ast

from os import path
from wordcloud import WordCloud
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
#how to run: mpiexec -n 5 python integrate.py
from multiprocessing import Pool,Process

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()

#os.path.dirname(os.path.realpath(__file__)) 

data = {}

TWITTER_USERS = ['NYT','washingtonpost', 'WSJ', 'BBC', 'YahooNews']

test_data = {"hi":50,"yo":12,"anime":100}
tweet = "Anime is cool and you should watch something"

def text_from_twitter(tweetDict):
	print "Tweet"


def callC(tweet=""):
	#pwd = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
	#print tweet
	os.chdir('/home/home1/lz107/cs590final/c')
	#args = ["./","main"]
	args_call = ["./PROG1",tweet]
	p = subprocess.Popen(args_call,stdin=PIPE, stdout=PIPE, stderr=PIPE)
	print p.stdout.read()
	#data.update(ast.literal_eval(p.stdout.read()))
	#print data
	#return data

def createCloud(filename, frequencies=None):
	print filename
	d = path.dirname(__file__)
	#generate from frequencies
	text = open(path.join(d, filename+'.txt')).read()
	if len(text)>0:
		wordcloud = WordCloud().generate(text)
		#WordCloud().generate_from_frequencies(frequencies,15)
		plt.figure()
		plt.imshow(wordcloud, interpolation="bilinear")
		plt.axis("off")
		plt.show()
		print "DONE SHOW CLOUD"
		# The pil way (if you don't have matplotlib)
		image = wordcloud.to_image()
		image.show()
		return


def main():
	#print "START"
	#print str(datetime.now())
	comm = MPI.COMM_WORLD
	#MPI.COMM_SELF.Spawn(sys.executable, args=['integrate.py'],maxprocs=5)
	#for i in range(0, 10 ,1):
	#print "MPI: "+str(rank)
	twitter_track.do_everything(TWITTER_USERS[rank])

	'''
	print("Hello! I'm rank %d from %d running in total..." % (comm.rank, comm.size))
	print("Hello! I'm rank %d from %d running in total..." % (comm.rank, comm.size))
	print("Hello! I'm rank %d from %d running in total..." % (comm.rank, comm.size))
	print("Hello! I'm rank %d from %d running in total..." % (comm.rank, comm.size))
	'''
	#comm.Disconnect()
	#print "END"
	#print str(datetime.now())
	
	comm.Barrier()   # wait for everybody to synchronize _here_
	#print "2 END"
	#print str(datetime.now())

if __name__ == '__main__':
	print "tweets or cloud? (t/c)"
	userInput = sys.stdin.readline().strip()
	if (userInput == 't'):
		main()
	else:
		pool = Pool()
        pool.map(createCloud, TWITTER_USERS)
		#for user in TWITTER_USERS:
		#	createCloud(user)
