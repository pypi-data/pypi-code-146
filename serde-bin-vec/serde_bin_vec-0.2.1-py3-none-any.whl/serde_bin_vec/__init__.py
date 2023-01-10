__version__ = '0.2.1'
import struct


def save(uuid: str, vector: list[float], filename='data.bin'):
    f = open(filename, 'ab')
    f.write(struct.pack('I'*32, *[ord(c) for c in uuid]))
    data = [struct.pack('d', f) for f in vector]
    [f.write(d) for d in data]
    f.close()


def read_all(filename='data.bin'):
    f = open(filename, 'rb')
    output = []
    Is = 'I'*32
    Ds = 'd'*512
    vec_len = 512*8
    while True:
        try:
            tmp = [''.join([chr(o) for o in struct.unpack(Is, f.read(128))]),
                   struct.unpack(Ds, f.read(vec_len))]
            output.append(tmp)
        except:
            break
    f.close()
    return output


def save_all(list_of_lists, filename='data.bin'):
    open(filename, 'a').write('')
    for item in list_of_lists:
        save(item[0], item[1], filename)
