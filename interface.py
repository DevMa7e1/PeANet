from flask import Flask, request, redirect
import os
import requests
import random
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
    f = open("posts")
    r = f.read()
    f.close()
    posts = []
    u = "Me"
    for j in r.split(chr(27)):
        if j != "":
            if len(j.split(chr(23))) == 3:
                posts.append([html.escape(u), html.escape(j).replace("\n", "<br>").split(chr(23))[1], j.split(chr(23))[0], j.split(chr(23))[2]])
            else:
                posts.append([html.escape(u), html.escape(j).replace("\n", "<br>").split(chr(23))[1], j.split(chr(23))[0], j.split(chr(23))[2], j.split(chr(23))[3]])
    for i in os.listdir("./publ"):
        ip = i.removesuffix(".rsa")
        try:
            f = open("ipaddr")
            ipaddr = f.read()
            f.close()
            r = requests.post("http://" + ip + ":8333/p", {"ip": ipaddr})
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
    ret = []
    for i in posts:
        if len(i) == 4:
            ret.append([i])
        else:
            for j in ret:
                if len(j) > 1:
                    for a in j:
                        if type(a[0]) == list:
                            if i[4] == a[0][3]:
                                a.append([i])
                else:
                    if type(j[0]) == list:
                        if i[4] == j[0][3]:
                            j.append([i])
    return reverse(ret)

def process_posts(posts):
    ret = ""
    for i in posts:
        if len(i) < 2:
            ret += f'<div class="post"><div class="minc"><p class="unm">-- {i[0][0]} --</p><div><p class="mini">{i[0][2]}</p><p class="mini">{i[0][3]}</p></div></div><p>{i[0][1]}</p><a href="/static/reply.html?id={i[0][3]}"><span class="material-symbols-outlined">add_comment</span></a></div><br>\n'
        else:
            for a in i:
                if type(a[0]) == list:
                    if len(a) < 2:
                        ret += f'<div class="post" style="margin-left: 30px"><div class="minc"><p class="unm">-- {a[0][0]} --</p><div><p class="mini">{a[0][2]}</p><p class="mini">{a[0][3]}</p></div></div><p>{a[0][1]}</p><a href="/static/reply.html?id={a[0][3]}"><span class="material-symbols-outlined">add_comment</span></a></div><br>\n'
                    else:
                        ret += f'<div class="post" style="margin-left: 30px"><div class="minc"><p class="unm">-- {a[0][0]} --</p><div><p class="mini">{a[0][2]}</p><p class="mini">{a[0][3]}</p></div></div><p>{a[0][1]}</p><a href="/static/reply.html?id={a[0][3]}"><span class="material-symbols-outlined">add_comment</span></a></div><br>\n'
                        for b in a:
                            if type(b[0]) == list:
                                ret += f'<div class="post" style="margin-left: 60px"><div class="minc"><p class="unm">-- {b[0][0]} --</p><div><p class="mini">{b[0][2]}</p><p class="mini">{b[0][3]}</p></div></div><p>{b[0][1]}</p><a href="/static/reply.html?id={b[0][3]}"><span class="material-symbols-outlined">add_comment</span></a></div><br>\n'
                else:
                    ret += f'<div class="post"><div class="minc"><p class="unm">-- {a[0]} --</p><div><p class="mini">{a[2]}</p><p class="mini">{a[3]}</p></div></div><p>{a[1]}</p><a href="/static/reply.html?id={a[3]}"><span class="material-symbols-outlined">add_comment</span></a></div><br>\n'
                
    return ret

@app.route("/")
def root():
    return template + '' + process_posts(get_posts()) + "</body></html>"
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
        if i != "":
            if i.split(chr(23))[2] == old:
                r = r.replace(i+chr(27), str(time.time())+chr(23)+text+chr(23)+i.split(chr(23),2)[2]+chr(27))
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
        if i.split(chr(23))[1] == text:
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
    ret = template + '<h1 style="font-size: 50px; font-weight: 600;">My posts</h1>'
    for l in range(len(r)):
        i = r[len(r)-l-1]
        if len(i.split(chr(23))) == 3:
            ret += f'<div class="post"><p>{i.split(chr(23))[1].replace("\n", "<br>")}</p><a href="/static/edit.html?text={i.split(chr(23))[2]}"><button>Edit</button></a><a href="/del?text={i.split(chr(23))[2]}"><button>Delete</button></a></div>'
        else:
            ret += f'<div class="post"><p class="unm">*Reply*</p><p>{i.split(chr(23))[1].replace("\n", "<br>")}</p><a href="/static/edit.html?text={i.split(chr(23))[2]}"><button>Edit</button></a><a href="/del?text={i.split(chr(23))[2]}"><button>Delete</button></a></div>'
    return ret
@app.route("/reply", methods=["POST"])
def reply_to_a_post():
    idr = request.form.get("id")
    text = request.form.get("text")
    f = open("posts", 'a')
    id = ""
    for i in range(11):
        id += random.choice(string.ascii_letters)
    f.write(str(time.time())+chr(23)+text+chr(23)+id+chr(23)+idr+chr(27))
    f.close()
    return redirect("/")

@app.route("/favicon.ico")
def retur_favicon():
    f = open("favicon.ico", 'rb')
    r = f.read()
    return r
app.run('0.0.0.0', 7444)