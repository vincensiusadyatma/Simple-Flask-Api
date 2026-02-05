from ..repositories import AuthRepository

class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def register(self,username:str, fullname:str,email:str,password:str):
        try:
            print(username)
            self.repo.createUser(username=username, fullname=fullname, email=email, password=password)
        except Exception as e:
            print(e)
        # end try
