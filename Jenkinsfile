
pipeline {
    agent any

    stages {
         stage("build") {
            steps {
                echo 'building the application ...'
                sh '''
                docker --version
                docker compose version
            }
         }
         stage("test") {
            steps {
                echo 'test the application test...'
            }
         }
         stage("deploy") {
            steps {
                echo 'deploy the application ...'
            }
         }
    }
}
