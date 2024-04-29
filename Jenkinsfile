pipeline {
    agent any

    stages {
        stage('unit-testing') {
            steps {
                script {
                    echo "Stage 1!"
                    ls -la
                }
            }
        }
        stage('building') {
            steps {
                script {
                    echo "Stage 2!"
                    ls -la
                }
            }
        }
        stage('pushing to dockerhub') {
            steps {
                script {
                    echo "Stage 3!"
                    ls -la
                }
            }
        }
    }
}        