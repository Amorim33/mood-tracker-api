# Python virtual environment
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# Use env variable PORT or default to 8080
API_PORT=$(if $(PORT),$(PORT),8080)

# Create virtual environment and setup application
venv:
	@echo "Creating virtual environment..."
	python3.10 -m venv $(VENV)
	@echo "Virtual environment created."
	make setup
	@echo "Setup complete."

# Setup application and install dependencies
setup:
	@echo "Setting up application..."
	${PIP} install -U pip==23.2.1
	${PIP} install -U pip-tools==7.3.0
	make install

# Install dependencies
install:
	@echo "Installing dependencies..."
	$(VENV)/bin/pip-sync requirements.txt dev-requirements.txt
	@echo "Done!"

# Run api in development mode
api:
	${PYTHON} -m uvicorn app.main:app --reload --port $(API_PORT)

# Run tests
test:
	${PYTHON} -m pytest -v

# Run coverage for application tests
coverage:
	${PYTHON} -m coverage run -m pytest
	${PYTHON} -m coverage report -m

# Format code style
format:
	${PYTHON} -m black .
	${PYTHON} -m ruff --fix .

# Run lint
lint:
	${PYTHON} -m ruff .
	${PYTHON} -m black . --check

# Generate lock file for dependencies
generate-requirements:
	@echo "Generating requirements.txt..."
	$(VENV)/bin/pip-compile requirements.in && $(VENV)/bin/pip-compile dev-requirements.in
	@echo "Done!"