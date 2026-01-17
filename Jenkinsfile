pipeline {
  agent any

  environment {
    IMAGE = "sample-python-ci:${env.BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Trivy Repo Scan') {
      steps {
        sh '''
          set -e
          cd "${WORKSPACE}"
          trivy fs --no-progress --timeout 15m --skip-dirs .venv .
        '''
      }
    }

    stage('Build') {
      steps {
        sh 'make build'
      }
    }

    stage('Unit Tests') {
      steps {
        sh 'make test'
      }
    }

    stage('Sonar Check') {
      steps {
        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
          sh '''
            set -e
            export SONAR_PROJECT_KEY="${SONAR_PROJECT_KEY:-sample-jenkins-ci}"
            export SONAR_PROJECT_NAME="${SONAR_PROJECT_NAME:-sample-jenkins-ci}"
            export SONAR_PROJECT_VERSION="${BUILD_NUMBER}"
            export SONAR_HOST_URL="${SONAR_HOST_URL:-http://sonarqube:9000}"
            export SONAR_DOCKER_NETWORK="${SONAR_DOCKER_NETWORK:-sample-jenkins-ci_default}"
            docker run --rm \
              -e SONAR_HOST_URL \
              -e SONAR_TOKEN \
              -e SONAR_PROJECT_KEY \
              -e SONAR_PROJECT_NAME \
              -e SONAR_PROJECT_VERSION \
              --network "${SONAR_DOCKER_NETWORK}" \
              --volumes-from jenkins-ci \
              -w "${WORKSPACE}" \
              sonarsource/sonar-scanner-cli:5 \
              -Dsonar.projectKey="${SONAR_PROJECT_KEY}" \
              -Dsonar.projectName="${SONAR_PROJECT_NAME}" \
              -Dsonar.projectVersion="${SONAR_PROJECT_VERSION}" \
              -Dsonar.sources=app \
              -Dsonar.tests=tests \
              -Dsonar.python.coverage.reportPaths=coverage.xml
          '''
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'make build-docker IMAGE=${IMAGE}'
      }
    }

    stage('Create Git Tag') {
      when {
        allOf {
          branch 'main'
          expression { return env.CHANGE_ID == null }
        }
      }

      steps {
        withCredentials([usernamePassword(
          credentialsId: 'github-token',
          usernameVariable: 'GITHUB_USER',
          passwordVariable: 'GITHUB_TOKEN'
        )]) {
          sh '''
            set -e

            TAG="v1.0.${BUILD_NUMBER}"
            echo "Creating tag $TAG"

            git config user.name "jenkins"
            git config user.email "jenkins@local"

            git commit -m "Update deploy image tag to ${TAG}"
            git push https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/WilliameCorreia/sample-jenkins-ci.git HEAD:main

            git tag -a "$TAG" -m "Release $TAG"

            git push https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/WilliameCorreia/sample-jenkins-ci.git "$TAG"

            docker tag "${IMAGE}" "sample-python-ci:${TAG}"
          '''
        }
      }
    }

    stage('Trivy Image Scan') {
      steps {
        sh '''
          set -e
          trivy image --no-progress ${IMAGE}
        '''
      }
    }
  }

  post {
    always {
      sh 'docker images | head -n 20 || true'
    }
  }
}
