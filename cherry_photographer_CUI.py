# https://www.raspberrypirulo.net/entry/socket-client

import socket
import time
from datetime import datetime
import os
import numpy  
import cv2  

# HOST_IP = "192.168.143.94" # 接続するサーバーのIPアドレス
CAMERA_PORT = 10000 # 接続するサーバーのポート
PREVIEW_PORT = 10001
SLIDER_PORT = 10002
DATESIZE = 1024  # 受信データバイト数

ip_1 = "192.168.143.94"
ip_2 = "192.168.143.95"
ip_3 = "192.168.143.96"
ip_4 = "192.168.143.97"
ip = [ip_1, ip_2, ip_3, ip_4]

point_1 = 140
point_2 = 220

class SocketClient():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def shoot(self, file_name):
        
        # sockインスタンスを生成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            # ソケットをオープンにして、サーバーに接続
            try:
                sock.connect((self.host, self.port))
            except:
                print('Error : Could not connect')
                return -1

            # 撮影命令送信
            send_text = 'shoot ' + file_name
            sock.send(send_text.encode('utf-8'))
            
            # 撮影完了待ち
            status_message = sock.recv(DATESIZE)
            print(status_message.decode('utf-8'))

            return 0

    def receive_picture(self, file_name):
        
        # sockインスタンスを生成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            # ソケットをオープンにして、サーバーに接続
            try:
                sock.connect((self.host, self.port))
            except:
                print('Error : Could not connect')
                return -1

            # ディレクトリ取得
            # file_name = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.jpg'
            path = os.path.dirname(os.path.abspath(__file__))
            directory = path + '/picture/'

            # 画像転送命令送信
            send_text = 'send ' + file_name
            sock.send(send_text.encode('utf-8'))
            
            # 画像受信
            # try:
            with open(directory + file_name, mode="ab") as f:

                while True:
                    data = sock.recv(DATESIZE)
                    if not data:
                        break
                    f.write(data)
                    sock.sendall(b'received done')
            print('receive done ' + directory + file_name)
        # except:
            # print('Data acquisition may not have been completed')

            return 0

    def preview(self, camera_num):
        while True:
            flg, img = self.getimage()
            if flg != 0:
                break
            cv2.imshow('camera ' + str(camera_num) + ' preview',img)  
            if cv2.waitKey(50) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def getimage(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # ソケットをオープンにして、サーバーに接続
        try:
            sock.connect((self.host, self.port))
        except:
            print('Error : Could not connect')
            return -1, None
        sock.send(('preview').encode("utf-8"))  
        buf=b''
        recvlen=100  
        while recvlen>0:  
            receivedstr=sock.recv(1024)  
            recvlen=len(receivedstr)  
            buf +=receivedstr
        sock.close()  
        narray=numpy.frombuffer(buf,dtype='uint8')  
        return 0, cv2.imdecode(narray,1)

    def move(self, distance):
        # sockインスタンスを生成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # ソケットをオープンにして、サーバーに接続
            sock.connect((self.host, self.port))
            # 撮影命令送信
            send_text = 'move_abs ' + str(distance)
            sock.send(send_text.encode('utf-8'))

            status_message = sock.recv(DATESIZE)
            print(status_message.decode('utf-8'))

    def led(self, onoff):
        # sockインスタンスを生成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # ソケットをオープンにして、サーバーに接続
            sock.connect((self.host, self.port))
            # 撮影命令送信
            send_text = 'LED ' + onoff
            sock.send(send_text.encode('utf-8'))

            status_message = sock.recv(DATESIZE)
            print(status_message.decode('utf-8'))

    def hello(self):

        try:
        # sockインスタンスを生成
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # ソケットをオープンにして、サーバーに接続
                sock.settimeout(0.2)
                sock.connect((self.host, self.port))
                # 撮影命令送信
                send_text = 'hello'
                sock.send(send_text.encode('utf-8'))

                status_message = sock.recv(DATESIZE)
                get_message = status_message.decode('utf-8')
                # print(get_message)
                
                if get_message == 'hello':
                    return True
        except:
            return False

    def servo(self, angle):
        # sockインスタンスを生成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # ソケットをオープンにして、サーバーに接続
            sock.connect((self.host, self.port))
            # 撮影命令送信
            send_text = 'servo ' + str(angle)
            sock.send(send_text.encode('utf-8'))

            status_message = sock.recv(DATESIZE)
            print(status_message.decode('utf-8'))

    def shutdown(self):
        # sockインスタンスを生成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # ソケットをオープンにして、サーバーに接続
            sock.connect((self.host, self.port))
            # 撮影命令送信
            send_text = 'shutdown'
            sock.send(send_text.encode('utf-8'))

    def reboot(self):
        # sockインスタンスを生成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # ソケットをオープンにして、サーバーに接続
            sock.connect((self.host, self.port))
            # 撮影命令送信
            send_text = 'reboot'
            sock.send(send_text.encode('utf-8'))

if __name__ == '__main__':

    # try:
    while True:
        HOST_IP = input("host ip:")
        input_data = input("command:") # ターミナルから入力された文字を取得
        
        input_datas = input_data.split()
        
        if len(input_datas) >= 2:
            command = input_datas[0]
            text = input_datas[1]
        else:
            command = input_data
            
        if command == 'shoot':
            client = SocketClient(HOST_IP, CAMERA_PORT)
            client.shoot(text)
        elif command == 'receive':
            client = SocketClient(HOST_IP, CAMERA_PORT)
            client.receive_picture(text)
        elif command == 'preview':
            client = SocketClient(HOST_IP, PREVIEW_PORT)
            client.preview(1)
        elif command == 'move':
            client = SocketClient(HOST_IP, SLIDER_PORT)
            client.move(text)
        elif command == 'LED':
            client = SocketClient(HOST_IP, CAMERA_PORT)
            client.led(text)
        elif command=='shutdown':
            client = SocketClient(HOST_IP, CAMERA_PORT)
            client.shutdown()
        elif command=='reboot':
            client = SocketClient(HOST_IP, CAMERA_PORT)
            client.reboot()
        elif command=='hello':
            client = SocketClient(HOST_IP, CAMERA_PORT)
            client.hello()
        # elif command == 'help':
        #     print()
        elif command == 'end()':
            break
        else:
            print('comand \"' + command + '\" is not prepared')

    # except:
    #     pass



