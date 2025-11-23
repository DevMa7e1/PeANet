from flask import Flask, request
import rsa
import os
import requests
import random
import string
import pn_functions

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
else:
    f = open("pub.rsa", 'rb')
    pub = rsa.PublicKey.load_pkcs1(f.read())
    f.close()
    f = open("pri.rsa", 'rb')
    pri = rsa.PrivateKey.load_pkcs1(f.read())
    f.close()

app = Flask(__name__)

@app.route("/")
def root():
    return pub.save_pkcs1()
@app.route("/ch", methods=["POST"])
def challange():
    byts = request.form.get("byts").encode("Latin-1")
    return rsa.decrypt(byts, pri)
@app.route("/chk")
def check():
    ip = request.args.get("ip")
    if os.path.exists(f"./publ/{ip}.rsa"):
        f = open(f"./publ/{ip}.rsa")
        pubk = rsa.PublicKey.load_pkcs1(f.read())
        ts = (random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)).encode("Latin-1")
        r = requests.post("http://"+ip+":8333/ch", {"byts":rsa.encrypt(ts, pubk).decode("Latin-1")})
        print(ts, r.text)
        if r.text == ts.decode():
            return "SUCCESS"
        else:
            return "FAIL"
    else:
        return "FAIL"
@app.route("/add")
def add_someone():
    ip = request.args.get("ip")
    f = open(f"./publ/{ip}.rsa", 'wb')
    r = requests.get("http://"+ip+":8333/")
    f.write(r.text.encode("Latin-1"))
    return "SUCCESS"
@app.route("/l5p")
def get_last_5_posts():
    posts = pn_functions.ppf()
    ret = ""
    if len(posts) >= 5:
        for i in range(5):
            ret += posts[len(posts)-1-i]+chr(27)
    else:
        for i in range(len(posts)):
            ret += posts[len(posts)-1-i]+chr(27)
    return ret

app.run('0.0.0.0', 8333)