import twitter_track
from mpi4py import MPI

def analyze_tweets(tweet_batch):
    comm = MPI.COMM_SELF.Spawn(sys.executable, args=['analyze.py'],maxprocs=5)
    print "tweet batch"
    #print tweet_batch
    print("TWEET Rank: "+str(rank))
    print process_tweets(current)
    comm.Disconnect()