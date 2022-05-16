import aiohttp
import asyncio

from bs4 import BeautifulSoup
import os

dir_path = "pic"
main_page = 'https://www.umei.cc'
url = 'https://www.umei.cc/e/action/get_img_a.php'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

if not os.path.isdir(dir_path):
    os.mkdir(dir_path)

all_pic_url = []
async def get_url(params_dict):
    async with aiohttp.ClientSession() as seccion:
        async with seccion.post(url,headers=headers,data=params_dict) as resp:
            pic_obj = BeautifulSoup(await resp.text(), 'html.parser')  #需要加个await
            ret = pic_obj.find_all('a')
            for uri in ret:
                # 获取uri以及图片的名称
                child_url = main_page + uri.get('href')
                child_name = uri.text

                # 请求图片详情页
                async with seccion.get(child_url, headers=headers) as child_ret:
                    child_ret.encoding = 'utf-8'

                    child_obj = BeautifulSoup(await child_ret.text(), 'html.parser')
                    # 获取最终图片地址
                    pic = child_obj.find('section', attrs={"class": "img-content"}).find('img').get('src')

                    all_pic_url.append(pic)

async def download_pic(url):
    async with aiohttp.ClientSession() as seccion:
        async with seccion.get(url,headers=headers) as get_resp:
            pic_name = url.rsplit('/',1)[-1]
            with open(os.path.join(dir_path,pic_name),mode='wb') as fw:
                fw.write(await get_resp.content.read())
                print(f'download {pic_name} done....')


async def main():
    tasks = []
    for num in range(100):
        params_dict = {
            "next": num,
            "table": "news",
            "action": "getmorenews",
            "limit": 10,
            "small_length": 120,
            "classid": 25
        }
        tasks.append(get_url(params_dict))
    await asyncio.wait(tasks)



async def aiodown_main():
    tasks = []
    for url in all_pic_url:
        tasks.append(download_pic(url))
    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    print('url downLoad ok。。。')
    asyncio.get_event_loop().run_until_complete(aiodown_main())
