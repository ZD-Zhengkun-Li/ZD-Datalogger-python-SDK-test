
pipeline{
  agent {
  docker { image 'node:14-alpine' }

  stages{
    stage("pull"){
     
      steps{
        echo 'Pull fnished'
        echo '...'
      }
    }
 
    stage("test"){
     
      steps{
        echo 'test fnished'
      }
    } 
    stage("deploy"){
     
      steps{
        echo 'deploy fnished'
      }
    }
  }
}
