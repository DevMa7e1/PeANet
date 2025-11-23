def ppf():
    f = open("posts")
    r = f.read().split("\n")
    f.close()
    for i in range(len(r)):
        r[i] = r[i].replace(chr(27), '\n')
    return r