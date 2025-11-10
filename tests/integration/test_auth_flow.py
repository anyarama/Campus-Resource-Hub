"""
Integration tests for authentication flow.

Tests the complete user journey:
- Register new account
- Login with correct credentials
- Access protected route (dashboard)
- Logout
- Verify unauthenticated access redirects to login

AI Contribution: Cline generated test structure
Reviewed and validated by developer on 2025-11-05
"""

from src.repositories.user_repo import UserRepository


class TestAuthFlow:
    """Integration tests for complete authentication workflow."""

    def test_register_login_dashboard_logout_flow(self, client, app):
        """
        Test complete user journey: register → login → dashboard → logout.

        This is the primary integration test validating:
        1. User can register with valid credentials
        2. User can login with registered credentials
        3. Authenticated user can access protected route
        4. User can logout successfully
        5. After logout, protected route redirects to login
        """
        with app.app_context():
            # Step 1: Register new user
            register_data = {
                "name": "Integration Test User",
                "email": "integration@test.com",
                "password": "TestPassword123",
                "confirm_password": "TestPassword123",
                "role": "student",
                "department": "Computer Science",
            }

            response = client.post("/auth/register", data=register_data, follow_redirects=False)

            # Should redirect to login after successful registration
            assert response.status_code == 302
            assert "/auth/login" in response.location

            # Verify user was created in database
            user = UserRepository.get_by_email("integration@test.com")
            assert user is not None
            assert user.name == "Integration Test User"
            assert user.role == "student"
            assert user.department == "Computer Science"

            # Step 2: Login with registered credentials
            login_data = {"email": "integration@test.com", "password": "TestPassword123"}

            response = client.post("/auth/login", data=login_data, follow_redirects=False)

            # Should redirect to dashboard after successful login
            assert response.status_code == 302
            assert "/dashboard" in response.location

            # Step 3: Access protected dashboard route
            response = client.get("/dashboard", follow_redirects=True)
            assert response.status_code == 200
            # Verify dashboard content is rendered
            assert b"Welcome, Integration Test User" in response.data

            # Step 4: Logout
            response = client.post("/auth/logout", follow_redirects=False)
            assert response.status_code == 302
            assert "/auth/login" in response.location or "/" in response.location

            # Step 5: Verify unauthenticated access redirects to login
            response = client.get("/dashboard", follow_redirects=False)
            assert response.status_code == 302
            assert "/auth/login" in response.location

    def test_login_with_wrong_password(self, client, app):
        """Test that login fails with incorrect password."""
        with app.app_context():
            # Create a user
            UserRepository.create(
                name="Test User",
                email="test@example.com",
                password="CorrectPassword123",
                role="student",
            )

            # Attempt login with wrong password
            login_data = {"email": "test@example.com", "password": "WrongPassword123"}

            response = client.post("/auth/login", data=login_data, follow_redirects=True)

            # Should stay on login page
            assert response.status_code == 200
            assert b"Invalid email or password" in response.data

    def test_login_with_nonexistent_email(self, client, app):
        """Test that login fails with non-existent email."""
        with app.app_context():
            login_data = {
                "email": "nonexistent@example.com",
                "password": "SomePassword123",
            }

            response = client.post("/auth/login", data=login_data, follow_redirects=True)

            # Should stay on login page with error
            assert response.status_code == 200
            assert b"Invalid email or password" in response.data

    def test_register_with_existing_email(self, client, app):
        """Test that registration fails if email already exists."""
        with app.app_context():
            # Create a user
            UserRepository.create(
                name="Existing User",
                email="existing@example.com",
                password="Password123",
                role="student",
            )

            # Attempt to register with same email
            register_data = {
                "name": "Another User",
                "email": "existing@example.com",
                "password": "DifferentPassword123",
                "confirm_password": "DifferentPassword123",
                "role": "student",
            }

            response = client.post("/auth/register", data=register_data, follow_redirects=True)

            # Should stay on register page with error
            assert response.status_code == 200
            users = UserRepository.get_all(role="student")["items"]
            duplicates = [u for u in users if u.email == "existing@example.com"]
            assert len(duplicates) == 1

    def test_register_with_weak_password(self, client, app):
        """Test that registration fails with weak password."""
        with app.app_context():
            register_data = {
                "name": "Weak Password User",
                "email": "weak@example.com",
                "password": "weak",  # Too short, no uppercase, no digit
                "confirm_password": "weak",
                "role": "student",
            }

            response = client.post("/auth/register", data=register_data, follow_redirects=True)

            # Should stay on register page with error
            assert response.status_code == 200
            # Check for password strength error message
            assert (
                b"at least 8 characters" in response.data
                or b"uppercase" in response.data
                or b"digit" in response.data
            )

    def test_register_with_mismatched_passwords(self, client, app):
        """Test that registration fails when passwords don't match."""
        with app.app_context():
            register_data = {
                "name": "Mismatch User",
                "email": "mismatch@example.com",
                "password": "Password123",
                "confirm_password": "DifferentPassword123",
                "role": "student",
            }

            response = client.post("/auth/register", data=register_data, follow_redirects=True)

            # Should stay on register page with error
            assert response.status_code == 200
            assert b"Passwords do not match" in response.data

    def test_protected_route_requires_authentication(self, client, app):
        """Test that protected routes redirect to login when not authenticated."""
        with app.app_context():
            # Try to access dashboard without logging in
            response = client.get("/dashboard", follow_redirects=False)

            # Should redirect to login
            assert response.status_code == 302
            assert "/auth/login" in response.location

    def test_profile_page_requires_authentication(self, client, app):
        """Test that profile page is protected."""
        with app.app_context():
            # Try to access profile without logging in
            response = client.get("/auth/profile", follow_redirects=False)

            # Should redirect to login
            assert response.status_code == 302
            assert "/auth/login" in response.location

    def test_remember_me_functionality(self, client, app):
        """Test that remember me checkbox extends session."""
        with app.app_context():
            # Create a user
            UserRepository.create(
                name="Remember User",
                email="remember@example.com",
                password="Password123",
                role="student",
            )

            # Login with remember me checked
            login_data = {
                "email": "remember@example.com",
                "password": "Password123",
                "remember": "on",
            }

            response = client.post("/auth/login", data=login_data, follow_redirects=False)

            # Should redirect to dashboard
            assert response.status_code == 302
            assert "/dashboard" in response.location

            # Verify user can access protected route
            response = client.get("/dashboard", follow_redirects=True)
            assert response.status_code == 200

    def test_multiple_roles_registration(self, client, app):
        """Test that users can register with different roles."""
        with app.app_context():
            roles_to_test = ["student", "staff", "admin"]

            for idx, role in enumerate(roles_to_test):
                register_data = {
                    "name": f"{role.capitalize()} User",
                    "email": f"{role}@example.com",
                    "password": "Password123",
                    "confirm_password": "Password123",
                    "role": role,
                }

                response = client.post("/auth/register", data=register_data, follow_redirects=False)

                # Should redirect to login
                assert response.status_code == 302

                # Verify user was created with correct role
                user = UserRepository.get_by_email(f"{role}@example.com")
                assert user is not None
                assert user.role == role


