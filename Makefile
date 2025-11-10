# Campus Resource Hub - Makefile
# AiDD 2025 Capstone Project
#
# Per .clinerules: Commands for fmt (format), lint (type check), test, and run
# All commands should pass before committing code

.PHONY: help install fmt lint test test-cov run clean init-db seed-db shell check all web-assets

# Default target - show help
help:
	@echo "Campus Resource Hub - Available Make Commands"
	@echo "=============================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install      Install all dependencies from requirements.txt"
	@echo ""
	@echo "Code Quality (per .clinerules - run before commit):"
	@echo "  make fmt          Format code with black and ruff"
	@echo "  make lint         Run type checking with mypy"
	@echo "  make test         Run tests with pytest"
	@echo "  make test-cov     Run tests with coverage report"
	@echo "  make check        Run fmt + lint + test (full quality check)"
	@echo "  make all          Same as 'make check'"
	@echo ""
	@echo "Frontend Assets:"
	@echo "  make web-assets   Build Vite assets and verify manifest (Task B)"
	@echo ""
	@echo "Development:"
	@echo "  make run          Run Flask development server"
	@echo "  make shell        Open Flask shell with app context"
	@echo ""
	@echo "Database:"
	@echo "  make init-db      Initialize database (create tables)"
	@echo "  make seed-db      Seed database with sample data (dev only)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        Remove cache files, __pycache__, etc."
	@echo ""

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed successfully"

# Format code with black and ruff
fmt:
	@echo "🎨 Formatting code with black..."
	black src/ tests/ --line-length 100
	@echo "🔧 Formatting code with ruff..."
	ruff check src/ tests/ --fix
	@echo "✅ Code formatting complete"

# Type checking with mypy
lint:
	@echo "🔍 Running mypy type checking..."
	mypy src/ --ignore-missing-imports --no-strict-optional --disable-error-code=name-defined
	@echo "✅ Type checking complete"

# Run tests with pytest
test:
	@echo "🧪 Running tests with pytest..."
	PYTHONPATH=. pytest tests/ -v
	@echo "✅ Tests complete"

# Run tests with coverage
test-cov:
	@echo "🧪 Running tests with coverage..."
	PYTHONPATH=. pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
	@echo "✅ Tests complete - coverage report in htmlcov/index.html"

# Run full quality check (format + lint + test)
check: fmt lint test
	@echo "✅ All quality checks passed!"

# Alias for check
all: check

# Build and verify Vite assets (Task B: MAKE IT WORK IN RUNTIME)
web-assets:
	@echo "🏗️  Building Vite assets..."
	npm run build
	@echo ""
	@echo "✅ Vite build complete"
	@echo ""
	@echo "🔍 Verifying manifest..."
	@if [ -f "src/static/dist/.vite/manifest.json" ]; then \
		echo "✅ Manifest found: src/static/dist/.vite/manifest.json"; \
		echo ""; \
		echo "📄 Manifest contents:"; \
		cat src/static/dist/.vite/manifest.json | python -m json.tool | head -20; \
		echo ""; \
		echo "✅ Build verification complete"; \
	elif [ -f "src/static/dist/manifest.json" ]; then \
		echo "✅ Manifest found: src/static/dist/manifest.json"; \
		echo ""; \
		echo "📄 Manifest contents:"; \
		cat src/static/dist/manifest.json | python -m json.tool | head -20; \
		echo ""; \
		echo "✅ Build verification complete"; \
	else \
		echo "❌ ERROR: No manifest.json found!"; \
		echo "Expected locations:"; \
		echo "  - src/static/dist/.vite/manifest.json"; \
		echo "  - src/static/dist/manifest.json"; \
		exit 1; \
	fi
	@echo ""
	@echo "🧪 Testing asset resolution..."
	@echo "Run 'make run' and visit http://localhost:5001/_debug/assets to verify"

# Run Flask development server
run:
	@echo "🚀 Starting Flask development server..."
	@echo "📍 Server running at: http://localhost:5001"
	@echo "🛑 Press CTRL+C to stop"
	@echo "⚠️  Note: Using port 5001 to avoid AirPlay conflict on macOS"
	@echo ""
	FLASK_APP=src/app.py FLASK_ENV=development flask run --host=0.0.0.0 --port=5001 --reload

# Open Flask shell
shell:
	@echo "🐚 Opening Flask shell with app context..."
	FLASK_APP=src/app.py FLASK_ENV=development flask shell

# Initialize database
init-db:
	@echo "💾 Initializing database..."
	FLASK_APP=src/app.py FLASK_ENV=development flask init-db
	@echo "✅ Database initialized"

# Seed database with sample data
seed-db:
	@echo "🌱 Seeding database with sample data..."
	FLASK_APP=src/app.py FLASK_ENV=development flask seed-db
	@echo "✅ Database seeded"

# Drop and recreate database
reset-db:
	@echo "⚠️  Dropping and recreating database..."
	FLASK_APP=src/app.py FLASK_ENV=development flask init-db --drop
	@echo "✅ Database reset complete"

# Clean up cache files
clean:
	@echo "🧹 Cleaning up cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Show current Python and dependency versions
versions:
	@echo "📋 Current versions:"
	@echo "-------------------"
	@python --version
	@echo "Flask: $$(pip show flask | grep Version | cut -d' ' -f2)"
	@echo "SQLAlchemy: $$(pip show sqlalchemy | grep Version | cut -d' ' -f2)"
	@echo "pytest: $$(pip show pytest | grep Version | cut -d' ' -f2)"
	@echo ""

# Create necessary directories
dirs:
	@echo "📁 Creating project directories..."
	mkdir -p instance
	mkdir -p src/static/uploads
	mkdir -p src/static/css
	mkdir -p src/static/js
	mkdir -p tests
	mkdir -p .prompt
	mkdir -p docs/context/{APA,DT,PM,shared}
	@echo "✅ Directories created"

# Development workflow - format and test before committing
pre-commit: fmt lint
	@echo "✅ Pre-commit checks passed - safe to commit!"

# Production build check
build-check: clean check
	@echo "🏗️  Production build check passed!"
	@echo "Ready for deployment"
