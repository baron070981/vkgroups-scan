#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import vk_display as disp
import vk_data as vkd
import variables as var
import logs
from pprint import pprint
import tkinter
from PIL import ImageTk, Image
from tkinter import messagebox
import threading

#filestate = False

# GLOBAL VARIABLES
GETDATA = True
LOCK = False
data_list = list()
TH = None

# СОЗДАНИЕ ОБЪЕКТОВ
log = logs.Logs() # объект записи хода выполнения программы
dtc = vkd.VkData() # объект с данными api
vk = vkd.VkGroupsHelper() # объект для работы с api
root = disp.MainWindow() #

root.file_state = root.default_insert()


def action():
    global root
    global vk
    global dtc
    global LOCK
    if root.STATE_DATA == False:
        dtc.DATA_STATE = root.get_data_from_widgets()
        if dtc.API_INIT == False:
            dtc.API_INIT = vk.init_api(root.login, root.password, root.app_id)
            TH = threading.Thread(target = root.progress_thread).start()
    if dtc.DATA_STATE and root.STATE_DATA and dtc.API_INIT:
        LOCK = True
    else:
        LOCK = False


def get_data_images(LOCK_STATE = False):
    global dtc
    global vk
    global root
    global data_list
    global GETDATA
    if LOCK_STATE == True and GETDATA == True:
        group_data = vk.get_groups_data(offset = dtc.OFFSET, count = 10, owner_id = root.owner_id)
        vk.parse_group_data(group_data, data_list)
        root.update()
        

def mains(event):
    global LOCK
    global GETDATA
    action()
    if LOCK:
        while True:
            get_data_images(LOCK_STATE = dtc.DATA_STATE)
            dtc.OFFSET += 10
            if len(data_list) > 0 and data_list[0].img_id in root.last_id_img_list:
                messagebox.showinfo('Info', 'Ни чего нового не найдено')
                LOCK = False
                GETDATA = False
                #break
            for data in data_list:
                root.show_image(data.url_img, data.img_id, save_state = True)
                time.sleep(.600)
            if dtc.OFFSET >= 300 or GETDATA == False:
                #TH.join()
                break




# ===================================

if __name__ == '__main__':
    root.button_start.bind('<Button 1>', mains)

    root.update()
    root.mainloop()
    log.write_from_loglist()










