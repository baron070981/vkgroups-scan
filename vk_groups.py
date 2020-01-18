import os
import sys
import time
import vk_display as disp
import vk_data as vkd
import variables as var
import logs


log = logs.Logs()
log_str = ''
dtc = vkd.VkData()
vk = vkd.VkGroupsHelper()
root = disp.MainWindow()
log_str += (str(dtc)+'\n'+str(vk.__class__)+'\n' + str(root.__class__))
log.write_log(log_str)



def action(event):
    global root
    global vk
    global dtc
    log.write_log('Button click')
    log.write_log(str(root.STATE_DATA))
    if root.STATE_DATA == False:
        root.default_insert()
        dtc.DATA_STATE = root.get_data_from_widgets()
        log.write_log('Get data from widgets: '+str(root.STATE_DATA))
        log.write_log('Not init API'+str(dtc.API_INIT))
        print(dtc.DATA_STATE)
        if dtc.API_INIT == False:
            dtc.API_INIT = vk.init_api(root.login, root.password, root.app_id)
            log.write_log('Init API '+str(dtc.API_INIT))
            print(dtc.API_INIT)


data_list = list()

def get_data_images(LOCK_STATE = False):
    global dtc
    global vk
    global root
    print(dtc, vk, root)
    global data_list
    if LOCK_STATE == True:
        group_data = vk.get_groups_data(offset = dtc.OFFSET, count = 30, owner_id = root.owner_id)
        vk.parse_group_data(group_data, data_list)
        root.button_start.configure(text = 'data')
        root.update()








# ===================================

if __name__ == '__main__':


    root.button_start.bind('<Button 1>', action)
    get_data_images(LOCK_STATE = dtc.DATA_STATE)
    print(data_list)
    root.mainloop()

    print()










