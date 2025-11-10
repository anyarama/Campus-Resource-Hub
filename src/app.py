"""
Campus Resource Hub - Application Factory
AiDD 2025 Capstone Project

Flask application factory following the app factory pattern per .clinerules.
Implements blueprints for: auth, resources, bookings, messages, reviews, admin.

AI Contribution: Cline generated initial app factory structure
Reviewed and configured by developer on 2025-11-02
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from typing import Optional

from src.config import get_config
from src.util.assets import asset_url
from src.utils.vite import vite_asset


# Initialize Flask extensions (created here, initialized in create_app)
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()


def create_app(config_name: Optional[str] = None) -> Flask:
    """
    Application factory for creating Flask app instances.

    This follows the app factory pattern per .clinerules, allowing for:
    - Multiple app instances with different configs (dev, test, prod)
    - Easier testing with isolated app contexts
    - Delayed configuration and extension initialization

    Args:
        config_name: Configuration name ('development', 'testing', 'production')
                    If None, uses FLASK_ENV environment variable

    Returns:
        Configured Flask application instance

    Example:
        >>> app = create_app('development')
        >>> app.run()
    """
    # Create Flask app instance
    app = Flask(
        __name__, instance_relative_config=True, static_folder="static", template_folder="templates"
    )

    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    config_class.init_app(app)

    # Ensure instance folder exists (for SQLite database)
    try:
        app.instance_path  # This creates the instance folder if needed
    except OSError:
        pass

    # Initialize Flask extensions
    initialize_extensions(app)

    # Import models (so Flask-Migrate can detect them)
    with app.app_context():
        pass

    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Register shell context (for flask shell)
    register_shell_context(app)

    # Register CLI commands
    register_cli_commands(app)

    # Register Vite asset helper for manifest-aware URLs
    app.jinja_env.globals["asset_url"] = asset_url
    app.jinja_env.globals["vite_asset"] = vite_asset

    # Add Cache-Control headers for development (per Task A requirement)
    @app.before_request
    def add_cache_headers():
        """Prevent caching of assets during development to avoid stale manifest issues."""
        from flask import request

        if app.debug and request.path.startswith("/static/dist/"):
            # Will be applied in after_request
            pass

    @app.after_request
    def apply_cache_headers(response):
        """Apply Cache-Control headers to static assets in development mode."""
        from flask import request

        if app.debug and request.path.startswith("/static/dist/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response

    @app.route("/_debug/assets")
    def _debug_assets():
        """
        Debug endpoint to diagnose asset resolution issues.
        Shows manifest location, resolved URLs, and file existence.
        """
        from src.util.assets import _manifest_path

        # Get resolved asset URLs
        css_url = asset_url("style")
        js_url = asset_url("enterpriseJs")

        # Check manifest existence
        manifest_path = _manifest_path()
        manifest_vite = os.path.join(app.root_path, "static", "dist", ".vite", "manifest.json")
        manifest_root = os.path.join(app.root_path, "static", "dist", "manifest.json")

        manifest_vite_exists = os.path.exists(manifest_vite)
        manifest_root_exists = os.path.exists(manifest_root)

        # Check if resolved files exist
        # Extract filename from URL (remove /static/ prefix)
        css_file = css_url.replace("/static/", "") if css_url.startswith("/static/") else css_url
        js_file = js_url.replace("/static/", "") if js_url.startswith("/static/") else js_url

        css_path = os.path.join(app.root_path, "static", css_file)
        js_path = os.path.join(app.root_path, "static", js_file)

        css_exists = os.path.exists(css_path)
        js_exists = os.path.exists(js_path)

        return f"""<pre>
=== Asset Resolution Debug ===

Manifest Locations:
  .vite/manifest.json: {manifest_vite_exists} ({manifest_vite})
  root manifest.json:  {manifest_root_exists} ({manifest_root})
  Using: {manifest_path}

Resolved URLs:
  CSS: {css_url}
  JS:  {js_url}

File Existence:
  CSS file exists: {css_exists} ({css_path})
  JS file exists:  {js_exists} ({js_path})

Status:
  {'✅ All assets resolved correctly' if (css_exists and js_exists) else '❌ Some assets missing - check build'}
