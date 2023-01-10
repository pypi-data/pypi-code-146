import unittest
import random
from .ByteTools import ByteTools


class ARC4:

	# based on https://github.com/bozhu/RC4-Python

	@staticmethod
	def KSA(key):
		keylength = len(key)

		S = list(range(256))

		j = 0
		for i in range(256):
			j = (j + S[i] + key[i % keylength]) % 256
			S[i], S[j] = S[j], S[i]  # swap

		return S

	@staticmethod
	def PRGA(S):
		i = 0
		j = 0
		while True:
			i = (i + 1) % 256
			j = (j + S[i]) % 256
			S[i], S[j] = S[j], S[i]  # swap

			K = S[(S[i] + S[j]) % 256]
			yield K

	@staticmethod
	def keystream(key):
		return ARC4.PRGA(ARC4.KSA(key))

	@staticmethod
	def process(data, key):

		keystream = ARC4.keystream(key)

		new_data = bytearray(data)

		for index in range(len(data)):
			new_data[index] ^= next(keystream)

		return new_data


class FastEnc:

	# use python native functions to generate gamma & xor it

	@staticmethod
	def process(data, key):
		random.seed(key)
		key_int = random.getrandbits(8*len(data))
		data_int = ByteTools.bytes2int(data)
		return ByteTools.int2bytes(key_int ^ data_int, len(data))


############################################################
# UNIT TEST
############################################################
	

class Test_ARC4(unittest.TestCase):

	def test_process(self):

		self.assertEqual(ARC4.process(b'Plaintext', b'Key').hex().upper(), 'BBF316E8D940AF0AD3')
		self.assertEqual(ARC4.process(b'pedia', b'Wiki').hex().upper(), '1021BF0420')
		self.assertEqual(ARC4.process(b'Attack at dawn', b'Secret').hex().upper(), '45A01F645FC35B383552544B9BF5')


class Test_FastEnc(unittest.TestCase):

	def test_process(self):

		data = b'Plaintext'
		key = b'Key'

		encrypted = FastEnc.process(data, key)
		decrypted = FastEnc.process(encrypted, key)
		
		self.assertEqual(encrypted, b'\xa7\x8c\xd7\x1c\xf9B\xf1\xdaw')
		self.assertEqual(decrypted, data)

		
if __name__ == '__main__':
	
	unittest.main()
