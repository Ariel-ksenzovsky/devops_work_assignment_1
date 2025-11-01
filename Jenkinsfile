pipeline {
  agent any

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '20'))
    disableConcurrentBuilds()
  }

  // Poll the GitHub repository every 2 minutes
  triggers {
    pollSCM('* * * * *')
  }

  environment {
    IMAGE_NAME     = 'myapp'
    IMAGE_TAG      = "0.0.${env.BUILD_NUMBER}"
    CONTAINER_NAME = 'myapp_container'
    APP_PORT       = '8080'   // internal port inside container
    HOST_PORT      = '8080'   // exposed port on host
  }

  stages {
    stage('Checkout') {
      steps {
        deleteDir()
        checkout scm
      }
    }

    stage('Verify Docker Installed') {
      steps {
        sh '''
          if ! command -v docker >/dev/null 2>&1; then
            echo "❌ Docker CLI not found. Please install Docker or mount /var/run/docker.sock."
            exit 127
          fi
          docker version
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          set -eux
          echo "🚀 Building Docker image..."
          docker build -t ${IMAGE_NAME}:latest -t ${IMAGE_NAME}:${IMAGE_TAG} .
          docker images | grep ${IMAGE_NAME}
        '''
      }
    }

    stage('Run Container') {
      steps {
        sh '''
          set -eux
          echo "🧹 Removing old container if exists..."
          docker rm -f ${CONTAINER_NAME} >/dev/null 2>&1 || true

          echo "🏃 Running new container..."
          docker run -d \
            --name ${CONTAINER_NAME} \
            -p ${HOST_PORT}:${APP_PORT} \
            --restart unless-stopped \
            ${IMAGE_NAME}:latest

          echo "✅ Container is now running:"
          docker ps --filter "name=${CONTAINER_NAME}"
        '''
      }
    }
  }

  post {
    always {
      echo "Build complete. Cleaning up old dangling images..."
      sh 'docker image prune -f || true'
    }
    success {
      echo "🎉 Build and run successful! Access your app at http://localhost:${HOST_PORT}"
    }
    failure {
      echo "❌ Build failed. Check logs above."
    }
  }
}
