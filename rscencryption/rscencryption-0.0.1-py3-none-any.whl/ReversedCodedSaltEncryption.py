def crypt(self, code):
	counter = 0
	text = ""
	for c in self:
		if ord(c) > (33 + 9) or ord(c) < 126:
			text += chr(ord(c) + int(str(code)[counter]))
			if counter + 1 >= len(str(code)):
				counter = 0
			else:
				counter += 1
	salt_text = ""
	j = len(text)
	for i in text:
		salt_text += i + text[j - 1]
		j -= 1
	return salt_text


def decrypt(self, code):
	text = ""
	j = 0
	while j < len(self):
		text += self[j]
		j += 2
	j -= 1
	while j > 0:
		text += self[j]
		j -= 2
	counter = 0
	decrypted_text = ""
	for c in text[:len(text) // 2]:
		if ord(c) > (33 + 9) or ord(c) < 126:
			decrypted_text += chr(ord(c) - int(str(code)[counter]))
			if counter + 1 >= len(str(code)):
				counter = 0
			else:
				counter += 1
	return decrypted_text
