import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import board
dir(board)
import busio
import gpiod
import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16,address=0x40)
kit1=ServoKit(channels=16,address=0x41)
host_name = '192.168.142.198'  
host_port = 8000


def getTemperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    return temp


class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
           <html>
           <body 
            style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <p>Current GPU temperature is {}</p>
           <form action="/" method="POST">
               Turn LED :
               <input type="submit" name="submit" value="shake">
	           <input type="submit" name="submit" value="open">
               <input type="submit" name="submit" value="close">
           </form>
           </body>
           </html>
        '''
        temp = getTemperature()
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:]).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]
        if post_data == 'shake':
            print("shake")
            kit.servo[14].angle=0
            time.sleep(1)
            kit.servo[14].angle=90
            kit.servo[12].angle=180
            time.sleep(1)
            kit.servo[12].angle=90
            kit.servo[0].angle=180
            kit.servo[1].angle=180
            kit.servo[2].angle=180
            kit.servo[3].angle=180
            kit.servo[4].angle=180
            time.sleep(2)
            kit.servo[0].angle=0
            kit.servo[1].angle=0
            kit.servo[2].angle=0
            kit.servo[3].angle=0
            kit.servo[4].angle=0
            time.sleep(1)
            kit.servo[14].angle=180
            time.sleep(1)
            kit.servo[14].angle=90
            time.sleep(1)
            kit.servo[12].angle=0
            time.sleep(1)
            kit.servo[12].angle=90
        if post_data == 'open':
            print("open") 
            kit1.servo[1].angle=0
        if post_data == 'close':
            print("close")
            kit1.servo[1].angle=180
        print("LED is {}".format(post_data))
        self._redirect('/')  


def start():
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))
    http_server.serve_forever()
