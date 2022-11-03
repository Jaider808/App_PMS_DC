from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, Cedula, password, fullname="") -> None:
        self.id = id
        self.Cedula = Cedula
        self.password = password
        self.fullname = fullname

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
