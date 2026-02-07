pipeline {
    agent any
    
    environment {
        // Git repository configuration
        GIT_REPO_URL = 'ssh://git@github.com/BOBBY01151/DevOps_tuter.git'
        GIT_CREDENTIALS_ID = 'github-ssh-credentials'
        GIT_BRANCH = 'main'
        
        // Docker Hub password (WARNING: HARDCODED - NOT SECURE)
        DOCKER_PASSWORD = '2003$vimu'
        
        // Docker Hub username
        DOCKER_HUB_USERNAME = 'vimukthibuddika'
        
        // Docker image configuration
        DOCKER_IMAGE_NAME = 'firsttuter'
        DOCKER_IMAGE_TAG = 'latest'
        DOCKER_FULL_IMAGE = "${DOCKER_HUB_USERNAME}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
        
        // Local Docker image (already built)
        LOCAL_IMAGE = 'firsttuter:latest'
        LOCAL_IMAGE_ID = 'b5f12b34fae9'
        
        // Container configuration
        CONTAINER_NAME = 'firsttuter-app'
        CONTAINER_PORT = '3000'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "Checking out code from GitHub repository: ${GIT_REPO_URL}"
                echo "Branch: ${GIT_BRANCH}"
                
                // Checkout code from GitHub using SSH credentials
                git branch: "${GIT_BRANCH}",
                    credentialsId: "${GIT_CREDENTIALS_ID}",
                    url: "${GIT_REPO_URL}"
                
                // Display current commit info
                sh '''
                    echo "Current commit:"
                    git log -1 --oneline
                    echo "Repository status:"
                    git status
                '''
            }
        }
        
        stage('Docker Hub Login') {
            steps {
                echo 'Logging into Docker Hub...'
                // WARNING: Login using hardcoded password
                sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin'
            }
        }
        
        stage('Tag Docker Image') {
            steps {
                echo "Tagging local image ${LOCAL_IMAGE} for Docker Hub..."
                sh """
                    docker tag ${LOCAL_IMAGE} ${DOCKER_FULL_IMAGE}
                    docker tag ${LOCAL_IMAGE} ${DOCKER_HUB_USERNAME}/${DOCKER_IMAGE_NAME}:build-${BUILD_NUMBER}
                """
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                sh """
                    docker push ${DOCKER_FULL_IMAGE}
                    docker push ${DOCKER_HUB_USERNAME}/${DOCKER_IMAGE_NAME}:build-${BUILD_NUMBER}
                """
            }
        }
        
        stage('Stop Old Container') {
            steps {
                echo 'Stopping and removing old container if exists...'
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                """
            }
        }
        
        stage('Deploy Container') {
            steps {
                echo 'Deploying Docker container...'
                sh """
                    docker run -d \
                        -p ${CONTAINER_PORT}:${CONTAINER_PORT} \
                        --name ${CONTAINER_NAME} \
                        --restart unless-stopped \
                        ${LOCAL_IMAGE}
                """
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying application is running...'
                sh 'sleep 5'
                sh """
                    docker ps | grep ${CONTAINER_NAME}
                    curl -f http://localhost:${CONTAINER_PORT} || exit 1
                """
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline completed successfully!'
            echo "Docker image pushed to: ${DOCKER_FULL_IMAGE}"
            echo "Container ${CONTAINER_NAME} is running on port ${CONTAINER_PORT}"
        }
        failure {
            echo '❌ Pipeline failed!'
            sh """
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
            """
        }
        always {
            echo 'Logging out from Docker Hub...'
            sh 'docker logout || true'
            
            echo 'Cleaning up old Docker images...'
            sh """
                docker image prune -f
                docker images | grep ${DOCKER_IMAGE_NAME} | grep build- | awk '{print \$3}' | xargs -r docker rmi || true
            """
        }
    }
}
