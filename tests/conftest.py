"""
Pytest Configuration and Fixtures - Campus Resource Hub
Provides shared fixtures for all test files.

Per .clinerules: Test fixtures for database and app context.
"""

import pytest
import os
import tempfile
from src.app import create_app, db as _db


@pytest.fixture(scope="function")
def app():
    """
    Create and configure a new app instance for each test function.

    Uses a temporary SQLite database that is deleted after each test.
    """
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()

    # Create app with testing config
    app = create_app("testing")
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            "WTF_CSRF_ENABLED": False,  # Disable CSRF for testing
        }
    )

    # Create database tables
    with app.app_context():
        _db.create_all()
        yield app

        # Cleanup: drop all tables and close connection
        _db.session.remove()
        _db.drop_all()

    # Close and remove the temporary database file
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def client(app):
    """
    Create a test client for the app.

    Useful for integration tests that need to make HTTP requests.
    """
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """
    Create a CLI runner for the app.

    Useful for testing CLI commands.
    """
    return app.test_cli_runner()
