import sys
import time
import requests
import vk_requests
from pprint import pprint
from PIL import ImageTk, Image
import tkinter as tk
from dataclasses import dataclass








@dataclass
class VkData:
    img_id:int = 0
    url_img:str = ''
    API_INIT:bool = False
    DATA_STATE:bool = False
    OFFSET:int = 0



class VkGroupsHelper:

    def __init__(self):
        self.api = None
        self.login = None
        self.password = None
        self.app_id = None
        self.group_data = None
        self.cach_ids = set()
        self.url_image = str()
        self.owner_id = None
        self.image_list = list()
        self.OFFSET = 0


    def init_api(self, login, password, app_id):
        try:
            self.api = vk_requests.create_api(app_id = app_id, login = login, password = password)
            return True
        except:
            print('Error init api')
            return False


    def __repr__(self):
        return '{}'.format(self.api)


    def get_groups_data(self, offset = 0, count = 2, owner_id = None):
        self.owner_id = owner_id
        if self.owner_id > 0:
            self.owner_id = 0 - self.owner_id
        if self.owner_id == 0:
            owner_id = -100
        return self.api.wall.get(owner_id = self.owner_id, offset = offset, count = count)


    def parse_group_data(self, group_data, data_list:list):
        time.sleep(.340)
        data_list.clear()
        for data_items in group_data['items']:
            if 'attachments' in data_items:
                if 'photo' in data_items['attachments'][0]:
                    url = data_items['attachments'][0]['photo']['sizes'][-1]['url']
                    iid = data_items['attachments'][0]['photo']['id']
                    if iid not in self.cach_ids:
                        print(iid,' ', url)
                        self.cach_ids.add(iid)
                        data_list.append(url)





if __name__ == '__main__':
    mainapi = VkGroupsHelper()
    mainapi.init_api('89992948531', 'baron070981', 7211649)
    print(mainapi)
    group_api = mainapi.get_groups_data(owner_id = -60427812)
    pprint(group_api)







