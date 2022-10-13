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
        sh 'cd python python3 app.py'
      }
    }

  }
}