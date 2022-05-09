import requests
from bs4 import BeautifulSoup
import time
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning


#关闭安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


dir_path = "/pic"
main_page = 'https://www.umei.cc'
url = 'https://www.umei.cc/e/action/get_img_a.php'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

if not os.path.isdir(dir_path):
    os.mkdir(dir_path)

num = 1
while 1:
    params_dict = {
        "next": num,
        "table": "news",
        "action": "getmorenews",
        "limit": 10,
        "small_length": 120,
        "classid": 25
    }
    try:

        ret = requests.post(url, headers=headers, data=params_dict, verify=False)
        if ret.status_code != 200:
            continue

        if "img src=" not in ret.text:
            break
        pic_obj = BeautifulSoup(ret.text, 'html.parser')
        ret = pic_obj.find_all('a')
        for uri in ret:
            # 获取uri以及图片的名称
            child_url = main_page + uri.get('href')
            child_name = uri.text

            # 请求图片详情页
            child_ret = requests.get(child_url, headers=headers, verify=False)
            child_ret.encoding = 'utf-8'

            child_obj = BeautifulSoup(child_ret.text, 'html.parser')
            # 获取最终图片地址
            pic = child_obj.find('section', attrs={"class": "img-content"}).find('img').get('src')

            pic_name = pic.split('/')[-1]

            # 获取图片
            pic_ret = requests.get(pic, headers=headers, verify=False)
            with open(os.path.join(dir_path, pic_name), mode='wb') as fw:
                fw.write(pic_ret.content)
                print(pic_name, ' ok')
    except:
        pass
    time.sleep(1)
    num += 1
