from ..config import Session
from ..models import User

class AuthRepository :
    def __init__(self):
        self.session = Session()
    
    def createUser(self,username:str, fullname:str,email:str,password:str):
        user = User(username=username, fullname=fullname, email=email, password=password)
        return self.session.add(user)
