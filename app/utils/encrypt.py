from Crypto.Cipher import AES
import binascii


class EncriptarAES:
    """Simple wrapper AES-GCM encrypt/decrypt using a fixed secret key.

    Nota: esta clase sigue el algoritmo provisto en la petición. En producción
    deberías gestionar claves con más cuidado (no hardcodearlas) y usar
    mecanismos de rotación/almacenamiento seguro.
    """

    # clave fija de 16 bytes (AES-128)
    secretKey = b"4563265512345678"

    def Encriptar(self, valor: str) -> str:
        """Encripta la cadena y devuelve hex(ciphertext)|hex(nonce)|hex(tag)."""
        aesCipher = AES.new(self.secretKey, AES.MODE_GCM)
        ciphertext, authTag = aesCipher.encrypt_and_digest(str.encode(valor))
        # devolver como hex separados por '|'
        return (
            binascii.hexlify(ciphertext).decode()
            + "|"
            + binascii.hexlify(aesCipher.nonce).decode()
            + "|"
            + binascii.hexlify(authTag).decode()
        )

    def Descifrar(self, valor: str) -> str:
        """Descifra el string devuelto por Encriptar y retorna la cadena original."""
        parts = valor.split("|")
        if len(parts) != 3:
            raise ValueError("Formato inválido para Descifrar: se esperan 3 partes separadas por '|'")
        ciphertext = binascii.unhexlify(parts[0])
        nonce = binascii.unhexlify(parts[1])
        authTag = binascii.unhexlify(parts[2])
        aesCipher = AES.new(self.secretKey, AES.MODE_GCM, nonce=nonce)
        plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
        return plaintext.decode()


def encrypt_token(token_str: str) -> str:
    """Helper: encripta un token JWT (o cualquier string) y devuelve el formato almacenable."""
    en = EncriptarAES()
    return en.Encriptar(token_str)


def decrypt_token(enc_str: str) -> str:
    """Helper: descifra una cadena en el formato producido por encrypt_token."""
    en = EncriptarAES()
    return en.Descifrar(enc_str)
