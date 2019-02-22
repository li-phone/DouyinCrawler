
import time
import os

class device_operation(object):
    def __init__(self):
        self.device_name = 'android'

    def takeSnapshot(self, filename='snapshot.png'):
        cmd1 = 'adb shell /system/bin/screencap -p /sdcard/' + filename
        cmd2 = 'adb pull /sdcard/' + filename + ' ./' + filename
        output1 = os.popen(cmd1)
        time.sleep(5)
        output2 = os.popen(cmd2)
        time.sleep(3)

    def press(self, key_event, opt):
        cmd1 = 'adb shell input keyevent ' + key_event
        output1 = os.popen(cmd1)

    def startActivity(self, component):
        cmd1 = 'adb shell am start ' + component
        output1 = os.popen(cmd1)

    def drag(self, x1, y1, x2, y2, ts):
        cmd1 = 'adb shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' ' + str(ts) + ' '
        output1 = os.popen(cmd1)

    def touch(self, x1, y1):
        cmd1 = 'adb shell input tap ' + str(x1) + ' ' + str(y1)
        output1 = os.popen(cmd1)

    def type(self, text):
        cmd1 = 'adb shell input text ' + str(text)
        output1 = os.popen(cmd1)

    def wm_size(self):
        cmd1 = 'adb shell wm size'
        output1 = os.popen(cmd1)
        size_str = output1.read()
        arr = str(size_str).split(':')[1].split(' ')[1].split('\n')[0].split('x')
        size = [0,0]
        size[0] = (int)(arr[0])
        size[1] = (int)(arr[1])
        return size

def waitForConnection():
    return device_operation()

