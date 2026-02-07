from ..repositories import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, username: str, fullname: str, email: str, password: str):
        if not all([username, fullname, email, password]):
            raise ValueError("All fields (username, fullname, email, password) are required")
        return self.repo.create_user(username, fullname, email, password)

    def list_users(self):
        return self.repo.list_users()

    def get_user(self, user_id: int):
        if not user_id:
            raise ValueError("user_id is required")
        return self.repo.get_user_by_id(user_id)

    def update_user(self, user_id: int, data: dict):
        if not user_id:
            raise ValueError("user_id is required")
        if not data:
            raise ValueError("No data provided for update")
        return self.repo.update_user(user_id, data)

    def delete_user(self, user_id: int):
        if not user_id:
            raise ValueError("user_id is required")
        return self.repo.delete_user(user_id)
