import os
import sys
import time
import vk_display as disp
import vk_data as vkd
import variables as var


dtc = vkd.VkData()
vk = vkd.VkGroupsHelper()
root = disp.MainWindow()


def action(event):
    global root
    global vk
    global dtc
    if root.STATE_DATA == False:
        dtc.DATA_STATE = root.get_data_from_widgets()
        print(dtc.DATA_STATE)
        if dtc.API_INIT == False:
            dtc.API_INIT = vk.init_api(root.login, root.password, root.app_id)
            print(dtc.API_INIT)


def get_data_images(LOCK_STATE = False):
    global dtc
    global vk
    global root
    print(dtc, vk, root)
    data_list = list()
    if LOCK_STATE == True:
        group_data = vk.get_groups_data(offset = dtc.OFFSET, count = 30, owner_id = root.owner_id)
        vk.parse_group_data(group_data, data_list)
        print(data_list)








# ===================================

if __name__ == '__main__':


    root.button_start.bind('<Button 1>', action)
    get_data_images(LOCK_STATE = dtc.DATA_STATE)

    root.mainloop()
