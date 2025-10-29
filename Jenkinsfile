pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'first_assignment'
        BUILD_NUM = "${BUILD_NUMBER}"
        CONTAINER_NAME = 'first_assignment_container'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Cloning repository...'
                checkout scm
            }
        }

        stage('Install Docker') {
            steps {
                echo '🐳 Installing Docker (if not installed)...'
                sh '''
                    if ! command -v docker >/dev/null 2>&1; then
                        echo "Docker not found. Installing..."
                        apt-get update -y
                        apt-get install -y ca-certificates curl gnupg lsb-release
                        mkdir -p /etc/apt/keyrings
                        curl -fsSL https://download.docker.com/linux/$(. /etc/os-release && echo "$ID")/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
                        echo \
                          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
                          https://download.docker.com/linux/$(. /etc/os-release && echo "$ID") \
                          $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
                        apt-get update -y
                        apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
                        systemctl start docker || true
                    else
                        echo "✅ Docker already installed."
                        docker --version
                    fi
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo '🏗️ Building Docker image...'
                    sh '''
                        docker build -t ${DOCKER_IMAGE}:latest .
                        docker build -t ${DOCKER_IMAGE}:0.0.${BUILD_NUM} .
                    '''
                }
            }
        }

        stage('Run') {
            steps {
                echo '🚀 Running container...'
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p 8080:80 ${DOCKER_IMAGE}:latest
                '''
            }
        }

        stage('Health check') {
            steps {
                sh '''
                    echo '🩺 Checking health...'
                    sleep 10
                    curl -fs http://localhost:8080 || (echo "Health check failed" && exit 1)
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo '🚢 Deploying container...'
                sh '''
                    docker rm -f ${CONTAINER_NAME}_prod || true
                    docker run -d --name ${CONTAINER_NAME}_prod -p 8081:80 ${DOCKER_IMAGE}:latest
                    echo "✅ Deployed successfully to local prod (http://localhost:8081)"
                '''
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning temporary resources...'
            sh 'docker system prune -f || true'
        }
    }
}
