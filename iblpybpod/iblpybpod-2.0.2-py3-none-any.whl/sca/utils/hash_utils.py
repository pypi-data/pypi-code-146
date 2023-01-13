BUF_SIZE = 6553600

def calculate_hash(self, filepath):

    sha1 = hashlib.sha1()
    with open(filepath, 'rb') as f:
        data = f.read(BUF_SIZE)
        sha1.update(data)

    return os.path.basename(filepath), 'sha1(firsts {0} bytes)'.format(BUF_SIZE), sha1.hexdigest()