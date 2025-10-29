pipeline {
    agent any
        environment {
        DOCKER_IMAGE = 'arielk2511/first_asiingnment'
        BUILD_NUM = "${BUILD_NUMBER}"
    }
    stages {
        
    
    stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

    stage('Build and Push Docker Image') {
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
                // Ensure old container is removed
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p 8080:80 ${IMAGE_NAME}:latest
                '''
            }
        }
        
        stage('helth check') {
            steps {
                sh '''
                sleep 10
                curl http://localhost
                '''
            }
        }

        stage('deploy') {
            steps {
                echo '🚀 Deploying container...'
                // Ensure old container is removed
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p 8080:80 ${IMAGE_NAME}:latest
                '''
            }
        }
    }

     post {
        always {
            echo '🧹 Cleaning temporary resources...'
            sh 'docker system prune -f'
        }
    }
}
