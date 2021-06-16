CODE_CHANGE = getGitChanges()
pipeline{
  agent any
  enviorment{
    NEW_VERSION = "1.0.3"
    SERVER_CREDENTIALS = credentials('')
  }
  parameters{
    string(name:'version',defaultValue:'',description:'version to deploy')
    choice(name:'version',choices:['1.1.0','1.2.0'],description:'')
    boolParam(name:'executeTests',defaultValue:true,description:'')
  }
  stages{
    stage("pull"){
      when{
        expression{
          BRANCH_NAME == "main" && CODE_CHANGE == true
        }
      }
      steps{
        echo 'Pull fnished'
        echo "version ${NEW_VERSION}"
      }
    }
    stage("test"){
      when{
        expression{
          params.executeTests == true
        }
      }
      steps{
        echo 'Test fnished'
      }
    }
    stage("deploy"){
      steps{
        echo 'deploy fnished'
        echo "deployed version:${params.version}"
      }
    }
  }


}
