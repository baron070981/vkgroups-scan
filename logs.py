import os
import sys
import time




class Logs:
    def __init__(self, filename = 'log.txt'):
        self.filename = filename
        self.COUNT = 1
        self.log_list = list()
        with open(filename, 'w') as f:
            pass
    
    
    def accum_logs(self, log_var):
        log_str = str(log_var).strip()
        t = time.ctime()
        log = str(self.COUNT)+'. '+t+' :: '+log_str+'\n'
        self.COUNT += 1
        self.log_list.append(log)
    
    
    def write_from_loglist(self):
        if len(self.log_list) > 0:
            with open(self.filename, 'a') as f:
                for data in self.log_list:
                    f.write(data)
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
    l.write_from_loglist()

