from ..config import Session
from ..models.User import User
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    def __init__(self):
        self.session = Session()

    def list_users(self):
        try:
            return self.session.execute(select(User)).scalars().all()
        except SQLAlchemyError as e:
            print("DB Error list_users:", e)
            return []

    def create_user(self, username: str, fullname: str, email: str, password: str):
        try:
            user = User(username=username, fullname=fullname, email=email, password=password)
            self.session.add(user)
            self.session.commit()
            return user
        except SQLAlchemyError as e:
            self.session.rollback()
            print("DB Error create_user:", e)
            return None

    def get_user_by_id(self, user_id: int):
        try:
            return self.session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
        except SQLAlchemyError as e:
            print("DB Error get_user_by_id:", e)
            return None

    def get_user_by_username(self, username: str):
        try:
            return self.session.execute(select(User).where(User.username == username)).scalar_one_or_none()
        except SQLAlchemyError as e:
            print("DB Error get_user_by_username:", e)
            return None

    def get_user_by_email(self, email: str):
        try:
            return self.session.execute(select(User).where(User.email == email)).scalar_one_or_none()
        except SQLAlchemyError as e:
            print("DB Error get_user_by_email:", e)
            return None

    def update_user(self, user_id: int, data: dict):
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return None
            for key, value in data.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            self.session.commit()
            return user
        except SQLAlchemyError as e:
            self.session.rollback()
            print("DB Error update_user:", e)
            return None

    def delete_user(self, user_id: int):
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return None
            self.session.delete(user)
            self.session.commit()
            return user
        except SQLAlchemyError as e:
            self.session.rollback()
            print("DB Error delete_user:", e)
            return None
