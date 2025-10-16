import math

def encrypt_vigenere(plaintext: str, keyword: str) -> str:
	"""
	Encrypts plaintext using a Vigenere cipher.
	>>> encrypt_vigenere("PYTHON", "A")
	'PYTHON'
	>>> encrypt_vigenere("python", "a")
	'python'
	>>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
	'LXFOPVEFRNHR'
	"""
	ciphertext = ""
	padded_key = keyword * math.ceil(len(plaintext) / len(keyword))
	padded_key = padded_key[:len(plaintext)]

	alphabet_start_index = ord('A')

	for text_symbol, key_symbol in zip(plaintext, padded_key):
		if text_symbol.isalpha():
			src_index = ord(text_symbol.upper()) - alphabet_start_index
			shift = ord(key_symbol.upper()) - alphabet_start_index
			enc_symbol = chr(alphabet_start_index + (src_index + shift) % 26)
			if text_symbol.islower():
				ciphertext += enc_symbol.lower()
			else:
				ciphertext += enc_symbol
		else:
			ciphertext += text_symbol
	return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
	"""
	Decrypts a ciphertext using a Vigenere cipher.
	>>> decrypt_vigenere("PYTHON", "A")
	'PYTHON'
	>>> decrypt_vigenere("python", "a")
	'python'
	>>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
	'ATTACKATDAWN'
	"""
	plaintext = ""
	padded_key = keyword * math.ceil(len(ciphertext) / len(keyword))
	padded_key = padded_key[:len(ciphertext)]

	alphabet_start_index = ord('A')

	for text_symbol, key_symbol in zip(ciphertext, padded_key):
		if text_symbol.isalpha():
			src_index = ord(text_symbol.upper()) - alphabet_start_index
			shift = ord(key_symbol.upper()) - alphabet_start_index
			enc_symbol = chr(alphabet_start_index + (src_index - shift) % 26)
			if text_symbol.islower():
				plaintext += enc_symbol.lower()
			else:
				plaintext += enc_symbol
		else:
			plaintext += text_symbol

	return plaintext
