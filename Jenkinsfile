pipeline {
  agent {
    docker {
      image 'docker:27.2.0-cli'                  // Docker CLI בלבד
      args '-v /var/run/docker.sock:/var/run/docker.sock'  // חיבור ל-daemon של ה-host
    }
  }

  environment {
    DOCKER_IMAGE = 'first_assignment'
    BUILD_NUM    = "${BUILD_NUMBER}"
    CONTAINER_NAME = 'first_assignment_container'
  }

  stages {
    stage('Checkout') {
      steps {
        echo '📥 Cloning repository...'
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          docker version
          docker build -t ${DOCKER_IMAGE}:latest .
          docker build -t ${DOCKER_IMAGE}:0.0.${BUILD_NUM} .
        '''
      }
    }

    stage('Run') {
      steps {
        sh '''
          docker rm -f ${CONTAINER_NAME} || true
          docker run -d --name ${CONTAINER_NAME} -p 8080:80 ${DOCKER_IMAGE}:latest
        '''
      }
    }

    stage('Health check') {
      steps {
        sh '''
          echo "🩺 Checking health..."
          sleep 10
          curl -fsS http://localhost:8080/ > /dev/null
        '''
      }
    }

    stage('Deploy (local prod)') {
      steps {
        sh '''
          docker rm -f ${CONTAINER_NAME}_prod || true
          docker run -d --name ${CONTAINER_NAME}_prod -p 8081:80 ${DOCKER_IMAGE}:latest
          echo "✅ Deployed to http://localhost:8081"
        '''
      }
    }
  }

  post {
    always {
      sh 'docker system prune -f || true'
    }
  }
}