</pre>"""

    return app


def initialize_extensions(app: Flask) -> None:
    """
    Initialize Flask extensions with the app instance.

    Per .clinerules security requirements:
    - SQLAlchemy for ORM (SQL injection prevention)
    - Flask-Login for session management
    - CSRF protection enabled globally
    """
    # Database
    db.init_app(app)

    # Database Migrations (Flask-Migrate)
    migrate.init_app(app, db)

    # Authentication (Flask-Login)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    # CSRF Protection (per .clinerules: enabled on ALL forms)
    csrf.init_app(app)

    # Optional: Flask-DebugToolbar in development
    if app.config.get("DEBUG_TB_ENABLED", False):
        try:
            from flask_debugtoolbar import DebugToolbarExtension

            DebugToolbarExtension(app)
        except ImportError:
            app.logger.warning("Flask-DebugToolbar not installed")


def register_blueprints(app: Flask) -> None:
    """
    Register application blueprints.

    Per .clinerules architecture:
    - auth: authentication & user management
    - resources: resource CRUD & search
    - bookings: booking flow & conflict detection
    - messages: user-to-user messaging
    - reviews: ratings & feedback
    - admin: dashboard, moderation, analytics
    """
    # Import blueprints (delayed import to avoid circular dependencies)
    from src.routes.auth import auth_bp
    from src.routes.resources import resources_bp
    from src.routes.bookings import bookings_bp
    from src.routes.reviews import reviews_bp
    from src.routes.messages import messages_bp
    from src.routes.admin import admin_bp
    from src.routes.concierge import concierge_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(resources_bp)
    app.register_blueprint(bookings_bp)  # Phase 6: Bookings
    app.register_blueprint(reviews_bp)  # Phase 6: Reviews
    app.register_blueprint(messages_bp)  # Phase 7: Messages
    app.register_blueprint(admin_bp)  # Phase 8: Admin Dashboard
    app.register_blueprint(concierge_bp)  # Phase 9: AI Concierge

    # Homepage route - redirect to appropriate page based on auth status
    @app.route("/")
    def index():
        from flask import redirect, url_for
        from flask_login import current_user

        if current_user.is_authenticated:
            # Redirect authenticated users to resources dashboard
            return redirect(url_for("resources.dashboard"))
        else:
            # Redirect unauthenticated users to login page
            return redirect(url_for("auth.login"))

    @app.route("/health")
    def health_check():
        """Health check endpoint for deployment monitoring."""
        return {"status": "healthy", "database": "connected" if db else "not initialized"}


def register_error_handlers(app: Flask) -> None:
    """
    Register custom error handlers for common HTTP errors.

    Per .clinerules: Error messages should NOT expose sensitive data.
    """
    from flask import render_template

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        app.logger.error(f"403 Forbidden error: {error}")
        return render_template("errors/403.html"), 403

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Rollback any failed transactions
        app.logger.error(f"Internal error: {error}")
        return render_template("errors/500.html"), 500

    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template("errors/401.html"), 401


def register_shell_context(app: Flask) -> None:
    """
    Register shell context for 'flask shell' command.

    Makes commonly used objects available in the Flask shell without imports.
    """
    # Import models (after app context is ready)
    from src.models import User, Resource, Booking, Message, Review

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "app": app,
            "User": User,
            "Resource": Resource,
            "Booking": Booking,
            "Message": Message,
            "Review": Review,
        }


def register_cli_commands(app: Flask) -> None:
    """
    Register custom CLI commands for database initialization and management.

    Usage:
        flask init-db    # Initialize database with tables
        flask seed-db    # Seed database with sample data (development only)
    """
    import click

    @app.cli.command("init-db")
    @click.option("--drop", is_flag=True, help="Drop existing tables before creating")
    def init_database(drop):
        """Initialize the database."""
        if drop:
            click.echo("Dropping existing tables...")
            db.drop_all()

        click.echo("Creating database tables...")
        db.create_all()
        click.echo("Database initialized successfully!")

    @app.cli.command("seed-db")
    def seed_database():
        """Seed database with sample data (development only)."""
        if not app.config.get("DEBUG"):
            click.echo("Error: This command is only available in development mode.")
            return

        click.echo("Seeding database with sample data...")
        # TODO: Implement seeding logic in Phase 11
        click.echo("Database seeding not yet implemented.")


# User loader for Flask-Login (required)
@login_manager.user_loader
def load_user(user_id: str):
    """
    Load user by ID for Flask-Login session management.

    Args:
        user_id: String representation of user's ID

    Returns:
        User object if found, None otherwise
    """
    from src.repositories.user_repo import UserRepository

    return UserRepository.get_by_id(int(user_id))


if __name__ == "__main__":
    """
    Run the application directly (development only).

    For production, use: gunicorn "src.app:create_app()"
    """
    app = create_app("development")
    app.run(host="0.0.0.0", port=5000, debug=True)
