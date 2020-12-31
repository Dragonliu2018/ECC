"""
A point in the group and the order of the group (in this case the number of points on the elliptic curve) are public knowledge.

Bob chooses a secret message (a number b with 0 < b < n).
Alice chooses a secret message (a number a with 0 < a < n).

"""

from random import SystemRandom
from Elliptic_Curve import EllipticCurve
try:
	from Crypto.Cipher import AES
except ModuleNotFoundError:
	print("You need to install pycryptodome")
	exit(1)
import hashlib
rand=SystemRandom()
def hashit(str):
	"""
	Returns the digest of the SHA-256 hash function for use as the key in our AES-256 encryption.
	"""
	result = hashlib.sha256(str.encode())
	return result.digest()

def encrypt(message, exchanged_value):
	"""
	Encrypts the message using the symmetric encryption scheme AES-256 with x-coordinate of the shared secret as a key.
	"""
	data = message.encode("utf8")
	key = hashit(exchanged_value)
	cipher = AES.new(key,AES.MODE_EAX)
	nonce = cipher.nonce
	ciphertext,tag = cipher.encrypt_and_digest(data)
	return(nonce,ciphertext,tag)


def decrypt(encrypted, exchanged_value):
	"""
	Decrypting the message. The variable "encrypted" is a tuple (nonce,ciphertext,tag).
	Since bob has the shared secret, he can make the appropriate key.
	For an attacker to (naively) obtain the correct key, they must solve the ECDLP.
	"""
	key = hashit(exchanged_value)
	cipher = AES.new(key,AES.MODE_EAX, nonce = encrypted[0])
	plaintext = cipher.decrypt(encrypted[1])
	try:
		cipher.verify(encrypted[2])
	except ValueError:
		print("The message could not be verified!")
	return plaintext.decode("utf8")

#生成密钥
def genkey():
	print("The elliptic curve we're working over is (modulo 115792089237316195423570985008687907853269984665640564039457584007908834671663):")
	ec = EllipticCurve(0,7,115792089237316195423570985008687907853269984665640564039457584007908834671663  )
	if ec.a == 0:
		print("y^2 = " + "x^3 + " + str(ec.b))	
	elif ec.a != 1:
		print("y^2 = " + "x^3 + " + str(ec.a)+"x + " + str(ec.b))
	else:
		print("y^2 = " + "x^3 + " + "x + " + str(ec.b))


	numberPoints = 115792089237316195423570985008687907852837564279074904382605163141518161494337
	print("The order of E is: ", numberPoints)
	print("-"*80)


	print("The point we're using is:")
	P = (int("79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798",16),int("483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8",16))
	print(P)
	print("The order of this point is:")
	print(numberPoints)
	print("The order of the point is prime.")


	b = rand.getrandbits(256)%numberPoints
	a = rand.getrandbits(256)%numberPoints
	bP = ec.multiply(b,P)
	aP = ec.multiply(a,P)
	abP = ec.multiply(a*b,P)

	keys = [a, aP, b, bP, abP]
	print("Alice's private key is: ", format(a,'x'))
	print("Alice's public key is: ({:x}, {:x} ) ".format(aP[0],aP[1]))
	print("Bob's private key is: ",format(b,'x'))
	print("Bob's public key is: ({:x}, {:x} ) ".format(bP[0],bP[1]))
	print("The exchanged value is: ({:x}, {:x} ) ".format(abP[0],abP[1]))

	return keys
#测试DH	
def test(message_in, key):
	# print("Alice, enter your message to be encrypted: \n")
	# message_in = '\n'.join(iter(input, ""))
	print("The encrypted message is:")
	encrypted = encrypt(message_in,str(key))
	print(encrypted[1].hex())
	print("Bob uses the shared secret to see that the original message is:")
	decrypted_message = decrypt(encrypted,str(key))
	print(decrypted_message)
	ans_list = [encrypted[1].hex(), decrypted_message]
	return ans_list
