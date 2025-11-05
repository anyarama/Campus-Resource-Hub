"""
Unit Tests for Authentication Utilities - Campus Resource Hub
Tests password hashing and validation in security/auth_utils.py.

Per .clinerules: NEVER store plaintext passwords. Test bcrypt helpers.
"""

from src.security.auth_utils import hash_password, verify_password, validate_password_strength


class TestPasswordHashing:
    """Test password hashing functionality."""

    def test_hash_password_returns_non_plaintext(self):
        """Test that hashed password is not plaintext."""
        password = "MySecretPassword123"
        hashed = hash_password(password)

        # Hashed password should not equal plaintext
        assert hashed != password

        # Hashed password should be a string
        assert isinstance(hashed, str)

        # Hashed password should be substantially longer than input
        assert len(hashed) > len(password)
        assert len(hashed) > 50  # Typical bcrypt hash length

    def test_hash_password_produces_different_hashes(self):
        """Test that same password produces different hashes (salted)."""
        password = "SamePassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # Due to salting, hashes should be different
        assert hash1 != hash2

    def test_hash_password_with_special_characters(self):
        """Test hashing password with special characters."""
        password = "P@ssw0rd!#$%^&*()"
        hashed = hash_password(password)

        assert hashed != password
        assert len(hashed) > 50

    def test_hash_password_with_unicode(self):
        """Test hashing password with unicode characters."""
        password = "Пароль123"  # Russian characters
        hashed = hash_password(password)

        assert hashed != password
        assert len(hashed) > 50


class TestPasswordVerification:
    """Test password verification functionality."""

    def test_verify_correct_password(self):
        """Test that correct password verification succeeds."""
        password = "CorrectPassword123"
        hashed = hash_password(password)

        result = verify_password(password, hashed)

        assert result is True

    def test_verify_incorrect_password(self):
        """Test that incorrect password verification fails."""
        password = "CorrectPassword123"
        hashed = hash_password(password)

        result = verify_password("WrongPassword123", hashed)

        assert result is False

    def test_verify_case_sensitive(self):
        """Test that password verification is case-sensitive."""
        password = "CaseSensitive123"
        hashed = hash_password(password)

        # Lowercase version should fail
        assert verify_password("casesensitive123", hashed) is False

        # Uppercase version should fail
        assert verify_password("CASESENSITIVE123", hashed) is False

        # Exact match should succeed
        assert verify_password("CaseSensitive123", hashed) is True

    def test_verify_empty_password(self):
        """Test verification with empty password."""
        password = "NonEmptyPassword123"
        hashed = hash_password(password)

        result = verify_password("", hashed)

        assert result is False

    def test_verify_password_with_special_chars(self):
        """Test verification preserves special characters."""
        password = "P@ssw0rd!#$"
        hashed = hash_password(password)

        # Exact match should work
        assert verify_password("P@ssw0rd!#$", hashed) is True

        # Slight variation should fail
        assert verify_password("P@ssw0rd!#", hashed) is False

    def test_verify_multiple_passwords(self):
        """Test that different passwords have different hashes."""
        password1 = "FirstPassword123"
        password2 = "SecondPassword456"

        hash1 = hash_password(password1)
        hash2 = hash_password(password2)

        # Each password should only verify against its own hash
        assert verify_password(password1, hash1) is True
        assert verify_password(password1, hash2) is False
        assert verify_password(password2, hash1) is False
        assert verify_password(password2, hash2) is True


