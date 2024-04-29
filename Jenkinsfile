pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS=credentials('dockerhub_creds')
        LC_ALL = "en_US.UTF-8"
        LANG    = "en_US.UTF-8"
        LANGUAGE = "en_US.UTF-8"
    }

    stages {
        stage('Cloning github-repository'){
            steps{
                cleanWs()
                sh 'git clone -b main https://github.com/IcyAltair/mle-template.git'
                sh 'ls -la'
            }
        }
        
        stage('Building ModelAPI-image') {
            steps {
                echo "Stage 2!"
                sh 'docker --version'
            }
        }
        stage('Run Unit-test') {
            steps {
                echo "Stage 1!"
                echo "Hello World again!"
            }
        }
        stage('Push ModelAPI-image to DockerHub') {
            steps {
                echo "Stage 3!"
            }
        }
    }
}        