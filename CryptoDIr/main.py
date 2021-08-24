#!/usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time


class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'script.py' and fname != 'data.txt.enc'):
                    dirs.append(dirName + "\\" + fname)
        return dirs

    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)


key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encryptor(key)
clear = lambda: os.system('cls')

if os.path.isfile('data.txt.enc'):
    while True:
        password = str(input("INPUT VALIDATION KEY : "))
        enc.decrypt_file("data.txt.enc")
        p = ''
        with open("data.txt", "r") as f:
            p = f.readlines()
        if p[0] == password:
            enc.encrypt_file("data.txt")
            break

    while True:
        clear()
        print('''
                
FUNCTIONS :
        ''')
        choice = int(input(
            '''1	: SPECIFIC FILE ENCRYPTION\n2	: SPECIFIC FILE DECRYPTION\n3	: ENCRYPT FILES OVER DIRECTORY\n4	: DECRYPT FILES OVER DIRECTORY\n
            
  INPUT MODE : '''))
        clear()
        if choice == 1:
            enc.encrypt_file(str(input("ASSIGN ENCRYPTION {FILE}: ")))
            print("FILE ENCRYPTION : ACCOMPLISHED")
        elif choice == 2:
            enc.decrypt_file(str(input("ASSIGN DECRYPTION {FILE}: ")))
            print("FILE DECRYPTION : ACCOMPLISHED")
        elif choice == 3:
            enc.encrypt_all_files()
            print("FILEs ENCRYPTION : ACCOMPLISHED")
        elif choice == 4:
            enc.decrypt_all_files()
            print("FILEs DECRYPTION : ACCOMPLISHED")
        elif choice == 0:
            exit()
        else:
            print(":INVALID ASSIGNMENT")

else:
    while True:
        clear()
        password = str(input("SETUP VALIDATION KEY  : "))
        repassword = str(input("CONFIRM VALIDATION    : "))
        if password == repassword:
            break
        else:
            print("VALIDATION KEYS NOT MATCHED")
    f = open("data.txt", "w+")
    f.write(password)
    f.close()
    enc.encrypt_file("data.txt")
    print("SETUP ACCOMPLISHED ッ")
    time.sleep(5)
