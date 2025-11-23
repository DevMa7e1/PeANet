import os
import requests
import rsa
import random
import string

def ppf():
    f = open("posts")
    r = f.read().split("\n")
    f.close()
    for i in range(len(r)):
        r[i] = r[i].replace(chr(27), '\n')
    return r

def check_ip(ip):
    if os.path.exists(f"./publ/{ip}.rsa"):
        f = open(f"./publ/{ip}.rsa")
        pubk = rsa.PublicKey.load_pkcs1(f.read())
        ts = (random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)).encode("Latin-1")
        r = requests.post("http://"+ip+":8333/ch", {"byts":rsa.encrypt(ts, pubk).decode("Latin-1")})
        if r.text == ts.decode():
            return True
    return False

def broadcast_ip_change():
    successes = 0
    for i in os.listdir("./publ"):
        ip = i.removesuffix(".rsa")
        r = requests.post("http://"+ip+"/ipcb", {"nip"})
        if "FINISHED" in r.text:
            successes += 1
    return successes