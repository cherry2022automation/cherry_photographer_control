# =============================================== 
# Cherry_Photographer_GUI_ver3.1.py
# ===============================================
# コンボボックスの値を取得してボタンが押されたら出力
# -----------------------------------------------
# ・コンボボックス追加
# ・デバック用ボタン追加
# ・入力欄クラス化
# ・画像表示 png→jpeg対応
# ・画像リサイズ
# ・画像をフレーム内に描画
# ；画像を4枚配置
# ・画像関連整理
# ・メニューバー表示
# ・マニュアル操作ウィンドウ追加
# ・ログボックス追加(紐づけなし)
# ・ファイル名生成実装
# ・フレーム配置改善
# ・ステータスハイライト表示実装
# ・各フレーム、フレームクラス継承
# ・画像更新 リアルタイム化
# ・動作紐づけ
# ・ファイル名表示
# ・最終調整
# -----------------------------------------------

from re import M
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import tkinter as tk
import os
from xml.sax.handler import feature_namespace_prefixes
from PIL import Image, ImageTk
import threading
from datetime import datetime
import time
import cherry_photographer_CUI as cherry

from pyparsing import col
import shutil

frame_around_pixel = 10

class control_frame(tk.Frame):

    variety = ["高砂", "佐藤錦", "紅秀峰"]
    grade = ["特秀", "秀", "マル秀", "ハネ出し"]
    size = ["S", "M", "L", "test"] # 要修正

    runnning = False

    def create_new_file_name(self):
        serial_text = str(self.new_serial_number()).zfill(5)
        time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        variety_en = {"高砂":"Takasago", "佐藤錦":"Satonishiki", "紅秀峰":"Benishuho"}
        grade_en = {"特秀":"Tokushu", "秀":"Shu", "マル秀":"Marushu", "ハネ出し":"Hanedashi"}
        directions = ["RIGHT", "BUTTOM", "LEFT", "TOP"]
        extension = '.bmp'
        new_file_names = []
        for dir in directions:
            new_file_names.append(serial_text + "_" + variety_en[self.cbox_variety.get()] + "_" + grade_en[self.cbox_grade.get()] + "_" + self.cbox_size.get() +  "_" + time_stamp + "_" + dir + extension)
        return new_file_names

    def new_serial_number(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        directory = directory + "\\picture\\"
        files = os.listdir(directory)
        now_serial_number = 0
        for file in files:
            file_names = file.split("_", 1)
            try:
                serial_number = int(file_names[0])
                now_serial_number = serial_number
            except:
                pass
        new_serial_number = now_serial_number + 1
        return new_serial_number
    
    def function_run(self):
        self.button_run['state'] = "disable"

        file_names = self.create_new_file_name()
        file_name = file_names[0].replace('_RIGHT.bmp', '')
        self.picture_frame_1.view_picture_name.set(file_name)

        thread = threading.Thread(target=self.cycle_run)
        thread.start()

        
        self.button_run['state'] = "normal"

    def shoot_and_get(self, cherry_pi_num, file_names):
        drive = ["I", "J", "K", "L"]
        original_directory = drive[cherry_pi_num-1] + ":\\Desktop\\data\\cherry_photographer\\picture\\"
        save_directory = os.path.dirname(os.path.abspath(__file__))
        save_directory = save_directory + "\\picture\\"

        client = cherry.SocketClient(cherry.ip[cherry_pi_num-1], cherry.CAMERA_PORT)
        client.shoot(file_names[cherry_pi_num-1])
        shutil.copyfile(original_directory+file_names[cherry_pi_num-1], save_directory+file_names[cherry_pi_num-1])
        self.picture_frame_1.view_picture_names[cherry_pi_num-1] = file_names[cherry_pi_num-1]
        self.picture_frame_1.picture_update_en[cherry_pi_num-1] = True

    def cycle_run(self):

        file_names = self.create_new_file_name()
        offset = 8
        point_1 = cherry.point_1 + offset
        point_2 = cherry.point_2 + offset

        origin = 0
        sequence_num = 1

        angle_open = 90
        angle_close = -20

        self.picture_frame_1.view_picture_names = ["", "", "", ""]
        self.picture_frame_1.picture_update_en = [True, True, True, True]

        self.master.configure(bg='pink')

        client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
        client.servo(angle_open)

        sequence_num += 1
        status_box_frame_1.update_status_box_text(sequence_num)
        client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
        client.move(origin)
        
        client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
        client.move(point_1)

        client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
        client.servo(angle_close)

        time.sleep(1)

        sequence_num += 1
        status_box_frame_1.update_status_box_text(sequence_num)
        self.shoot_and_get(1, file_names)

        sequence_num += 1
        status_box_frame_1.update_status_box_text(sequence_num)
        self.shoot_and_get(2, file_names)

        sequence_num += 1
        status_box_frame_1.update_status_box_text(sequence_num)
        client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
        client.move(point_2)

        sequence_num += 1
        status_box_frame_1.update_status_box_text(sequence_num)
        self.shoot_and_get(3, file_names)

        sequence_num += 1
        status_box_frame_1.update_status_box_text(sequence_num)
        self.shoot_and_get(4, file_names)

        client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
        client.servo(angle_open)

        sequence_num += 1
        status_box_frame_1.update_status_box_text(sequence_num)
        client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
        client.move('5')

        client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
        client.move(origin)
        sequence_num = 1
        status_box_frame_1.update_status_box_text(sequence_num)

        self.master.configure(bg='white smoke')

    def __init__(self, status_box_frame, picture_frame, master = None):

        self.status_box_frame_1 = status_box_frame
        self.picture_frame_1 = picture_frame

        tk.Frame.__init__(self, master)
        self.master = master

        # フレームの作成
        self.frame_input = ttk.Frame(self.master, padding=16, borderwidth=1, relief="ridge")

        #品種コンボボックス
        svar_veriety = StringVar
        self.cbox_variety = ttk.Combobox(self.frame_input, textvariable=svar_veriety, values=self.variety, width=10, state="readonly")
        self.cbox_variety.set(self.variety[0])

        # 等級コンボボックス
        svar_grade = StringVar
        self.cbox_grade = ttk.Combobox(self.frame_input, textvariable=svar_grade, values=self.grade, width=10, state="readonly")
        self.cbox_grade.set(self.grade[0])

        # サイズコンボボックス
        svar_size = StringVar
        self.cbox_size = ttk.Combobox(self.frame_input, textvariable=svar_size, values=self.size, width=10, state="readonly")
        self.cbox_size.set(self.size[0])

        # 撮影実行ボタン
        self.button_run = ttk.Button(self.frame_input, text='撮影', command=lambda: self.function_run())
        self.button_run.bind("<Return>", lambda event:self.function_run())

        # レイアウト
        self.frame_input.grid(row=0, column=0, columnspan=2, padx=frame_around_pixel, pady=frame_around_pixel)
        self.cbox_variety.pack(side=LEFT)
        self.cbox_grade.pack(side=LEFT)
        self.cbox_size.pack(side=LEFT)
        self.button_run.pack(side=LEFT)

class picture_frame(tk.Frame):

    preview_w_size = int(4056/16)
    preview_h_size = int(3040/16)
    img = [None, None, None, None]
    canvas = [None, None, None, None]
    rotate_angle = [90, 0, 270, 0]
    label_name = [None, None, None, None]

    cam_R = 0
    cam_B = 1
    cam_L = 2
    cam_T = 3

    picture_update_en = [False, False, False, False]
    last_time_no_image = [False, False, False, False]
    display_picture_serial = 0

    # view_picture_names = ["preview_R.jpeg", "preview_B.jpeg", "preview_L.jpeg", "preview_T.jpeg"]
    view_picture_names = ["", "", "", ""]
    no_image_file_name = "no_image.png"

    # タイマー処理 作成中
    def time_event(self):
        thread = threading.Thread(target=self.update_picture)
        thread.start()
        self.after(100, self.time_event)

    def update_picture(self):

        # カレントディレクトリ取得
        directory = os.path.dirname(os.path.abspath(__file__))
        directory = directory + "\\picture\\"

        for i in range(4):

            no_image = False

            if self.picture_update_en[i] == True:

                # 画像用意
                try:
                    open_image = Image.open(directory + self.view_picture_names[i])
                except:
                    open_image = Image.open(directory + self.no_image_file_name)
                    no_image = True

                # 更新の有無
                if no_image == True:
                    if self.last_time_no_image[i] == True:
                        continue
                    else:
                        self.last_time_no_image[i] = True
                else:
                    self.last_time_no_image[i] = False
                    self.picture_update_en[i] = False

                self.img[i] = open_image
                self.img[i] = self.img[i].resize((self.preview_w_size, self.preview_h_size))
                self.img[i] = self.img[i].rotate(self.rotate_angle[i], expand=True)
                self.img[i] = ImageTk.PhotoImage(self.img[i])

                # 画像表示
                self.canvas[i].create_image(0, 0, image=self.img[i], anchor=tk.NW)

    def __init__(self, master=None):

        self.master = master
        tk.Frame.__init__(self, master)

        # フレーム生成
        frame_picture = ttk.Frame(self.master, padding=16, borderwidth=1, relief="ridge")
        frame_picture.grid(row=1, column=0, padx=frame_around_pixel, pady=frame_around_pixel)

        # canvas生成
        for i in range(4):

            if i==self.cam_R or i==self.cam_L:
                self.canvas[i] = tk.Canvas(frame_picture, width=self.preview_h_size, height=self.preview_w_size)    
            else:
                self.canvas[i] = tk.Canvas(frame_picture, width=self.preview_w_size, height=self.preview_h_size)

        self.view_picture_name = tk.StringVar()
        # self.view_picture_name.set("eee")
        self.label_name = tk.Label(frame_picture, textvariable=self.view_picture_name)

        # 配置
        self.canvas[self.cam_R].grid(row=1, column=2, rowspan=2)
        self.canvas[self.cam_B].grid(row=2, column=1)
        self.canvas[self.cam_L].grid(row=1, column=0, rowspan=2)
        self.canvas[self.cam_T].grid(row=1, column=1)
        
        self.label_name.grid(row=0, column=0, columnspan=2)

        self.picture_update_en = [True, True, True, True]
        self.last_time_no_image = [False, False, False, False]
        self.update_picture()
        self.time_event()

class status_box_frame(tk.Frame):

    strings = [ "操作待ち",
                    "移動：撮影地点1",
                    "撮影：カメラ(右)",
                    "撮影：カメラ(下)",
                    "移動：撮影地点2",
                    "撮影：カメラ(上)",
                    "撮影：カメラ(左)",
                    "移動：初期位置"]

    def update_status_box_text(self, highlight_now):
        self.status_box.configure(state="normal")

        self.status_box.tag_remove('highlight', '0.0', 'end')
        self.status_box.tag_add('highlight', str(highlight_now)+'.0', str(highlight_now)+'.end')

        self.status_box.configure(state="disabled")

    def print_status_box_text(self):

        self.status_box.configure(state="normal")
        self.status_box.delete('1.0', 'end')

        for line in self.strings:
            self.status_box.insert('end', line+'\n')

        self.status_box.configure(state="disabled")

    # def add_line(self, text, bg):
    #     self.status_box.configure(state="normal")
    #     self.status_box.insert('end', text+'\n')
    #     self.status_box.configure(state="disabled")

    def __init__(self, master = None):

        self.master = master

        self.frame_status_box = ttk.Frame(self.master, padding=16, borderwidth=1, relief="ridge")
        self.frame_status_box.grid(row=1, column=1, padx=frame_around_pixel, pady=frame_around_pixel, sticky=(N, W, S, E))

        text = StringVar()
        self.status_box = Text(self.frame_status_box, height=20, width=20, state="disabled")
        self.status_box.grid(row=0, column=0, sticky=(N, W, S, E))

        # スクロールバー処理
        # self.scrollbar = ttk.Scrollbar(self.frame_status_box, orient=VERTICAL, command=self.status_box.yview)
        # self.status_box['yscrollcommand'] = self.scrollbar.set
        # self.scrollbar.grid(row=0, column=1, sticky=(N, S))

        # 背景色用タグ設定
        self.status_box.tag_config('runnning', background="salmon")
        self.status_box.tag_config('normal', background="white")

        self.print_status_box_text()

        self.status_box.tag_configure('highlight', background='salmon')
        self.status_box.tag_add('highlight', '1.0', '1.end')

class camera_frame(tk.Frame):

    # タイマー処理 作成中
    def time_event(self):
        thread = threading.Thread(target=self.status_check)
        thread.start()
        self.after(500, self.time_event)

    def status_check(self):
        client = cherry.SocketClient(cherry.ip[self.num-1], cherry.CAMERA_PORT)
        self.online = client.hello()
        if self.online == True:
            self.text_status.set('online')
            self.label_camera_status['bg'] = 'light blue'
            
            self.button_LED['state'] = 'normal'
            self.button_preview['state'] = 'normal'
        else:
            self.text_status.set('offline')
            self.label_camera_status['bg'] = 'gray40'

            self.button_LED['state'] = 'disable'
            self.button_preview['state'] = 'disable'

    def LED_button_function(self):
        if self.text_LED_state.get()=='LED：OFF':
            self.text_LED_state.set('LED：ON')
            client = cherry.SocketClient(cherry.ip[self.num-1], cherry.CAMERA_PORT)
            client.led('ON')
        else:
            self.text_LED_state.set('LED：OFF')
            client = cherry.SocketClient(cherry.ip[self.num-1], cherry.CAMERA_PORT)
            client.led('OFF')

    def preview_button_function(self):
        client = cherry.SocketClient(cherry.ip[self.num-1], cherry.PREVIEW_PORT)
        client.preview(self.num)

    def __init__(self, text, master=None):

        self.master = master
        tk.Frame.__init__(self, master)

        widget_width = 8

        self.num=int(text[0])

        # フレーム生成
        self.frame_camera = ttk.Frame(self.master, padding=16, borderwidth=1, relief="ridge")
        # self.frame_camera.pack(side=LEFT, padx=frame_around_pixel, pady=frame_around_pixel)
        self.frame_camera.grid(row=0, column=self.num-1, padx=frame_around_pixel, pady=frame_around_pixel)
        
        self.label_camera_name = tk.Label(self.frame_camera, text = "Cherry Pi "+text)

        self.text_status = StringVar(self.frame_camera)
        self.text_status.set('offline')
        self.label_camera_status = tk.Label(self.frame_camera, textvariable=self.text_status, bg='gray40')
        
        self.text_LED_state = StringVar(self.frame_camera)
        self.text_LED_state.set('LED：OFF')
        self.button_LED = tk.Button(self.frame_camera, textvariable=self.text_LED_state, width=widget_width, command=lambda: self.LED_button_function())
        self.button_preview = tk.Button(self.frame_camera, text='preview', width=widget_width, command=lambda: self.preview_button_function())
        
        self.label_camera_name.pack()
        self.label_camera_status.pack()
        self.button_LED.pack()
        self.button_preview.pack()

        self.time_event()

class slider_frame(tk.Frame):

    def update_position():
        pass

    def origin(self):
        client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
        client.move('0')

    def move(self):
        distance = self.tbox_distance.get()
        try:
            distance = int(distance)
        except:
            return
        # print(distance)
        client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
        client.move(distance)

    def __init__(self, master=None):

        self.master = master

        widget_width = 8

        # フレーム生成
        self.frame_slider = ttk.Frame(self.master, padding=16, borderwidth=1, relief="ridge")
        # self.frame_slider.pack(side=BOTTOM, padx=frame_around_pixel, pady=frame_around_pixel)
        self.frame_slider.grid(row=1, column=0, columnspan=2, padx=frame_around_pixel, pady=frame_around_pixel)
        
        self.label_name = tk.Label(self.frame_slider, text = "Slider")
        self.label_distance = tk.Label(self.frame_slider, text="distance")
        self.label_position = tk.Label(self.frame_slider, text="position")
        
        self.button_origin = tk.Button(self.frame_slider, text='origin', width=widget_width, command=lambda: self.origin())
        self.button_move = tk.Button(self.frame_slider, text='move', width=widget_width, command=lambda: self.move())

        self.tbox_distance = tk.Entry(self.frame_slider, width=20)
        
        self.label_name.grid(row=0, column=0, columnspan=2)
        self.label_position.grid(row=1, column=0)
        self.button_origin.grid(row=1, column=1)
        self.tbox_distance.grid(row=2, column=0)
        self.button_move.grid(row=2, column=1)

class hatch_frame(tk.Frame):

    angle_open = 90
    angle_close = -20

    def hatch_button_function(self):
        if self.text_hatch_state.get()=='hatch：close':
            self.text_hatch_state.set('hatch：open')
            client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
            client.servo(self.angle_open)
        else:
            self.text_hatch_state.set('hatch：close')
            client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
            client.servo(self.angle_close)

    def __init__(self, master=None):

        self.master = master

        widget_width = 10

        # フレーム生成
        self.frame_hatch = ttk.Frame(self.master, padding=16, borderwidth=1, relief="ridge")
        # self.frame_hatch.pack(side=LEFT, padx=frame_around_pixel, pady=frame_around_pixel)
        self.frame_hatch.grid(row=1, column=2, padx=frame_around_pixel, pady=frame_around_pixel)
        

        self.hatch_name = tk.Label(self.frame_hatch, text = "hatch")
        
        self.text_hatch_state = StringVar(self.frame_hatch)
        self.text_hatch_state.set('hatch：close')
        
        self.button_hatch = tk.Button(self.frame_hatch, textvariable=self.text_hatch_state, width=widget_width, command=lambda: self.hatch_button_function())
        
        self.hatch_name.pack()
        self.button_hatch.pack()

def open_manual_operation():
    sub_win = tk.Toplevel()
    sub_win.title("マニュアル操作")
    cherry_pi_1 = camera_frame("1 (R)", master=sub_win)
    cherry_pi_2 = camera_frame("2 (B)", master=sub_win)
    cherry_pi_3 = camera_frame("3 (L)", master=sub_win)
    cherry_pi_4 = camera_frame("4 (T)", master=sub_win)
    slider = slider_frame(master=sub_win)
    hatch = hatch_frame(sub_win)
    sub_win.grab_set()

def open_shutdown_dialog():
    sub_win = tk.Toplevel()
    sub_win.title("シャットダウン")
    sub_win.grab_set()
    message = tk.StringVar()
    label_message = tk.Label(sub_win, textvariable=message, padx=30, pady=30)
    label_message.pack()
    message.set("シャットダウン完了までお待ち下さい")

    angle_open = 90
    client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
    client.servo(angle_open)

    client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
    client.move(0)

    client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
    client.move(100)

    client = cherry.SocketClient(cherry.ip_1, cherry.SLIDER_PORT)
    client.servo(-20)

    for i in range(4):
        client = cherry.SocketClient(cherry.ip[i], cherry.CAMERA_PORT)
        client.shutdown()

    sub_win.after(30000, message.set, "電源を切って終了してください")

font_size = 14

root = Tk()
default_font = tk.font.nametofont("TkDefaultFont")
default_font.configure(size=font_size)
text_font = tk.font.nametofont("TkTextFont")
text_font.configure(size=font_size)
fixed_font = tk.font.nametofont("TkFixedFont")
fixed_font.configure(size=font_size)
root.title('Cherry Photographer')

status_box_frame_1 = status_box_frame(master=root)
picture_frame_1 = picture_frame(master=root)
control_frame_1 = control_frame(status_box_frame_1, picture_frame_1, master=root)

# メニュー
men = tk.Menu(root)
root.config(menu=men)
menu_operation = tk.Menu(root)
men.add_cascade(label='操作', menu=menu_operation)
menu_operation.add_command(label='マニュアル操作', command=open_manual_operation)
menu_operation.add_command(label='', command=None)
menu_operation.add_command(label='', command=None)
menu_operation.add_command(label='シャットダウン', command=open_shutdown_dialog)

# ウィンドウの表示開始
root.mainloop()