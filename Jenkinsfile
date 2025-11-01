pipeline {
  agent any
  options { skipDefaultCheckout(true) }

  environment {
    GITHUB_TOKEN = 'jenkins-dind'
    DOCKER_IMAGE    = 'first_assignment'
    BUILD_NUM       = "${BUILD_NUMBER}"
    CONTAINER_NAME  = 'first_assignment_dev'
    PROD_CONTAINER  = 'first_assignment_prod'
  }

    trigger {
      pollSCM('* * * * *')
    }

   stages {
    stage('Checkout') {
      steps {
        deleteDir()
        checkout([$class: 'GitSCM',
          branches: [[name: '*/main']],   // adjust if needed
          userRemoteConfigs: [[
            url: 'https://github.com/Ariel-ksenzovsky/devops_work_assignment_1.git',
            credentialsId: 'jenkins-dind' // <— use your ID (jenkins-dind) if that’s the one
          ]],
          extensions: [
            [$class: 'CleanBeforeCheckout'],
            [$class: 'PruneStaleBranch'],
            [$class: 'CloneOption', shallow: false, noTags: false, depth: 0, timeout: 30]
          ]
        ])
        sh 'git rev-parse --is-inside-work-tree && git log -1 --oneline'
      }
    }

    // ... your other stages unchanged ...
  }

    stage('Preflight: Docker available?') {
      steps {
        sh '''
          if ! command -v docker >/dev/null 2>&1; then
            echo "❌ docker CLI not found on this agent."
            echo "➡️  Map /var/run/docker.sock and install docker CLI."
            exit 127
          fi
          docker version
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          docker build -t ${DOCKER_IMAGE}:latest .
          docker build -t ${DOCKER_IMAGE}:0.0.${BUILD_NUM} .
        '''
      }
    }

    stage('Run (dev)') {
      steps {
        sh '''
          docker rm -f ${CONTAINER_NAME} || true
          docker run -d --name ${CONTAINER_NAME} -p 8080:80 ${DOCKER_IMAGE}:latest
        '''
      }
    }

    stage('Health check (dev)') {
      steps {
        sh '''
          echo "🩺 Checking http://localhost:8080 ..."
          for i in $(seq 1 12); do
            if curl -fsS http://localhost:8080/ >/dev/null; then
              echo "✅ Healthy"
              exit 0
            fi
            sleep 5
          done
          echo "❌ Health check failed"
          docker logs ${CONTAINER_NAME} || true
          exit 1
        '''
      }
    }

    stage('Deploy (local prod)') {
      steps {
        sh '''
          docker rm -f ${PROD_CONTAINER} || true
          docker run -d --name ${PROD_CONTAINER} -p 8081:80 ${DOCKER_IMAGE}:latest
          echo "✅ Deployed to http://localhost:8081"
        '''
      }
    }
  }

  post {
    always {
      echo '🧹 Cleanup...'
      script {
        try { sh 'docker system prune -f || true' } catch (ignored) {}
        try { cleanWs(cleanWhenNotBuilt: false) } catch (ignored) {}
      }
    }
  }
}
