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

filestate = False

GETDATA = True
log = logs.Logs()
dtc = vkd.VkData()
vk = vkd.VkGroupsHelper()
root = disp.MainWindow()
LOCK = False
root.file_state = root.default_insert()
log.accum_logs([str(dtc.__class__), str(vk.__class__), str(root.__class__)])


def action():
    log.accum_logs('----Call action(event)-----')
    global root
    global vk
    global dtc
    global LOCK
    log.accum_logs('----Start state:-----')
    log.accum_logs(['STATE DATA:'+str(root.STATE_DATA), 'INIT API:'+str(dtc.API_INIT),
                    'DATA STATE:'+str(dtc.DATA_STATE)])
    if root.STATE_DATA == False:
        dtc.DATA_STATE = root.get_data_from_widgets()
        log.accum_logs(['STATE DATA:'+str(root.STATE_DATA), 'DATA STATE:'+str(dtc.DATA_STATE)])
        if dtc.API_INIT == False:
            dtc.API_INIT = vk.init_api(root.login, root.password, root.app_id)
            log.accum_logs('Init api good' + str(dtc.API_INIT))

    if dtc.DATA_STATE and root.STATE_DATA and dtc.API_INIT:
        log.accum_logs('-----Returned from action TRUE-----')
        LOCK = True
    else:
        log.accum_logs('----Returned from action FALSE----')
        log.accum_logs(['STATE DATA:'+str(root.STATE_DATA), 'INIT API:'+str(dtc.API_INIT),
                        'DATA STATE:'+str(dtc.DATA_STATE)])
        LOCK = False



data_list = list()

def get_data_images(LOCK_STATE = False):
    log.accum_logs('----Call get data images()-----')
    global dtc
    global vk
    global root
    print(dtc, vk, root)
    global data_list
    global GETDATA
    log.accum_logs(['LOCK STATE:'+str(LOCK_STATE)])
    if LOCK_STATE == True and GETDATA == True:
        log.accum_logs('---GETTING DATAS-----')
        group_data = vk.get_groups_data(offset = dtc.OFFSET, count = 10, owner_id = root.owner_id)
        vk.parse_group_data(group_data, data_list)
        root.update()
print

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
                break
            for data in data_list:
                root.show_image(data.url_img, data.img_id, save_state = True)
                time.sleep(.600)
            if dtc.OFFSET >= 300 or GETDATA == False:
                break




# ===================================

if __name__ == '__main__':

    log.accum_logs('To cicles mainloop')
    root.button_start.bind('<Button 1>', mains)

    root.update()
    root.mainloop()
    log.write_from_loglist()










