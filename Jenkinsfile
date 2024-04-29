pipeline {
    agent any

    environment {
        GIT_SSH_KEY = credentials('github_bigdata2024_itmo')  // ID of the SSH key added in Jenkins credentials
        GIT_REPO_URI = "git@github.com:Dzigen/BigData2024_ITMO_lab1.git" 
    }

    stages {
        stage('Checkout from GitHub') {
            steps {
                script {
                    // Define custom GIT SSH command
                    sh "ssh-agent bash -c 'ssh-add ${GIT_SSH_KEY}; git clone ${GIT_REPO_URI}'"
                }
            }
        }
    }
}        