import hashlib
import re

class User:
    def __init__(self, user_id, username, email, password, role="user"):
        self.id = user_id
        self.username = username
        self.email = email
        self.password_hash = self._hash(password)
        self.role = role

    def _hash(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == self._hash(password)

class AuthError(Exception):
    pass

class UserManager:
    def __init__(self):
        self._users = {}
        self._next_id = 1

    def create_user(self, username, email, password, role="user"):
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise ValueError("Invalid email")
        if len(password) < 4:
            raise ValueError("Password too short")
        if role not in ("admin", "user", "guest"):
            raise ValueError("Invalid role")
        user_id = self._next_id
        self._next_id += 1
        user = User(user_id, username, email, password, role)
        self._users[user_id] = user
        return user

    def authenticate(self, username, password):
        for user in self._users.values():
            if user.username == username:
                if user.check_password(password):
                    return user
                raise AuthError("Wrong password")
        raise AuthError("User not found")

    def delete_user(self, user_id):
        if user_id not in self._users:
            raise AuthError("User not found")
        del self._users[user_id]

    def change_role(self, user_id, new_role, requester_role):
        if requester_role != "admin":
            raise AuthError("Permission denied")
        if user_id not in self._users:
            raise AuthError("User not found")
        if new_role not in ("admin", "user", "guest"):
            raise ValueError("Invalid role")
        self._users[user_id].role = new_role

    def get_user_by_id(self, user_id):
        return self._users.get(user_id)
