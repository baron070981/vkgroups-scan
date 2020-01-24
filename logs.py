#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
from random import randint
from pprint import pprint



class Logs:
    def __init__(self, filename = 'log.txt'):
        self.filename = filename
        self.COUNT = 1
        self.log_list = list()
        with open(filename, 'w') as f:
            pass
    
    
    def accum_logs(self, *log_var):
        #print('Type:', type(log_var), ' Len:', len(log_var))
        log_var = log_var[0]
        if type(log_var) == list:
            for data in log_var:
                t = time.ctime()
                log = str(self.COUNT)+'. '+t+' :: '+str(data)
                self.log_list.append(log)
                self.COUNT += 1
        else:
            t = time.ctime()
            log = str(self.COUNT)+'. '+t+' :: '+str(log_var)
            self.log_list.append(log)
            self.COUNT +=1
    
    
    def write_from_loglist(self):
        if len(self.log_list) > 0:
            with open(self.filename, 'a') as f:
                for data in self.log_list:
                    f.write(data+'\n')
            self.log_list.clear()
    
    
    def write_log(self, log_str:str):
        t = time.ctime()
        log = str(self.COUNT)+'. '+t+' :: '+log_str+'\n'
        with open(self.filename, 'a') as f:
            f.write(log)
            self.COUNT += 1
            





if __name__ == '__main__':
    l = Logs()
    for i in range(5):
        time.sleep(.700)
        l.accum_logs('error test')
    
    sl = list()
    for i in range(5):
        time.sleep(.700)
        nums = [chr(randint(53, 77)) for i in range(randint(10,30))]
        s = ''.join(nums)
        sl.append(s)
    
    l.accum_logs(sl)
    
    l.write_from_loglist()
    
    
    
    
    
    
    
    
    

