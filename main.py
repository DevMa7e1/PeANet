from flask import Flask, request
import rsa
import os
import pn_functions
import requests
import time

if not os.path.exists("pub.rsa"):
    print("First startup, generating keys...")
    pub, pri = rsa.newkeys(4096)
    print("Done")
    f = open("pub.rsa", 'wb')
    f.write(pub.save_pkcs1())
    f.close()
    f = open("pri.rsa", 'wb')
    f.write(pri.save_pkcs1())
    f.close()
    os.mkdir("publ")
    f = open("info", 'w')
    f.write(input("Username (you can change it later)>"))
    f.close()
    f = open("ipaddr", 'w')
    f.write(input("Please input your IP address>"))
    f.close()
    f = open("posts", 'x')
    f.close()
    f = open("last", 'w')
    f.write(str(time.time()))
    f.close()
else:
    f = open("pub.rsa", 'rb')
    pub = rsa.PublicKey.load_pkcs1(f.read())
    f.close()
    f = open("pri.rsa", 'rb')
    pri = rsa.PrivateKey.load_pkcs1(f.read())
    f.close()

if os.path.exists("ipaddr"):
    f = open("ipaddr")
    ipaddr = f.read()
    f.close()
else:
    ipaddr = input("Please input your IP address>")
    pn_functions.broadcast_ip_change(ipaddr)
    f = open("ipaddr", 'w')
    f.write(ipaddr)
    f.close()

app = Flask(__name__)

@app.route("/")
def root():
    return pub.save_pkcs1()
@app.route("/ch", methods=["POST"])
def challange():
    byts = request.form.get("byts").encode("Latin-1")
    return rsa.decrypt(byts, pri)
@app.route("/p", methods=["POST"])
def get_posts():
    ip = request.form.get("ip")
    ret = ""
    if os.path.exists(f"./publ/{ip}.rsa"):
        if pn_functions.check_ip(ip):
            posts = pn_functions.ppf()
            for i in posts:
                ret += i + chr(27)
    return ret
@app.route("/info")
def send_info():
    f = open("info")
    r = f.read()
    f.close()
    return r
@app.route("/ipcb", methods=["POST"])
def ip_changed():
    time.sleep(5)
    nip = request.form.get("nip")
    pubk = requests.get("http://"+nip+":8333/").text
    for i in os.listdir("./publ"):
        f = open("./publ/"+i)
        r = f.read()
        f.close()
        if r == pubk:
            f = open("./publ/"+nip+".rsa", 'w')
            f.write(pubk)
            f.close()
            if pn_functions.check_ip(nip):
                os.remove("./publ/"+i)
            else:
                return "ILLEGAL REQUEST"
    return "PROCEDURE FINISHED"
@app.route("/last", methods=["POST"])
def get_last_access_time():
    ip = request.form.get("ip")
    if pn_functions.check_ip(ip):
        f = open("last")
        r = f.read()
        f.close()
        return r
    return "0"

app.run('0.0.0.0', 8333)