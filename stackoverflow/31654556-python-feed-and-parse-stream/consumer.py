#!/usr/bin/env python
import os
import random
import subprocess
import time
import threading
import Queue
import atexit

def setup():
    # make a named pipe for every file the program should write
    logfilepipe='logpipe'
    os.mkfifo(logfilepipe)

def cleanup():
    # put your named pipes here to get cleaned up
    logfilepipe='logpipe'
    os.remove(logfilepipe)

atexit.register(cleanup)

class MyIter():
    sample_data=[0,1,2,4,9,-100,16,25,100,-8,'seven',10000,144,8,47,91,2.4,'^',56,18,77,94]
    def __init__(self, numiterations=1000):
        self.numiterations=numiterations
        self.current = 0

    def __iter__(self):
        return self

    def next(self):
        self.current += 1
        if self.current > self.numiterations:
            raise StopIteration
        else:
            return random.choice(self.__class__.sample_data)

def parse_func(source,line):
    print "[%s] %s" % (source,line)

def input_func(p, queue):
    # run the command with output redirected
    for line in MyIter(10): # Limit for testing purposes
        time.sleep(0.1) # sleep a tiny bit
        p.stdin.write(str(line)+'\n')
        queue.put(('INPUT', line))

    p.stdin.close()
    p.wait()
    queue.put(('QUIT', True))
    
def read_output(source, queue, tag=None):
    print "Starting to read output for %r" % source
    if isinstance(source,str):
        source=open(source, 'r') # open file with string name
    line = source.readline()
    while line != '':
        queue.put((tag, line.rstrip()))
        line = source.readline()

if __name__=='__main__':
    cmd='daemon.py'

    # set up our FIFOs instead of using files - put file names into setup() and cleanup()
    setup()

    logfilepipe='logpipe'
    
    # Message queue for handling all output, whether it's stdout, stderr, or a file output by our command
    lq = Queue.Queue()

    # open the subprocess for command
    print "Running command."
    p = subprocess.Popen(['/Users/aaron/Development/scraps/stackoverflow/31654556-python-feed-and-parse-stream/'+cmd,logfilepipe], 
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Start threads to handle the input and output
    threading.Thread(target=input_func, args=(p, lq)).start()
    threading.Thread(target=read_output, args=(p.stdout, lq, 'OUTPUT')).start()
    threading.Thread(target=read_output, args=(p.stderr, lq, 'ERRORS')).start()

    # open a thread to read any other output files (e.g. log file) as named pipes
    threading.Thread(target=read_output, args=(logfilepipe, lq, 'LOG')).start()

    # Now combine the results from our threads to do what you want
    run=True
    while(run):
        (tag, line) = lq.get()
        if tag == 'QUIT':
            run=False
        else:
            parse_func(tag, line)

