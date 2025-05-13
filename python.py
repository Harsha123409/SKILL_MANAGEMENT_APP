# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# hashed_password = pwd_context.hash("harshayadav")
# print(hashed_password)

import bcrypt

password = "harshayadav"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed)
