#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import ImageTk, Image
import tkinter as tk
import tkinter.ttk as ttk
import os
import variables as var
import requests
import time
from tkinter import messagebox
import re
import sys



class MainWindow(tk.Tk):
    def __init__(self, bg = '#000000'):
        self.app_id_list = list()
        self.owner_list = list()
        self.data_list = list()

        super(MainWindow, self).__init__()

        self.log_label = tk.Label(text = 'login')
        self.pas_label = tk.Label(text = 'password')
        self.appid_label = tk.Label(text = 'id app')
        self.owner_label = tk.Label(text = 'id club')

        self.log_entry = tk.Entry()
        self.pas_entry = tk.Entry()
        self.appid_combo = ttk.Combobox(values = self.app_id_list, height = 3)
        self.owner_combo = ttk.Combobox(values = self.owner_list, height = 3)

        self.button_start = tk.Button(text = 'scan', bg = 'red', fg = '#ffffff')

        self.label_data = tk.Label(text = 'data:')
        self.text_data = tk.Text(bg = 'blue', fg = 'yellow', height=2, width = 10)

        self.img_label = tk.Label(bg = '#555555')

        self.log_label.grid(row = 0, column = 0, sticky = 'w'+'s'+'n'+'e')
        self.log_entry.grid(row = 1, column = 0, padx = 10, sticky = 'w'+'s'+'n'+'e')
        self.pas_label.grid(row = 2, column = 0, sticky = 'w'+'s'+'n'+'e')
        self.pas_entry.grid(row = 3, column = 0, columnspan = 2, padx = 10, sticky = 'w'+'s'+'n'+'e')
        self.appid_label.grid(row = 4, column = 0, sticky = 'w'+'s'+'n'+'e')
        self.appid_combo.grid(row = 5, column = 0, padx = 10, sticky = 'w'+'s'+'n'+'e')
        self.owner_label.grid(row = 6, column = 0, sticky = 'w'+'s'+'n'+'e')
        self.owner_combo.grid(row = 7, column = 0, padx = 10, sticky = 'w'+'s'+'n'+'e')
        self.button_start.grid(row = 8, column = 0, padx = 10, pady = 15, sticky = 'w'+'s'+'n'+'e')
        self.label_data.grid(row = 9, column = 0, pady = 10, sticky = 'w'+'s'+'n'+'e')
        self.text_data.grid(row = 10, column = 0, padx = 10, pady = 10, sticky = 'w'+'e')
        self.img_label.grid(row = 0, rowspan = 11, column = 1, sticky = 'w'+'s'+'n'+'e')

        self.STATE_DATA = False
        self.login = None
        self.password = None
        self.app_id = None
        self.owner_id = None
        self.image = None
        self.file_state = False


    def set_lists(self, appid_list, owner_list):
        self.app_id_list = list(appid_list)
        self.owner_list = list(owner_list)
        return len(self.app_id_list), len(self.owner_list)



    def get_data_from_widgets(self):
        if self.STATE_DATA == False:
            self.login = self.log_entry.get()
            self.password = self.pas_entry.get()
            app_id = self.appid_combo.get()
            owner_id = self.owner_combo.get()
            if self.login == '' or self.password == '' or app_id == '' or owner_id == '':
                self.STATE_DATA = False
                return False
            elif len(self.login) > 0 and len(self.password) > 0 and len(app_id) > 0 and len(owner_id) > 0:
                try:
                    self.app_id = int(app_id)
                    self.owner_id = int(owner_id)
                except:
                    self.STATE_DATA = False
                    return False
                if self.owner_id > 0:
                    self.owner_id = 0 - self.owner_id
                if self.owner_id == 0:
                    self.owner_id = -100
        self.STATE_DATA = True
        if self.file_state == False:
            with open('appdata.txt', 'w') as f:
                try:
                    f.write('login:'+self.login+'\n')
                    f.write('password:'+self.password+'\n')
                    f.write('app_id:'+str(self.app_id)+'\n')
                    f.write('owner:'+str(self.owner_id)+'\n')
                    self.file_state = True
                except:
                    messagebox.showwarning('Warning', 'Error load data to file')
        return True


    def default_insert(self, state_insert = True):
        '''
    формат файла appdata.txt:
      login:user login
      password:user password    
      appid:app_id
      .....
      .....
        может быть сколько угодно
      owner:owner_id
      ......
      ......
        может быть сколько угодно
    
    порядок строк строго соблюдать не обязательно
    в каждой строке должно быть только одно значение
        '''
        if state_insert:
            if os.path.exists('appdata.txt') == False:
                messagebox.showwarning('Warnning', 'Not found file')
                return False
            with open('appdata.txt', 'r') as f:
                data = f.read().split('\n')
                parent = r'(.+):(.+)'
                for line in data:
                    if 'own' in line[0:5].strip():
                        try:
                            owner = int(re.search(parent, line).group(2).strip())
                            self.owner_list.append(owner)
                        except:
                            continue
                    if 'app' in line[0:5].strip():
                        try:
                            appid = int(re.search(parent, line).group(2).strip())
                            self.app_id_list.append(appid)
                        except:
                            continue
                    if 'log' in line[0:5].strip():
                        self.login = re.search(parent, line).group(2).strip()
                    if 'pas' in line[0:5].strip():
                        self.password = re.search(parent, line).group(2).strip()
            self.owner_combo.config(values = self.owner_list)
            self.appid_combo.config(values = self.app_id_list)
            self.owner_combo.set(value = self.owner_list[0])
            self.log_entry.insert(0, self.login)
            self.pas_entry.insert(0, self.password)
            self.appid_combo.set(value = self.app_id_list[0])
            return True





    def show_image(self, url, id_img, folder = 'imagesvk', save_state = True):
        os.makedirs(folder, exist_ok = True)
        req = requests.get(url)
        if req.status_code != 200:
            return False
        t = time.ctime().strip()
        t = t.split(' ')
        t = '_'.join(t)
        t = t.split(':')
        t = '_'.join(t)
        filename = str(id_img)+'.jpg'
        fold = folder+ '\\' + filename
        state_file = False
        with open(fold, 'wb') as f:
            try:
                f.write(req.content)
                self.text_data.delete(1.0, tk.END)
                self.text_data.insert(1.0, 'Succes load:'+url)
                state_file = True
            except:
                self.text_data.delete(1.0, tk.END)
                self.text_data.insert(1.0, 'Error load: ' + url)
        if state_file:
            self.image = ImageTk.PhotoImage(Image.open(fold))
            self.img_label.configure(image = self.image)
            self.img_label.image = self.image
            self.update()
            if save_state == False:
                os.remove(fold)









if __name__ == '__main__':
    root = MainWindow()
    root.default_insert()
    print(root.default_insert.__doc__)
    root.mainloop()












