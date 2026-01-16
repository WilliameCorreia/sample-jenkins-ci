IMAGE ?= sample-python-ci
WORKDIR ?= /app
VENV ?= .venv
PYTHON ?= $(VENV)/bin/python

build:
	@if [ ! -d "$(VENV)" ]; then python -m venv "$(VENV)"; fi
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install pytest pytest-cov

build-docker: build
	docker build -t $(IMAGE) .

test: build
	$(PYTHON) -m pytest --maxfail=1 --disable-warnings --cov=app --cov-report=term-missing --cov-report=xml

sonar:
	docker run --rm \
		-e SONAR_HOST_URL \
		-e SONAR_TOKEN \
		-e SONAR_PROJECT_KEY=sample-jenkins-ci \
		-e SONAR_PROJECT_NAME=sample-jenkins-ci \
		-e SONAR_PROJECT_VERSION=local \
		-v $(PWD):/usr/src \
		-w /usr/src \
		sonarsource/sonar-scanner-cli:5 \
		-Dsonar.projectKey=sample-jenkins-ci \
		-Dsonar.projectName=sample-jenkins-ci \
		-Dsonar.projectVersion=local \
		-Dsonar.sources=app \
		-Dsonar.tests=tests

trivy-repo:
	trivy fs --no-progress .

trivy-image:
	trivy image --no-progress $(IMAGE)
