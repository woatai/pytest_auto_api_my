pipeline {
    agent {
        label 'python-api'
    }

    options {
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
    }

    environment {
        VENV_DIR = '.venv-ci'
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        PYTHONDONTWRITEBYTECODE = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
            }
        }

        stage('Prepare Python') {
            steps {
                sh '''
                    set -eu
                    python3 -m venv "$VENV_DIR"
                    "$VENV_DIR/bin/python" -m pip install --upgrade pip
                    "$VENV_DIR/bin/python" -m pip install -r requirements.txt
                '''
            }
        }

        stage('Offline Tests') {
            steps {
                sh '''
                    set -eu
                    "$VENV_DIR/bin/python" -m pytest test_case/test_framework_basics.py -q -s
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report/tmp/**', allowEmptyArchive: true
        }
    }
}
