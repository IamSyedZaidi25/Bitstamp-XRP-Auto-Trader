import bcrypt

pw2hash = input("Please enter a password to hash: ")
pw2hash = bytes(pw2hash, 'utf-8')
hashedpw = bcrypt.hashpw(pw2hash, bcrypt.gensalt())
print(hashedpw)

pw3hash = input("Please enter a password to unlock: ")
pw3hash = bytes(pw3hash, 'utf-8')
hashedpw2 = bcrypt.hashpw(pw3hash, hashedpw)



while hashedpw2 != hashedpw:
	pw3hash = input("Incorrect password, please re-enter: ")
	pw3hash = bytes(pw3hash, 'utf-8')
	hashedpw2 = bcrypt.hashpw(pw3hash, hashedpw)

print("Unlock successful...")
