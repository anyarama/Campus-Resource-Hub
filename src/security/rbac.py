"""
Campus Resource Hub - Role-Based Access Control (RBAC)
AiDD 2025 Capstone Project

Decorators for role-based access control per .clinerules security requirements.

AI Contribution: Cline generated RBAC decorator structure
Reviewed and configured by developer on 2025-11-05
"""

from functools import wraps
from typing import Callable
from flask import abort
from flask_login import current_user


def require_roles(*roles: str) -> Callable:
    """
    Decorator to require specific user roles for route access.

    Enforces role-based access control (RBAC) per .clinerules security requirements.
    Returns 403 Forbidden if user lacks required role.

    Args:
        *roles: Variable number of role strings ('student', 'staff', 'admin')

    Returns:
        Decorated function that checks user roles before execution

    Example:
        @app.route('/admin/dashboard')
        @login_required
        @require_roles('admin')
        def admin_dashboard():
            return render_template('admin/dashboard.html')

        @app.route('/staff/approvals')
        @login_required
        @require_roles('staff', 'admin')
        def staff_approvals():
            return render_template('staff/approvals.html')

    Security Notes:
        - User must be authenticated (use @login_required first)
        - 401 if not authenticated (handled by Flask-Login)
        - 403 if authenticated but wrong role
        - Role check is case-sensitive
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is authenticated (should be handled by @login_required)
            if not current_user.is_authenticated:
                abort(401)  # Unauthorized

            # Check if user has one of the required roles
            if current_user.role not in roles:
                abort(403)  # Forbidden (authenticated but wrong role)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_admin(f: Callable) -> Callable:
    """
    Decorator requiring admin role.

    Convenience wrapper around require_roles('admin').

    Example:
        @app.route('/admin/users')
        @login_required
        @require_admin
        def manage_users():
            return render_template('admin/users.html')
    """
    return require_roles("admin")(f)


def require_staff(f: Callable) -> Callable:
    """
    Decorator requiring staff role (includes admin).

    Convenience wrapper around require_roles('staff', 'admin').
    Used for booking approvals and staff-level operations.

    Example:
        @app.route('/bookings/<int:booking_id>/approve')
        @login_required
        @require_staff
        def approve_booking(booking_id):
            # Only staff or admin can approve bookings
            pass
    """
    return require_roles("staff", "admin")(f)


def require_staff_or_admin(f: Callable) -> Callable:
    """
    Decorator requiring staff or admin role.

    Alias for require_staff (kept for backward compatibility).

    Example:
        @app.route('/bookings/<int:booking_id>/approve')
        @login_required
        @require_staff_or_admin
        def approve_booking(booking_id):
            # Only staff or admin can approve bookings
            pass
    """
    return require_roles("staff", "admin")(f)


def require_resource_owner_or_admin(f: Callable) -> Callable:
    """
    Decorator requiring user to be resource owner or admin.

    More complex decorator that checks ownership in addition to roles.
    Expects 'resource_id' parameter in route.

    Example:
        @app.route('/resources/<int:resource_id>/edit')
        @login_required
        @require_resource_owner_or_admin
        def edit_resource(resource_id):
            # Only owner or admin can edit
            pass

    Note: Implementation requires checking resource owner_id against current_user.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)

        # Admin can access any resource
        if current_user.role == "admin":
            return f(*args, **kwargs)

        # Check ownership (requires resource_id in kwargs)
        resource_id = kwargs.get("resource_id")
        if resource_id is None:
            abort(400)  # Bad request - missing resource_id

        # Import here to avoid circular dependency
        from src.repositories.resource_repo import ResourceRepository

        resource = ResourceRepository.get_by_id(resource_id)
        if resource is None:
            abort(404)  # Resource not found

        if resource.owner_id != current_user.user_id:
            abort(403)  # Forbidden - not owner, not admin

        return f(*args, **kwargs)

    return decorated_function
