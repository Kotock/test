import pytest
from user_system import UserManager, AuthError

@pytest.fixture
def manager_with_users():
    mgr = UserManager()
    mgr.create_user("alice", "alice@mail.com", "secret", "admin")
    mgr.create_user("bob", "bob@mail.com", "password", "user")
    return mgr

class TestUserSystem:
    def test_create_user(self):
        mgr = UserManager()
        u = mgr.create_user("test", "test@mail.com", "pass", "user")
        assert u.username == "test"
        assert u.role == "user"

    def test_create_user_invalid_email(self):
        mgr = UserManager()
        with pytest.raises(ValueError):
            mgr.create_user("test", "bad-email", "pass")

    def test_create_user_short_password(self):
        mgr = UserManager()
        with pytest.raises(ValueError):
            mgr.create_user("test", "test@mail.com", "123")

    @pytest.mark.parametrize("role", ["admin", "user", "guest"])
    def test_create_user_roles(self, role):
        mgr = UserManager()
        u = mgr.create_user("test", "test@mail.com", "pass", role)
        assert u.role == role

    def test_authenticate_success(self, manager_with_users):
        u = manager_with_users.authenticate("alice", "secret")
        assert u.username == "alice"

    def test_authenticate_wrong_password(self, manager_with_users):
        with pytest.raises(AuthError):
            manager_with_users.authenticate("alice", "wrong")

    def test_authenticate_user_not_found(self, manager_with_users):
        with pytest.raises(AuthError):
            manager_with_users.authenticate("nobody", "secret")

    def test_delete_user(self, manager_with_users):
        manager_with_users.delete_user(1)
        assert manager_with_users.get_user_by_id(1) is None

    def test_change_role_by_admin(self, manager_with_users):
        manager_with_users.change_role(2, "admin", "admin")
        assert manager_with_users.get_user_by_id(2).role == "admin"

    def test_change_role_permission_denied(self, manager_with_users):
        with pytest.raises(AuthError):
            manager_with_users.change_role(2, "admin", "user")
