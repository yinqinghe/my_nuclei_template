import requests
import random
import json


class DnsLog():
    domain = ""
    token = ""
    Webserver = ""

    def __init__(self, Webserver, token):
        self.Webserver = Webserver  # dnslog的http监听地址，格式为 ip:端口
        self.token = token  # token
        # 检测DNSLog服务器是否正常
        try:
            res = requests.post("http://" + Webserver + "/api/verifyToken", json={"token": token}).json()
            print(res)
            self.domain = res['Msg']
        except:
            exit("DnsLog 服务器连接失败")
        if res["Msg"] == "false":
            exit("DnsLog token 验证失败")

    # 生成随机子域名
    def randomSubDomain(self, length=5):
        subDomain = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', length)) + '.' + self.domain
        return subDomain

    # 验证子域名是否存在
    def checkDomain(self, domain):
        print(domain)
        res = requests.post("http://" + self.Webserver + "/api/verifyDns", json={"Query": domain},
                            headers={"token": self.token}).json()
        print(res)
        if res["Msg"] == "false":
            return False
        else:
            return True


url = "http://47.236.109.211:8000/"

dns = DnsLog("47.236.109.211:8000", "mikejordan")

# subDomain = dns.randomSubDomain()
subDomain='mikes.mikes.mikejordan.cn'
if dns.checkDomain(subDomain):
    print("存在FastJosn")