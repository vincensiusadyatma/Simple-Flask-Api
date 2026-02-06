from ..repositories import AuthRepository
from ..utils import createToken

class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def register(self,username:str, fullname:str,email:str,password:str):
        
        if self.repo.getUserByEmail(email):
            raise ValueError("Email already registered")
        elif len(password) < 6:
            raise ValueError("Password must be at least 6 characters")

        else:
            try:
                user = self.repo.createUser(
                    username=username,
                    fullname=fullname,
                    email=email,
                    password=password
                )
            except Exception as e:
                print(f"DB Error: {e}")
                raise Exception("Failed to create user")  
        return user
    
    def login(self, email:str, password:str):
        try:
            user = self.repo.getUserByEmail(email)

            if user is None or user.password != password:
                raise ValueError("Email or password incorrect")
            else :
                token = createToken(username=user.username, email=user.email)
                return {"user": {"id": user.id, "username": user.username, "email": user.email}, "token": token}

        except ValueError as e:
            raise e 

        except Exception as e:
            print(f"Login error: {e}")
            raise Exception("Internal server error") 