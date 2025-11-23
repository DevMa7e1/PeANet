from flask import Flask, request, redirect
import os
import requests
import random
import rsa
import string

app = Flask(__name__)

f = open("template.html")
template = f.read()
f.close()

def get_posts():
    posts = []
    for i in os.listdir("./publ"):
        ip = i.removesuffix(".rsa")
        r = requests.get("http://" + ip + ":8333/l5p")
        u = requests.get("http://" + ip + ":8333/info")
        if r.status_code == 200 and u.status_code == 200:
            for j in r.text.split(chr(27)):
                if j != "":
                    posts.append((u.text, j))
    ret = []
    while len(ret) < posts:
        j = random.choice(posts)
        ret.append(j)
        posts.remove(j)
    return ret

def process_posts(posts):
    ret = ""
    for i in posts:
        ret += f'<div class="post"><p>{i[0]}</p><p>{i[1]}</p></div>\n'
    return ret

def check_ip(ip):
    if os.path.exists(f"./publ/{ip}.rsa"):
        f = open(f"./publ/{ip}.rsa")
        pubk = rsa.PublicKey.load_pkcs1(f.read())
        ts = (random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)).encode("Latin-1")
        r = requests.post("http://"+ip+":8333/ch", {"byts":rsa.encrypt(ts, pubk).decode("Latin-1")})
        if r.text == ts.decode():
            return True
    return False

@app.route("/")
def root():
    return template + process_posts(get_posts()) + "</body></html>"
@app.route("/add")
def add_someone():
    ip = request.args.get("ip")
    f = open(f"./publ/{ip}.rsa", 'wb')
    r = requests.get("http://"+ip+":8333/")
    f.write(r.text.encode("Latin-1"))
    return "SUCCESS"
@app.route("/post", methods=["POST"])
def make_a_post():
    f = open("posts", 'w')

app.run('0.0.0.0', 7444)