pipeline {
    agent any
    
    triggers {
        cron('0 22 * * *')   // Runs daily at exactly 10:00 PM
    }

    stages {

        stage('Check Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'behave -f allure_behave.formatter:AllureFormatter -o allure-results'
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure(
                    commandline: 'allure',
                    includeProperties: false,
                    results: [[path: 'allure-results']]
                )
            }
        }
    }
}
post {
        always {
            emailext(
                subject: "Build ${currentBuild.currentResult}: ${env.JOB_NAME}",
                body: """
                Build Status: ${currentBuild.currentResult}
                Job Name: ${env.JOB_NAME}
                Build Number: ${env.BUILD_NUMBER}

                Check Allure Report:
                ${env.BUILD_URL}allure/
                """,
                to: "vraghupathy@trellissoft.ai"
            )
        }
    }
}
