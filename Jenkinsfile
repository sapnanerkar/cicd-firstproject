pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '-v /tmp:/tmp'
        }
    }

    environment {
        SLACK_CHANNEL = '#jenkins-alerts'
        DOCKER_REGISTRY = 'docker.io/yourusername'
        DOCKER_IMAGE = "${DOCKER_REGISTRY}/flask-tasks"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest --cov=app --cov-report=xml:coverage.xml --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                    cobertura 'coverage.xml'
                }
            }
        }

        stage('Build Docker Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-creds') {
                        docker.image("${DOCKER_IMAGE}:${env.BUILD_ID}").push()
                    }
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh "docker-compose -f docker-compose.staging.yml up -d"
                }
            }
        }

        stage('Approve Production') {
            when {
                branch 'main'
            }
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    input message: 'Deploy to production?'
                }
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh "kubectl apply -f k8s-deployment.yaml"
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '*/test-reports/.xml', allowEmptyArchive: true
            cleanWs()
        }
        success {
            slackSend(
                channel: env.SLACK_CHANNEL,
                message: "SUCCESS: Job ${env.JOB_NAME} #${env.BUILD_NUMBER}\n${env.BUILD_URL}"
            )
        }
        failure {
            slackSend(
                channel: env.SLACK_CHANNEL,
                message: "FAILED: Job ${env.JOB_NAME} #${env.BUILD_NUMBER}\n${env.BUILD_URL}"
            )
        }
    }
}