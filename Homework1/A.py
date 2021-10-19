from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

import socket


Kprim = b'1122334455667788'
initializationVector = b'0099887766554433'

PORTk = 65432
PORTb = 65433


def receiveKey():
    keySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #cream un ob de tip socket
    keySocket.connect(('127.0.0.1', PORTk))  #ne conectam la key manager cu adresa si portul lui
    K = keySocket.recv(16)  #primim de la key maanger cheia k care este de 16 bytes
    keySocket.close()  #inchidem conexinea cu KM
    return K

def decryptKey(K):
    decipher = AES.new(Kprim, AES.MODE_ECB)  #cream un obiect de tip AES cu cheia  K' si modul de criptare ECB
    Key = decipher.decrypt(K) # decriptam cheia K primita de la KM

    return Key



def sendtoB(K, opMode):

    #decriptam cheia de la KM
    Key = decryptKey(K)


    B = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    B.connect(('127.0.0.1', PORTb))  #ne conectam la nodul b
    B.send(opMode.encode('utf-8')) #trimitem lui B modul de operare pe care il vrem ECB sau CFB (din string in bytes)
    B.send(K) #si trimitem si cheia

    message =  B.recv(7).decode('utf-8') #primim de la b semnalul de start success de lungime 7
    print(message)  #il afisam




    name=input("Path to file: ") #preluam pathul fisierului ce urmeaza sa l trimitem lui b
    f=open(name,'r')   #il deschidem in read mode


    #luam cate 16 bytes
    block=f.read(16)

    while block:
        block = block.encode()


        if opMode == "ECB":
            if len(block) < 16:  # adaugam padding daca lungimea blocului de text este sub 16
                block = pad(block, 16)
            cipher = AES.new(Key, AES.MODE_ECB)  # cipher AES pentru a cripta folosind ECB mode
            B.send(cipher.encrypt(block)) #crpitam folosind ECB
        elif opMode=='CFB':
            cipher = AES.new(Key, AES.MODE_CFB, initializationVector)  # cipher AES pentru a cripta folosind CFB mode
            #pentru CFB trebuie sa adaugam si vectorul de initializare
            B.send(cipher.encrypt(block))

        block = f.read(16) #preluam urmatorii 16 bytes

    B.close()  #inchidem conex cu B

def start():

    mode = ""

    while mode=="":
        inp = input("Choose CFB or ECB \n")
        if inp == 'ECB' or inp == 'CFB':
            mode=inp
        else:
            print("Invalid, type again")
   
    Key = receiveKey()  #preluam cheia de la km
    sendtoB(Key, mode)  #trimite lui b modul de operare, cheia si fisierul criptat

if __name__ == '__main__':
    start()