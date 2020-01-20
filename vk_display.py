from PIL import ImageTk, Image
import tkinter as tk
import tkinter.ttk as ttk
import os
import variables as var
import requests
import time



class MainWindow(tk.Tk):
    def __init__(self, bg = '#000000'):
        self.app_id_list = list()
        self.owner_list = list()
        self.data_list = list()

        super(MainWindow, self).__init__()

        self.log_label = tk.Label(text = 'Логин')
        self.pas_label = tk.Label(text = 'Пароль')
        self.appid_label = tk.Label(text = 'id приложения')
        self.owner_label = tk.Label(text = 'id группы')

        self.log_entry = tk.Entry()
        self.pas_entry = tk.Entry()
        self.appid_combo = ttk.Combobox(values = self.app_id_list, height = 3)
        self.owner_combo = ttk.Combobox(values = self.owner_list, height = 3)

        self.button_start = tk.Button(text = 'сканировать', bg = 'red', fg = '#ffffff')

        self.label_data = tk.Label(text = 'Данные:')
        self.text_data = tk.Text(bg = 'blue', fg = 'yellow', height=2)

        self.img_label = tk.Label(bg = '#555555')

        self.log_label.grid(row = 0, column = 0, columnspan = 2, sticky = 'w'+'s'+'n'+'e')
        self.log_entry.grid(row = 1, column = 0, columnspan = 2, padx = 10, sticky = 'w'+'s'+'n'+'e')
        self.pas_label.grid(row = 0, column = 2, columnspan = 2, sticky = 'w'+'s'+'n'+'e')
        self.pas_entry.grid(row = 1, column = 2, columnspan = 2, padx = 10, sticky = 'w'+'s'+'n'+'e')
        self.appid_label.grid(row = 2, column = 0, columnspan = 2, sticky = 'w'+'s'+'n'+'e')
        self.appid_combo.grid(row = 3, column = 0, columnspan = 2, padx = 10, sticky = 'w'+'s'+'n'+'e')
        self.owner_label.grid(row = 2, column = 2, columnspan = 2, sticky = 'w'+'s'+'n'+'e')
        self.owner_combo.grid(row = 3, column = 2, columnspan = 2, padx = 10, sticky = 'w'+'s'+'n'+'e')
        self.button_start.grid(row = 4, column = 0, columnspan = 4, padx = 10, pady = 15, sticky = 'w'+'s'+'n'+'e')
        self.label_data.grid(row = 5, column = 0, pady = 10, sticky = 'w'+'s'+'n'+'e')
        self.text_data.grid(row = 5, column = 1, columnspan = 3, padx = 10, pady = 10, sticky = 'w'+'e')
        self.img_label.grid(row = 6, column = 0, columnspan = 4, sticky = 'w'+'s'+'n'+'e')

        self.STATE_DATA = False
        self.login = None
        self.password = None
        self.app_id = None
        self.owner_id = None
        self.image = None


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
        return True


    def default_insert(self, state_insert = True):
        if state_insert:
            self.log_entry.insert(0,'')
            self.pas_entry.insert(0,'')
            self.appid_combo.insert(0,'')
            self.owner_combo.insert(0,'-60427812')





    def show_image(self, url:str, id_img:int, folder:str = 'imagesvk', save_state = True):
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




st = False

def action(event):
    global st
    if root.STATE_DATA == False:
        root.default_insert()
        st = root.get_data_from_widgets()
        print(root.login, root.password, root.app_id, root.owner_id, st)
    else:
        print('Нет доступа к данным. ->', root.login, root.password, root.app_id, root.owner_id, st)








if __name__ == '__main__':
    pass
