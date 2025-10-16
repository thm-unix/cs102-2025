def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    alphabet_start_index = ord("A")
    for symbol in plaintext:
        if symbol.isalpha():
            src_index = ord(symbol.upper()) - alphabet_start_index
            enc_symbol = chr(alphabet_start_index + ((src_index + shift) % 26))
            if symbol.islower():
                ciphertext += enc_symbol.lower()
            else:
                ciphertext += enc_symbol
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    alphabet_start_index = ord("A")
    for symbol in ciphertext:
        if symbol.isalpha():
            src_index = ord(symbol.upper()) - alphabet_start_index
            enc_symbol = chr(alphabet_start_index + ((src_index - shift) % 26))
            if symbol.islower():
                plaintext += enc_symbol.lower()
            else:
                plaintext += enc_symbol
        else:
            plaintext += symbol
    return plaintext
