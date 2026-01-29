from passlib.context import CryptContext

password_context = CryptContext(
    schemes=['bcrypt'],
    deprecated="auto"  # it means in future, if bcrypt deprecates, use another more secure, non-deprecated algorithm instead. 
)

def hash_password(password:str) -> str:
    print("hellloooo")
    return password_context.hash(password)

def verify_password(password:str, hash:str) -> bool:
    return password_context.verify(password, hash)