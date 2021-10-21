import os
print("Hello %s! Your operation system is %s. Enjoy!" % (os.getlogin(), os.name))

def ping(ip_address):
    if os.system("ping %s" % ip_address) == 0:
        print("Command executed successfully!")


ping("127.0.0.1")

