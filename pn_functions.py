import os
import requests
import rsa
import random
import string
import threading

def ppf():
    f = open("posts")
    r = f.read().split(chr(27))
    f.close()
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

def fire_and_forget(ip, nip):
    requests.post("http://"+ip+":8333/ipcb", {"nip": nip})

def broadcast_ip_change(nip):
    successes = 0
    for i in os.listdir("./publ"):
        ip = i.removesuffix(".rsa")
        threading.Thread(target=fire_and_forget, args=(ip, nip)).start()
    return successes