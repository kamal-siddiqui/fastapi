from passlib.context import CryptContext

pass_cnt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):
        return pass_cnt.hash(password)
    
    def verify(plain_password, hashed_password):
        return pass_cnt.verify(plain_password, hashed_password)