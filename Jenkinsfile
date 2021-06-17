pipeline {
    agent {
        dockerfile true
    }
    environment {
        CI = 'true'
    }
    stages {
        stage('CheckEnv') {
            steps {
                sh 'python --version'
                sh 'ls'
		        sh 'make -v'
                sh 'git submodule update --init --recursive'
                sh  """
                        git checkout .
                        git checkout origin/${GIT_BRANCH}
                        git checkout -B buildbranch origin/${GIT_BRANCH}
                    """
            }
        }
    
        stage('Build') { 
            steps { 
	    sh  '''
            cd ..
            mkdir -p Downloads
            cd Downloads
            wget https://releases.linaro.org/components/toolchain/binaries/latest-7/aarch64-linux-gnu/gcc-linaro-7.5.0-2019.12-x86_64_aarch64-linux-gnu.tar.xz
            tar -C /opt -xf gcc-linaro-7.5.0-2019.12-x86_64_aarch64-linux-gnu.tar.xz
            echo 'export PATH=/opt/gcc-linaro-7.5.0-2019.12-x86_64_aarch64-linux-gnu/bin/:$PATH' >> ~/.bashrc
            '''
         sh  '''
            mkdir -p build
            cd build
            cmake ..
            make
            '''
        sh  '''
            mkdir -p build-aarch64
            cd build-aarch64
            cmake .. -DVCPKG_TARGET_TRIPLET=arm64-linux -DCMAKE_CXX_COMPILER=aarch64-linux-gnu-g++ -DCMAKE_C_COMPILER=aarch64-linux-gnu-gcc -DCMAKE_SYSTEM_PROCESSOR=aarch64 -DCMAKE_SYSTEM_NAME=Linux
            make
		    '''
            }
        }
        stage('Test') { 
            steps {
                 echo 'Testing..'
            }
        }
        stage('Pack') { 
        
            steps {
                 script {
                    def date_time = "${BUILD_TIMESTAMP}"
                    def file_name = 'version'

                    def tag_name = ''
                    def zip_name = ''
                      sh """
                        if test -f $file_name; then
                          echo "$file_name exists."
                        else 
                           echo "$file_name does not exists."
                        fi
                        """
                    def version_number = readFile(file: 'version').trim()

                 
                    tag_name = version_number + '-' + env.GIT_BRANCH + '-' + 'build' + date_time
                    zip_name = "zdbox2-soad-tcp-" + "$tag_name" + ".zip"   
                    
                     sh  """ 
                          git tag $tag_name
                          git push https://zd-server-hp1:ZDautomotive888@github.com/ZDAutomotive/zdbox2-soad-tcp.git HEAD:${GIT_BRANCH} --tags
                         """ 
                    
                    sh  """ 
                            mkdir -p to_zip
                            cp -r artifact ./to_zip
                            cp -r Makefile.mk ./to_zip
                            cp -r example ./to_zip
                            cd to_zip
                            touch version.txt
                            echo "$tag_name" > version.txt
                            zip -r $zip_name .
                        """
                }
            }
        }

        stage('Deliver') {
            steps {
                script {
                    archiveArtifacts artifacts: 'to_zip/*.zip', fingerprint: true
                    
                   
                    sh "rm -r to_zip"
                }
            }
        }
        stage('End') {
            steps{
                sh  """
                        git checkout origin/${GIT_BRANCH}
                    """
            }
        }
    }
}