class TestPasswordStrengthValidation:
    """Test password strength validation."""

    def test_strong_password_valid(self):
        """Test that strong password passes validation."""
        is_valid, message = validate_password_strength("StrongPass123")

        assert is_valid is True
        assert message == "Password is strong"

    def test_password_too_short(self):
        """Test that short password fails validation."""
        is_valid, message = validate_password_strength("Short1")

        assert is_valid is False
        assert "at least 8 characters" in message

    def test_password_no_uppercase(self):
        """Test that password without uppercase fails."""
        is_valid, message = validate_password_strength("lowercase123")

        assert is_valid is False
        assert "uppercase" in message.lower()

    def test_password_no_lowercase(self):
        """Test that password without lowercase fails."""
        is_valid, message = validate_password_strength("UPPERCASE123")

        assert is_valid is False
        assert "lowercase" in message.lower()

    def test_password_no_digit(self):
        """Test that password without digit fails."""
        is_valid, message = validate_password_strength("NoDigitsHere")

        assert is_valid is False
        assert "digit" in message.lower()

    def test_password_exactly_8_chars_valid(self):
        """Test that 8-character password is acceptable."""
        is_valid, message = validate_password_strength("Valid123")

        assert is_valid is True
        assert message == "Password is strong"

    def test_password_with_special_chars_valid(self):
        """Test that special characters are allowed (not required)."""
        is_valid, message = validate_password_strength("P@ssw0rd!")

        assert is_valid is True
        assert message == "Password is strong"

    def test_password_all_requirements_met(self):
        """Test password that meets all requirements."""
        is_valid, message = validate_password_strength("MySecureP@ss2024")

        assert is_valid is True
        assert message == "Password is strong"

    def test_empty_password_invalid(self):
        """Test that empty password fails validation."""
        is_valid, message = validate_password_strength("")

        assert is_valid is False
        assert "at least 8 characters" in message

    def test_password_only_numbers_invalid(self):
        """Test that all-numeric password fails."""
        is_valid, message = validate_password_strength("12345678")

        assert is_valid is False
        # Should fail on no uppercase or no lowercase
        assert "uppercase" in message.lower() or "lowercase" in message.lower()

    def test_password_only_letters_invalid(self):
        """Test that password without numbers fails."""
        is_valid, message = validate_password_strength("OnlyLetters")

        assert is_valid is False
        assert "digit" in message.lower()


class TestPasswordHashingIntegration:
    """Integration tests for hash and verify together."""

    def test_hash_and_verify_workflow(self):
        """Test complete hash and verify workflow."""
        # User registers with password
        original_password = "UserPassword123"
        password_hash = hash_password(original_password)

        # Password should be hashed (not plaintext)
        assert password_hash != original_password

        # User logs in with correct password
        assert verify_password(original_password, password_hash) is True

        # User tries wrong password
        assert verify_password("WrongPassword123", password_hash) is False

    def test_multiple_users_same_password(self):
        """Test that same password produces different hashes for different users."""
        # Two users happen to use the same password
        password = "CommonPassword123"

        user1_hash = hash_password(password)
        user2_hash = hash_password(password)

        # Hashes should be different (salted)
        assert user1_hash != user2_hash

        # But both should verify correctly
        assert verify_password(password, user1_hash) is True
        assert verify_password(password, user2_hash) is True

    def test_validate_then_hash_workflow(self):
        """Test typical registration workflow: validate then hash."""
        password = "NewUserPass123"

        # First, validate password strength
        is_valid, message = validate_password_strength(password)
        assert is_valid is True

        # Only hash if valid
        if is_valid:
            password_hash = hash_password(password)
            assert password_hash != password
            assert verify_password(password, password_hash) is True

    def test_weak_password_rejected(self):
        """Test that weak passwords are rejected before hashing."""
        weak_password = "weak"

        # Validate first
        is_valid, message = validate_password_strength(weak_password)
        assert is_valid is False

        # In real app, would not proceed to hashing
        # But technically hashing still works even for weak passwords
        hashed = hash_password(weak_password)
        assert verify_password(weak_password, hashed) is True


class TestEdgeCases:
    """Test edge cases and security considerations."""

    def test_very_long_password(self):
        """Test hashing and verifying very long password."""
        password = "A" * 1000 + "b1"  # 1002 chars
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_password_with_whitespace(self):
        """Test that whitespace is preserved in password."""
        password = "Pass Word 123"
        hashed = hash_password(password)

        # With exact whitespace should work
        assert verify_password("Pass Word 123", hashed) is True

        # Without whitespace should fail
        assert verify_password("PassWord123", hashed) is False

    def test_password_leading_trailing_spaces(self):
        """Test that leading/trailing spaces matter."""
        password = "Password123"
        hashed = hash_password(password)

        # With extra spaces should fail
        assert verify_password(" Password123", hashed) is False
        assert verify_password("Password123 ", hashed) is False
        assert verify_password(" Password123 ", hashed) is False

    def test_null_bytes_in_password(self):
        """Test handling of null bytes (should work but is unusual)."""
        # This is an edge case - most systems would reject this
        # But our hashing should handle it
        password = "Pass\x00word123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True