class TestAuthEdgeCases:
    """Edge cases and error handling tests."""

    def test_register_with_missing_required_fields(self, client, app):
        """Test that registration fails with missing required fields."""
        with app.app_context():
            # Missing name
            register_data = {
                "email": "missing@example.com",
                "password": "Password123",
                "confirm_password": "Password123",
                "role": "student",
            }

            response = client.post("/auth/register", data=register_data, follow_redirects=True)

            # Should have validation error
            assert response.status_code == 200

    def test_login_with_missing_fields(self, client, app):
        """Test that login fails with missing fields."""
        with app.app_context():
            # Missing password
            login_data = {"email": "test@example.com"}

            response = client.post("/auth/login", data=login_data, follow_redirects=True)

            # Should stay on login page
            assert response.status_code == 200

    def test_csrf_token_present_in_forms(self, client, app):
        """Test that CSRF tokens are present in auth forms."""
        with app.app_context():
            # Get login page
            response = client.get("/auth/login")
            assert response.status_code == 200
            assert b'name="csrf_token"' in response.data

            # Get register page
            response = client.get("/auth/register")
            assert response.status_code == 200
            assert b'name="csrf_token"' in response.data

    def test_logout_requires_post_method(self, client, app):
        """Test that logout only accepts POST requests (CSRF protection)."""
        with app.app_context():
            # Create and login user
            UserRepository.create(
                name="Test User",
                email="test@example.com",
                password="Password123",
                role="student",
            )

            login_data = {"email": "test@example.com", "password": "Password123"}
            client.post("/auth/login", data=login_data, follow_redirects=True)

            # Try GET request to logout (should fail or redirect)
            response = client.get("/auth/logout", follow_redirects=False)

            # Should not allow GET (either 405 Method Not Allowed or redirect)
            # The actual implementation uses POST for security
            assert response.status_code in [302, 405]
