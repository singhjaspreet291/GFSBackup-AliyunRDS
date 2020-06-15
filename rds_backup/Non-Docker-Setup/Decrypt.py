import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

#Encryption of files
class CustomEncDyc:
    def encrypt(key, filename):
        chunksize =64 * 1024
        outputFile = filename+'.enc'
        filesize = str(os.path.getsize(filename)).zfill(16)
        IV = Random.new().read(16)

        encryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(filename, 'rb') as infile:
            with open(outputFile, 'wb') as outfile:
                outfile.write(filesize.encode('utf-8'))
                outfile.write(IV)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk +=b' ' * (16 - (len(chunk) % 16))
                    outfile.write(encryptor.encrypt(chunk))

    #Decryption of files
    def decrypt(key, filename):
        chunksize =64 * 1024
        outputFile = filename[:-4]
        print(outputFile)
        
        with open(filename, 'rb') as infile:
            filesize = int(infile.read(16))
            IV = infile.read(16)

            decryptor = AES.new(key, AES.MODE_CBC, IV)

            with open(outputFile, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))
                    outfile.truncate(filesize)

    def getKey(password):
        hasher = SHA256.new(password.encode('utf-8'))
        return hasher.digest()
obj=CustomEncDyc
filename = input('File to decrypt: ')
password = input('Password: ')
obj.decrypt(obj.getKey(password), filename)
print('Done.')


    