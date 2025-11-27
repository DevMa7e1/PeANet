# PeANet
### Personal Access Network
Simple social network with no central servers. Absolutely everything is hosted by users. This means complete access to your data, who can access it and how. Edit or delete posts at will, change your username anytime you want, etc.

## How it works
Your node communicates with the outside world through port 8333, controlled by main.py. PeANet's interface (from which you can make posts and see others' posts) is hosted on port 7444, controlled by interface.py.
### WARNING
If you want to set up your node to communicate outside your local network **only port-forward port 8333!!!** 
### Inner functioning
Stuff that is stored locally (on your node):
* Posts and replies (your posts dissappear when your node goes offline)
* Friend list (your friends' nodes IPs)
* Username
* Public and private RSA keys (used for identity verification)
* Last access time

Where it is stored (in the order above):
* ./posts
* ./publ/
* ./info
* pub.rsa and pri.rsa
* ./last

### Posts file structure
Posts are stored in this format:
* time of creation 
* characted 0x17
* post text content
* character 0x17
* post id
* character 0x1B

Replies are stored in a slightly different format:
* time of creation 
* characted 0x17
* reply text content
* character 0x17
* reply id
* character 0x17
* OG post/reply id
* character 0x1B
### Other files' functions
#### info
This file stores your username. Edit this file to change your username.
#### ipaddr
This file stores your IP address. 

For some reason, my ISP sends my outgoing internet trafic through one IP address through which multiple homes connect through. As a concequence, my router shows me a different IP than a website like whatismyip.com. I can contact my port forwarded servers only through the IP showed by my router. Because of this issue, PeANet can't automatically detect IP address changes and update the ipaddr file.

When you spot that your IP has changed, you can simply delete the ipaddr file and main.py will ask you for your new IP address. Doing this will also make main.py automatically broadcast that your IP has changed to its known friend nodes.
#### last
This file stores the Unix time for when you last requested / from interface.py. This file has no format, it is stored in cleartext.
### Routes
#### For port 8333
* / **[GET]** -> returns public key
* /p **[POST]**-> takes in ip, returns the user's posts if identity is successfully validated
* /info **[GET]** -> returns username
* /ipcb **[POST]** -> takes in nip (new IP). If identity validation is successful, it updates that node's IP and returns PROCEDURE FINISHED. If something went wrong, it returns ILLEGAL REQUEST. It will also return PROCEDURE FINISHED if node doesn't exist in the local database.
* /last **[POST]** -> takes in ip, returns the user's last access time if identity is successfully validated
#### For port 7444
* / **[GET]** -> main page
* /add **[POST]** -> adds a new node (accessed through /static/addpr.html)
* /post **[POST]** -> makes a new post (accessed through /static/post.html)
* /edit **[POST]** -> edits a post (accessed through /static/edit.html)
* /del **[GET]** -> deletes a post, takes in argument text (post's ID)
* /view_all **[GET]** -> returns interface for seeing all your posts. From here you can also edit and delete posts.
* /reply **[POST]** -> makes a new reply (accessed through /static/reply.html)
* /favicon.ico **[GET]** -> returns PeANet's logo's contents. Exists because of how browsers request the favicon.
