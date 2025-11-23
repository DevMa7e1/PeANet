from flask import Flask, request, redirect
import os
import requests
import random
import rsa
import string
import time

app = Flask(__name__)

f = open("template.html")
template = f.read()
f.close()

def get_posts():
    posts = []
    for i in os.listdir("./publ"):
        ip = i.removesuffix(".rsa")
        try:
            r = requests.get("http://" + ip + ":8333/l5p")
            u = requests.get("http://" + ip + ":8333/info")
            if r.status_code == 200 and u.status_code == 200:
                for j in r.text.split(chr(27)):
                    if j != "":
                        posts.append((u.text, j.replace("\n", "<br>")))
        except:
            pass
    ret = []
    while len(posts) > 0:
        j = random.choice(posts)
        ret.append(j)
        posts.remove(j)
    return ret

def process_posts(posts):
    ret = ""
    for i in posts:
        ret += f'<div class="post"><p>-- {i[0]} --</p><p>{i[1]}</p></div>\n'
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
    return template + '<a href="/view_all"><button>View my posts</button></a>' + process_posts(get_posts()) + "</body></html>"
@app.route("/add")
def add_someone():
    ip = request.args.get("ip")
    f = open(f"./publ/{ip}.rsa", 'wb')
    r = requests.get("http://"+ip+":8333/")
    f.write(r.text.encode("Latin-1"))
    return "SUCCESS"
@app.route("/post", methods=["POST"])
def make_a_post():
    text = request.form.get("text")
    f = open("posts", 'a')
    f.write(str(time.time())+chr(23)+text+chr(27))
    f.close()
    return redirect("/")
@app.route("/edit", methods=["POST"])
def edit_a_post():
    text = request.form.get("text")
    old = request.form.get("old")
    f = open("posts", 'r')
    r = f.read()
    f.close()
    for i in r.split(chr(27)):
        if i.split(chr(23))[0] == old:
            r = r.replace(i+chr(27), str(time.time())+chr(23)+text+chr(27))
    f = open("posts", 'w')
    f.write(r)
    f.close()
    return redirect("/")
@app.route("/del")
def delete_a_post():
    text = request.args.get("text")
    f = open("posts")
    r = f.read()
    f.close()
    for i in r.split(chr(27)):
        if i.split(chr(23))[0] == text:
            r = r.replace(i+chr(27), "")
    f = open("posts", 'w')
    f.write(r)
    f.close()
    return redirect("/")
@app.route("/view_all")
def view_all_my_posts():
    f = open("posts")
    r = f.read().split(chr(27))
    r.remove("")
    ret = template
    for i in r:
        ret += f'<div class="post"><p>{i.split(chr(23))[1].replace("\n", "<br>")}</p><a href="/static/edit.html?text={i.split(chr(23))[0]}"><button>Edit</button></a><a href="/del?text={i.split(chr(23))[0]}"><button>Delete</button></a></div>'
    return ret
@app.route("/favicon.ico")
def retur_favicon():
    f = open("favicon.ico", 'rb')
    r = f.read()
    return r

app.run('0.0.0.0', 7444)