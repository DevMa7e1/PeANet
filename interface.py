from flask import Flask, request, redirect
import os
import requests
import random
import rsa
import string
import time
import html

app = Flask(__name__)

f = open("template.html")
template = f.read()
f.close()

def reverse(lis):
    ret = []
    for i in range(len(lis)):
        ret.append(lis[len(lis)-1-i])
    return ret

def get_posts():
    posts = []
    for i in os.listdir("./publ"):
        ip = i.removesuffix(".rsa")
        try:
            r = requests.get("http://" + ip + ":8333/p")
            u = requests.get("http://" + ip + ":8333/info")
            if r.status_code == 200 and u.status_code == 200:
                for j in r.text.split(chr(27)):
                    if j != "":
                        if len(j.split(chr(23))) == 3:
                            posts.append([html.escape(u.text), html.escape(j).replace("\n", "<br>").split(chr(23))[1], j.split(chr(23))[0], j.split(chr(23))[2]])
                        else:
                            posts.append([html.escape(u.text), html.escape(j).replace("\n", "<br>").split(chr(23))[1], j.split(chr(23))[0], j.split(chr(23))[2], j.split(chr(23))[3]])
        except:
            pass
    n = len(posts)
    for i in range(n-1):
        for j in range(n-i-1):
            if float(posts[j][2]) > float(posts[j+1][2]):
                posts[j], posts[j+1] = posts[j+1], posts[j]
    return reverse(posts)

def process_posts(posts):
    ret = ""
    for i in posts:
        ret += f'<div class="post"><div class="minc"><p class="mini">{i[2]}</p></div><div class="minc"><p class="mini">{i[3]}</p></div><p>-- {i[0]} --</p><p>{i[1]}</p><a href="/static/reply.html?id={i[3]}"><button>Reply</button></a></div><br>\n'
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
    id = ""
    for i in range(11):
        id += random.choice(string.ascii_letters)
    f.write(str(time.time())+chr(23)+text+chr(23)+id+chr(27))
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
@app.route("/reply", methods=["POST"])
def reply_to_a_post():
    id = request.form.get("id")
    text = request.form.get("text")
    f = open("posts", 'a')
    id = ""
    for i in range(11):
        id += random.choice(string.ascii_letters)
    f.write(str(time.time())+chr(23)+text+chr(23)+id+chr(23)+id+chr(27))
    f.close()
    return redirect("/")

@app.route("/favicon.ico")
def retur_favicon():
    f = open("favicon.ico", 'rb')
    r = f.read()
    return r
app.run('0.0.0.0', 7444)