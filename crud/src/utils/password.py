from passlib.context import CryptContext


class Password:
    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def hash_password(password):
        return Password.__pwd_context.hash(password)

    @staticmethod
    def verify_password(crypt_pass, raw_pass):
        return Password.__pwd_context.verify(raw_pass, crypt_pass)
