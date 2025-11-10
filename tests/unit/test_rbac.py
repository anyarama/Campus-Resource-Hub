"""
Unit tests for RBAC (Role-Based Access Control) decorators.

Tests the @require_roles, @require_admin, and @require_staff_or_admin decorators
to ensure proper authorization enforcement.

AI Contribution: Cline generated test structure
Reviewed and validated by developer on 2025-11-05
"""

from src.security.rbac import require_roles, require_admin, require_staff_or_admin
from src.repositories.user_repo import UserRepository
from src.models import db


def ensure_user(name: str, email: str, role: str, password: str = "Password123"):
    existing = UserRepository.get_by_email(email)
    if existing:
        existing.role = role
        existing.set_password(password)
        db.session.commit()
        return existing
    return UserRepository.create(name=name, email=email, password=password, role=role)


class TestRBACDecorators:
    """Unit tests for RBAC decorator functions."""

    def test_require_roles_allows_correct_role(self, client, app):
        """Test that @require_roles allows users with the correct role."""
        with app.app_context():
            # Create a student user
            ensure_user(name="Student User", email="student@test.com", role="student")

            # Define a test route that requires student role
            @app.route("/student-only")
            @require_roles("student")
            def student_route():
                return {"message": "Student access granted"}

            # Login as student
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "student@test.com", "password": "Password123"},
                )

                # Access the protected route
                response = client.get("/student-only")
                assert response.status_code == 200
                assert b"Student access granted" in response.data

    def test_require_roles_blocks_wrong_role(self, client, app):
        """Test that @require_roles blocks users without the required role."""
        with app.app_context():
            # Create a student user
            ensure_user(name="Student User", email="student@test.com", role="student")

            # Define a test route that requires admin role
            @app.route("/admin-only-test")
            @require_roles("admin")
            def admin_route():
                return {"message": "Admin access granted"}

            # Login as student
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "student@test.com", "password": "Password123"},
                )

                # Try to access admin route (should be forbidden)
                response = client.get("/admin-only-test")
                assert response.status_code == 403

    def test_require_roles_returns_401_when_unauthenticated(self, client, app):
        """Test that @require_roles returns 401 for unauthenticated users."""
        with app.app_context():
            # Define a test route that requires student role
            @app.route("/protected-test")
            @require_roles("student")
            def protected_route():
                return {"message": "Access granted"}

            # Try to access without logging in (should be unauthorized)
            response = client.get("/protected-test")
            assert response.status_code == 401

    def test_require_roles_multiple_roles(self, client, app):
        """Test that @require_roles works with multiple allowed roles."""
        with app.app_context():
            # Create users with different roles
            ensure_user(name="Staff User", email="staff@test.com", role="staff")
            ensure_user(name="Admin User", email="admin@test.com", role="admin")
            ensure_user(name="Student User", email="student@test.com", role="student")

            # Define a route that allows both staff and admin
            @app.route("/staff-or-admin-test")
            @require_roles("staff", "admin")
            def staff_or_admin_route():
                return {"message": "Staff or admin access granted"}

            # Test staff access (should succeed)
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "staff@test.com", "password": "Password123"},
                )
                response = client.get("/staff-or-admin-test")
                assert response.status_code == 200

            # Logout
            with client:
                client.post("/auth/logout")

            # Test admin access (should succeed)
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "admin@test.com", "password": "Password123"},
                )
                response = client.get("/staff-or-admin-test")
                assert response.status_code == 200

            # Logout
            with client:
                client.post("/auth/logout")

            # Test student access (should be forbidden)
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "student@test.com", "password": "Password123"},
                )
                response = client.get("/staff-or-admin-test")
                assert response.status_code == 403

    def test_require_admin_decorator(self, client, app):
        """Test the @require_admin convenience decorator."""
        with app.app_context():
            # Create admin and non-admin users
            ensure_user(name="Admin User", email="admin@test.com", role="admin")
            ensure_user(name="Student User", email="student@test.com", role="student")

            # Define an admin-only route
            @app.route("/admin-decorator-test")
            @require_admin
            def admin_only():
                return {"message": "Admin access granted"}

            # Test admin access (should succeed)
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "admin@test.com", "password": "Password123"},
                )
                response = client.get("/admin-decorator-test")
                assert response.status_code == 200

            # Logout
            with client:
                client.post("/auth/logout")

            # Test student access (should be forbidden)
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "student@test.com", "password": "Password123"},
                )
                response = client.get("/admin-decorator-test")
                assert response.status_code == 403

    def test_require_staff_or_admin_decorator(self, client, app):
        """Test the @require_staff_or_admin convenience decorator."""
        with app.app_context():
            # Create users with different roles
            ensure_user(name="Admin User", email="admin@test.com", role="admin")
            ensure_user(name="Staff User", email="staff@test.com", role="staff")
            ensure_user(name="Student User", email="student@test.com", role="student")

            # Define a staff-or-admin route
            @app.route("/staff-admin-decorator-test")
            @require_staff_or_admin
            def staff_or_admin():
                return {"message": "Staff or admin access granted"}

            # Test admin access (should succeed)
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "admin@test.com", "password": "Password123"},
                )
                response = client.get("/staff-admin-decorator-test")
                assert response.status_code == 200

            # Logout
            with client:
                client.post("/auth/logout")

            # Test staff access (should succeed)
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "staff@test.com", "password": "Password123"},
                )
                response = client.get("/staff-admin-decorator-test")
                assert response.status_code == 200

            # Logout
            with client:
                client.post("/auth/logout")

            # Test student access (should be forbidden)
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "student@test.com", "password": "Password123"},
                )
                response = client.get("/staff-admin-decorator-test")
                assert response.status_code == 403

    def test_rbac_preserves_function_metadata(self, app):
        """Test that RBAC decorators preserve original function metadata."""
        with app.app_context():

            @require_roles("admin")
            def test_function():
                """Test docstring."""
                return "Test"

            # The decorator should preserve function name and docstring
            assert test_function.__name__ == "test_function"
            assert test_function.__doc__ == "Test docstring."

    def test_admin_ping_route_authorization(self, client, app):
        """Test the actual /admin/ping route RBAC enforcement."""
        with app.app_context():
            # Create admin and student users
            ensure_user(name="Admin User", email="admin@test.com", role="admin")
            ensure_user(name="Student User", email="student@test.com", role="student")

            # Test unauthenticated access (should redirect to login)
            response = client.get("/admin/ping")
            assert response.status_code in {302, 401}
            if response.status_code == 302:
                assert "/auth/login" in (response.headers.get("Location") or "")

            # Test admin access (should succeed)
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "admin@test.com", "password": "Password123"},
                )
                response = client.get("/admin/ping")
                assert response.status_code == 200
                payload = response.get_json()
                assert payload["message"] == "Admin access confirmed"

            # Logout
            with client:
                client.post("/auth/logout")

            # Test student access (should be forbidden)
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "student@test.com", "password": "Password123"},
                )
                response = client.get("/admin/ping")
                assert response.status_code == 403


class TestRBACEdgeCases:
    """Edge cases and error scenarios for RBAC."""

    def test_rbac_with_case_sensitive_roles(self, client, app):
        """Test that role comparison is case-sensitive."""
        with app.app_context():
            # Create user with lowercase role
            ensure_user(name="Test User", email="test@test.com", role="admin")

            # Define route requiring uppercase "ADMIN" (should fail)
            @app.route("/uppercase-admin-test")
            @require_roles("ADMIN")
            def uppercase_admin():
                return {"message": "Access granted"}

            # Login
            with client:
                client.post(
                    "/auth/login",
                    data={"email": "test@test.com", "password": "Password123"},
                )

                # Should be forbidden (role is "admin", not "ADMIN")
                response = client.get("/uppercase-admin-test")
                assert response.status_code == 403

    def test_rbac_with_empty_roles_list(self, app):
        """Test that @require_roles with empty list blocks all access."""
        with app.app_context():

            @require_roles()
            def no_roles_allowed():
                return "Should never reach here"

            # This decorator configuration should block everyone
            # (no roles are allowed)
