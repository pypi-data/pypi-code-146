#!python

import os
import socket
from datetime import datetime
from pprint import pprint

from codec.diameter.diameter import Diameter
from codec.diameter.dictionary import DictionaryLayout, DefaultDictionaryLayout


# address and port is arbitrary
def server():
    host = '127.0.0.1'
    port = 3868
    print(os.getcwd())
    xml_dict_path: str = f'{os.getcwd()}/../../../src/unittest/python/Diameter.xml'

    dictionary_layout: DictionaryLayout = DefaultDictionaryLayout(xml_dict_path)
    message: Diameter = Diameter(dictionary_layout)

    # create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        print("[+] Listening on {0}:{1}".format(host, port))
        sock.listen(5)
        # permit to access
        conn, address = sock.accept()

        with conn as c:
            # display the current time
            time = datetime.now().ctime()
            print("[+] Connecting by {0}:{1} ({2})".format(address[0], address[1], time))

            while True:
                request: bytes = c.recv(4096)

                if not request:
                    print("[-] Not Received")
                    break

                print("[+] Received", repr(request))

                pprint(message.decode(request))

                response = input("[+] Enter string : ")
                c.sendall(response.encode('utf-8'))
                print("[+] Sending to {0}:{1}".format(address[0], address[1]))


if __name__ == "__main__":
    server()
