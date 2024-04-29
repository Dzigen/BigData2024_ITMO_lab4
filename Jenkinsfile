pipeline {
    agent any

    stages {
        stage('unit-testing') {
            steps {
                echo "Stage 1!"
                ls -la
            }
        }
        stage('building') {
            steps {
                echo "Stage 2!"
                ls -la
            }
        }
        stage('pushing to dockerhub') {
            steps {
                echo "Stage 3!"
                ls -la
            }
        }
    }
}        