"""
Integration tests for asset rendering in templates.

Verifies that Vite-built assets are correctly loaded on all pages.
Per task requirements:
- GET '/auth/login' and '/dashboard' should return 200
- HTML should contain '/static/dist/' and both '.css' and '.js' references
"""


def test_login_page_loads_assets(client):
    """Test that login page loads with proper asset URLs."""
    response = client.get("/auth/login")
    assert response.status_code == 200

    html = response.data.decode("utf-8")

    # Check that static/dist paths are present
    assert "/static/dist/" in html, "Asset URLs should include /static/dist/"

    # Check that CSS is loaded
    assert ".css" in html, "Page should load CSS assets"
    assert '<link rel="stylesheet"' in html, "Page should have stylesheet link tags"

    # Check that JS is loaded
    assert ".js" in html, "Page should load JavaScript assets"
    assert "<script" in html, "Page should have script tags"


def test_dashboard_page_loads_assets(client, app):
    """Test that dashboard page loads with proper asset URLs (authenticated)."""
    # Create a test user and login
    with app.app_context():
        from src.models import User
        from src.app import db

        # Create test user if not exists
        user = User.query.filter_by(email="test@example.com").first()
        if not user:
            user = User(name="Test User", email="test@example.com", role="student")
            user.set_password("testpass123")  # Use the setter method
            db.session.add(user)
            db.session.commit()

    # Login
    client.post(
        "/auth/login",
        data={"email": "test@example.com", "password": "testpass123"},
        follow_redirects=True,
    )

    # Access dashboard
    response = client.get("/dashboard")
    assert response.status_code == 200

    html = response.data.decode("utf-8")

    # Check that static/dist paths are present
    assert "/static/dist/" in html, "Asset URLs should include /static/dist/"

    # Check that CSS is loaded
    assert ".css" in html, "Page should load CSS assets"
    assert '<link rel="stylesheet"' in html, "Page should have stylesheet link tags"

    # Check that JS is loaded
    assert ".js" in html, "Page should load JavaScript assets"
    assert "<script" in html, "Page should have script tags"


def test_vite_asset_function_resolves_css(app):
    """Test that vite_asset() correctly resolves CSS entry."""
    with app.app_context():
        from src.utils.vite import vite_asset

        css_url = vite_asset("enterprise.css")

        # Should return a URL starting with /static/
        assert css_url.startswith("/static/"), f"CSS URL should start with /static/, got: {css_url}"

        # Should contain dist/assets/
        assert "/dist/assets/" in css_url, f"CSS URL should contain /dist/assets/, got: {css_url}"

        # Should end with .css
        assert css_url.endswith(".css"), f"CSS URL should end with .css, got: {css_url}"


def test_vite_asset_function_resolves_js(app):
    """Test that vite_asset() correctly resolves JS entry."""
    with app.app_context():
        from src.utils.vite import vite_asset

        js_url = vite_asset("app.js")

        # Should return a URL starting with /static/
        assert js_url.startswith("/static/"), f"JS URL should start with /static/, got: {js_url}"

        # Should contain dist/assets/
        assert "/dist/assets/" in js_url, f"JS URL should contain /dist/assets/, got: {js_url}"

        # Should end with .js
        assert js_url.endswith(".js"), f"JS URL should end with .js, got: {js_url}"


def test_debug_assets_endpoint(client):
    """Test that /_debug/assets endpoint works and shows asset status."""
    response = client.get("/_debug/assets")
    assert response.status_code == 200

    html = response.data.decode("utf-8")

    # Should show debug information
    assert "Asset Resolution Debug" in html, "Debug page should show header"
    assert "manifest.json" in html, "Debug page should mention manifest"
    assert "Resolved URLs" in html, "Debug page should show resolved URLs"

    # Should show CSS and JS URLs
    assert "CSS:" in html, "Debug page should show CSS URL"
    assert "JS:" in html, "Debug page should show JS URL"
