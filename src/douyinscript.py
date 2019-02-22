
# coding=utf-8

import csv
import cv2
import time
from monkeyrunner import monkeyrunner as mr

def template_match(sub_image, full_image, method = 'cv2.TM_CCOEFF'):
    sub_image_w, sub_image_h = sub_image.shape[::-1]
    img = full_image.copy()
    method = eval(method)

    res = cv2.matchTemplate(img, sub_image, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + sub_image_w, top_left[1] + sub_image_h)
    cv2.rectangle(img, top_left, bottom_right, 255, 2)
    ts = time.time()
    cv2.imwrite(str(ts) + ".png",img)

    center = [0,0]
    center[0] = (top_left[0] + bottom_right[0]) / 2
    center[1] = (top_left[1] + bottom_right[1]) / 2
    return center

def template_match2(sub_image_path, full_image_path):
    sub_image = cv2.imread(sub_image_path, 0)
    full_image = cv2.imread(full_image_path, 0)
    # 6 中匹配效果对比算法
    methods = [ 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED','cv2.TM_CCOEFF']
    center = []
    # for meth in methods:
    #     center = template_match(sub_image,full_image,meth)
    center = template_match(sub_image, full_image, 'cv2.TM_CCOEFF_NORMED')
    return center

device = mr.waitForConnection()
wm_size = device.wm_size()
header_loc = [wm_size[0],wm_size[1]]

def snapshot():
    device.takeSnapshot()

def tap(x,y,seconds = 1):
    device.touch(x,y)
    time.sleep(seconds)

def locate(sub_image_path,full_image_path = 'snapshot.png'):
    snapshot()
    tap_loc = template_match2(sub_image_path,full_image_path)
    print('位置：' + str(tap_loc[0]) + ',' + str(tap_loc[1]))
    return tap_loc

def run(short_id,unique_id, header_loc, search_result_loc = [0,0]):
    max_x = wm_size[0]*3.0/4.0
    min_y = wm_size[1]*1.0/5.0
    if(not (header_loc[0] > max_x and header_loc[1] < min_y)):
        header_loc = locate('.\\res\\locate_icon.png')
    tap(wm_size[0]/2,header_loc[1])

    if('0' == short_id):
        short_id = unique_id
    print('输入抖音号:' + str(short_id))
    device.type(short_id)
    time.sleep(1)

    print('点击搜索')
    tap(header_loc[0],header_loc[1],10)

    print('点击第一个搜索结果')
    max_x = wm_size[0]*2/3
    min_y = wm_size[1]*1/2
    if(not (search_result_loc[0] > max_x and search_result_loc[1] < min_y)):
        search_result_loc = locate('.\\res\\follower_button.png')
    tap(wm_size[0]/2,search_result_loc[1],5)

    print('点击关注')
    loc = locate('.\\res\\following.png')
    tap(loc[0],loc[1],10)

    while(True):
        print('向下滑动')
        device.drag(wm_size[0]/2, wm_size[1]*4/5, wm_size[0]/2, wm_size[1]/1/5, 500)
        time.sleep(2)
        loc = locate('.\\res\\no_more.png')
        max_x = wm_size[0] * 1 / 20
        dx = abs(loc[0] - wm_size[0]/2)
        if (dx < max_x):
            break

    print('点击返回')
    device.press('KEYCODE_BACK','DOWN_AND_UP')
    time.sleep(1)

    print('点击返回')
    device.press('KEYCODE_BACK','DOWN_AND_UP')
    time.sleep(1)

    print('点击返回')
    device.press('KEYCODE_BACK','DOWN_AND_UP')
    time.sleep(1)


print('点击HOME键')
device.press('KEYCODE_HOME','DOWN_AND_UP')
time.sleep(1)

print('启动抖音app')
device.startActivity(component='com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.splash.SplashActivity')
time.sleep(20)

print('点击返回')
device.press('KEYCODE_BACK','DOWN_AND_UP')
time.sleep(1)

print('向上滑动')
device.drag(wm_size[0]/2, wm_size[1]*4/5, wm_size[0]/2, wm_size[1]*3/5, 500)
time.sleep(1)

print('点击搜索按钮')
tap_loc = locate('.\\res\\search_icon.png')
tap(tap_loc[0],tap_loc[1],3)

print('寻找定位icon')
header_loc = locate('.\\res\\locate_icon.png')

data_path = 'F:\\duekiller\\2\\douyin\\douyin_data\\douyin-user_id=60002954951-total=130-nick_name=\'pumpkin\'.csv'
csv_file = csv.reader(open(data_path, 'r', encoding="utf-8"))
is_not_header = False
for x in csv_file:
    if(is_not_header):
        short_id = x[1]
        unique_id = x[2]
        run(short_id,unique_id, header_loc)
        time.sleep(1)
    else:
        is_not_header = True
print('点击返回')
device.press('KEYCODE_BACK','DOWN_AND_UP')
device.press('KEYCODE_BACK','DOWN_AND_UP')
device.press('KEYCODE_HOME','DOWN_AND_UP')
device.press('KEYCODE_HOME','DOWN_AND_UP')
time.sleep(1)



