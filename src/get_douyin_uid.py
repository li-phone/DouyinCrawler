
import json
import csv
import os

def get_user_info(followings):
    if('followings' not in followings.keys()):
        print('请求异常！')
        return []
    else:
        user_infos = []
        followings = followings['followings']
        for x in followings:
            uid = x['uid']
            short_id = x['short_id']
            unique_id = x['unique_id']
            nickname = x['nickname']
            user_info = [str(uid), str(short_id), str(unique_id), str(nickname)]
            # print(uid, short_id, unique_id, nickname)
            user_infos.append(user_info)
        return user_infos

def get_body(path):
    with open(path, "r", encoding="utf-8", newline="") as file:
        lines = ''
        while True:
            line = file.readline()  # 整行读取数据
            lines += line
            if not line:
                break
        return lines

def get_nick_name_from_uid(user_id,data_dir):
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if(-1 != file.find(user_id) and -1 != file.find('aweme_v1_aweme_post_body')):
                file_path = os.path.join(root, file)
                print('processing ' + file_path + '...')
                body = get_body(file_path)
                json_obj = json.loads(body)
                aweme_list = json_obj['aweme_list']
                author = aweme_list[0]['author']
                nickname = author['nickname']
                return nickname



def fetch_body(body_path,save_base_path = '',user_id = '',nick_name=''):
    lines = get_body(body_path)
    followings = json.loads(lines)

    total = 'total='+str(followings['total'])
    save_path = os.path.join(save_base_path, 'douyin-' + user_id + '-' + total + '-' + nick_name + '.csv')
    followings_lists = []
    followings_lists.append(get_user_info(followings))

    if(not os.path.exists(save_path)):
        with open(save_path, "a", encoding="utf-8", newline="") as f:
            k = csv.writer(f, dialect="excel")
            k.writerow(["uid", "short_id", "unique_id", "nickname"])

    with open(save_path, "a", encoding="utf-8", newline="") as f:
        k = csv.writer(f, dialect="excel")
        for xx in followings_lists:
            for x in xx:
                k.writerow(x)
        print('processed ' + body_path + ' OK！')

if __name__ == '__main__':
    data_dir = '.\\data'
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if(-1 != file.find('aweme_v1_user_following_list_body')):
                file_str = file
                user_id = file_str.split('-')[0]
                file_path = os.path.join(root, file)
                print('processing ' + file_path + '...')
                try:
                    nick_name = 'nick_name=\'' + get_nick_name_from_uid(user_id,data_dir) + '\''
                    fetch_body(file_path,'.\\douyin_data',user_id,nick_name)
                except:
                    print('fetch data error!')

