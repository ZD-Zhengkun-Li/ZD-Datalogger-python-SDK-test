CODE_CHANGE = getGitChanges()
pipeline{
  agent any
  enviorment{
    NEW_VERSION = "1.0.3"
    SERVER_CREDENTIALS = credentials('')
  }
  stages{
    stage("pull"){
      when{
        expression{
          BRANCH_NAME == "main" && CODE_CHANGE == true
        }
      }
      steps{
        sh echo 'Pull fnished'
        sh echo "version ${NEW_VERSION}"
      }
    }
    stage("test"){
      when{
        expression{
          BRANCH_NAME == "main"
        }
      }
      steps{
        sh "echo 'Test fnished'"
      }
    }
    stage("deploy"){
      steps{
        sh "echo 'deploy fnished'"
      }
    }
  }


}
