
from Cryptodome.Cipher import AES

import socket


Kprim = b'1122334455667788'
initializationVector = b'0099887766554433'

PORT = 65433
HOST= '127.0.0.1'




def receivefromA(conn):
    opMode = conn.recv(3).decode('utf-8')  #primeste modul de operare de la A
    Key = conn.recv(16)   #primeste cheia
    decipher = AES.new(Kprim, AES.MODE_ECB)
    Key = decipher.decrypt(Key) #decripteaza cheia primita de la A cu cheia K'
    conn.send('Success'.encode('utf-8')) #ii trimite lui A mesajul de incepere a comunicarii



    block=conn.recv(16)
    plain=""
    while block:

        if opMode == 'ECB':
            cipher = AES.new(Key, AES.MODE_ECB)
            plain=plain+cipher.decrypt(block).decode('utf-8')


        else:
            cipher = AES.new(Key, AES.MODE_CFB, initializationVector)
            plain = plain + cipher.decrypt(block).decode('utf-8')

        block = conn.recv(16)
    print(plain)

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen()
    conn, addr = server.accept()
    receivefromA(conn)

if __name__ == '__main__':
    start()