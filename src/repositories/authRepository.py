from ..config import Session
from ..models import User
from sqlalchemy import select

class AuthRepository :
    def __init__(self):
        self.session = Session()
    
    def createUser(self,username:str, fullname:str,email:str,password:str):
        user = User(username=username, fullname=fullname, email=email, password=password)
        print(username)
        self.session.add(user)
        self.session.commit()
       
        return user
    
    def getUserByEmail(self,email:str):
        return self.session.execute(select(User).where(User.email == email))
