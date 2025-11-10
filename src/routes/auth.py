"""
Campus Resource Hub - Authentication Routes
AiDD 2025 Capstone Project

Flask blueprint for user authentication: register, login, logout.
Per .clinerules: CSRF enabled, bcrypt passwords, server-side validation.

AI Contribution: Cline generated initial auth route structure
Reviewed and secured by developer on 2025-11-05
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from src.app import db
from src.models.user import User
from src.repositories.user_repo import UserRepository
from src.security.auth_utils import verify_password, validate_password_strength


# Create auth blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    User registration route.

    GET: Display registration form
    POST: Process registration with server-side validation

    Security per .clinerules:
    - Password strength validation (8+ chars, upper, lower, digit)
    - Email uniqueness check
    - bcrypt password hashing
    - CSRF token required (handled by Flask-WTF)
    - XSS protection via Jinja autoescape
    """
    # Redirect if already logged in
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("resources.dashboard"))

    if request.method == "POST":
        # Get form data
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "student").strip().lower()
        department = request.form.get("department", "").strip()

        # Server-side validation
        errors = []

        if not name or len(name) < 2:
            errors.append("Name must be at least 2 characters.")

        if not email or "@" not in email:
            errors.append("Valid email address is required.")

        # Check email uniqueness
        existing_user = UserRepository.get_by_email(email)
        if existing_user:
            errors.append("Email address already registered.")

        # Password strength validation
        is_strong, strength_msg = validate_password_strength(password)
        if not is_strong:
            errors.append(strength_msg)

        if password != confirm_password:
            errors.append("Passwords do not match.")

        # Role validation
        if role not in ["student", "staff", "admin"]:
            role = "student"  # Default to student if invalid

        # If validation errors, show them
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "auth/register.html", name=name, email=email, role=role, department=department
            )

        # Create new user
        try:
            UserRepository.create(
                name=name,
                email=email,
                password=password,
                role=role,
                department=department if department else None,
            )
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))

        except Exception:
            db.session.rollback()
            flash("Registration failed. Please try again.", "danger")
            return render_template(
                "auth/register.html", name=name, email=email, role=role, department=department
            )

    # GET request - show form
    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    User login route.

    GET: Display login form
    POST: Authenticate user and create session

    Security per .clinerules:
    - bcrypt password verification (constant-time comparison)
    - CSRF token required
    - Session protection enabled (Flask-Login)
    - Failed login attempts tracked (future enhancement)
    """
    # Redirect if already logged in
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("resources.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember", False)

        # Server-side validation
        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("auth/login.html", email=email)

        # Get user by email
        user = UserRepository.get_by_email(email)

        # Verify password (using constant-time comparison)
        if user and verify_password(password, user.password_hash):
            # Login successful
            login_user(user, remember=remember)
            flash(f"Welcome back, {user.name}!", "success")

            # Redirect to next page or dashboard
            next_page = request.args.get("next")
            if not next_page or not next_page.startswith("/"):
                next_page = url_for("resources.dashboard")
            return redirect(next_page)
        else:
            # Login failed - intentionally vague message for security
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html", email=email)

    # GET request - show form
    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    User logout route.

    POST-only for CSRF protection (prevents logout via GET link in email phishing).
    Clears Flask-Login session.
    """
    logout_user()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/profile")
@login_required
def profile():
    """
    User profile page (view only).

    Shows current user's information. Edit functionality to be added in Phase 5.
    """
    return render_template("auth/profile.html", user=current_user)
