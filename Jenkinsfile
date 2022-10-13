pipeline {
  agent any
  stages {
    stage('check code') {
      steps {
        git(url: 'https://github.com/Logeshwaran1507/youtube_app', branch: 'master')
      }
    }

    stage('test') {
      steps {
        sh 'docker build -f python/Dockerfile'
      }
    }

  }
}