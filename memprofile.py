'''
Created on 4 Jul 2019

@author: Alex Ip

Decorator to show memory usage at start and end of function.
Note that the "after" figure is shown before garbage collection occurs on out-of-scope variables 

Modified from Ihor Bobak's version at
http://web.archive.org/web/20180416235121/http://ihorbobak.com/index.php/2018/02/22/python-process-memory-profiling/
'''
import time
import os
import psutil

def memprofile(func):
    '''
    Decorator to show memory usage at start and end of function.
    '''
    def elapsed_since(start):
        '''
        Function to return time elapsed from start time
        '''
        return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))
    
    
    def get_process_memory():
        '''
        Function to return memory usage of current process
        '''
        process = psutil.Process(os.getpid())
        return process.memory_info().rss


    def wrapper(*args, **kwargs):
        '''
        Wrapper function for memprofile decorator
        '''
        mem_before = get_process_memory()
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = elapsed_since(start)
        mem_after = get_process_memory()
        print("{}: memory before: {:,}, after: {:,}, consumed: {:,}; exec time: {}".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before,
            elapsed_time))
        return result
    return wrapper