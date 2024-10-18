pipeline {
    agent any    
    environment {
        VENV_DIR = '/var/jenkins_home/workspace/Publicacion_POM/venv'
        APP_VERSION = '1.0.0'
        PLATFORM = 'Linux'
        BROWSER = 'Chrome'
    }
    stages {
        stage('Clean Up and Checkout ') {
            steps {
                deleteDir()
                //Clonar el repositorio Git
                git url: 'https://github.com/ericruizINE/Publicacion_POM.git', branch: 'main'
            }
        }
        stage('Install & Setup venv') {
            steps {
                // Instalar el paquete python3-venv si aún no está instalado
                sh 'apt-get update && apt-get install -y python3-venv'
                sh 'apt-get update && apt-get install -y python3-pip'
                sh "python3 -m venv ${VENV_DIR}"
            }
        }
        stage('Install Dependencies') {
            steps {
                // Activar el entorno virtual e instalar las dependencias
                sh """
                    . ${VENV_DIR}/bin/activate
                    pip install --no-cache-dir -r requirements.txt
                """
            }
        }
        stage('Preparar ambiente') {
            steps {
                script {
                    // Generar archivo environment.properties con variables de entorno
                    def alluredir = "tests/report"
                    sh "mkdir -p ${alluredir}"
                    sh """
                        echo 'APP_VERSION=${env.APP_VERSION}' >> ${alluredir}/environment.properties
                        echo 'PLATFORM=${env.PLATFORM}' >> ${alluredir}/environment.properties
                        echo 'BROWSER=${env.BROWSER}' >> ${alluredir}/environment.properties
                    """
                }
            }
        }
        stage('Descarga de Archivos CSV Presidencia') {
          steps {
            sh """
                    . ${VENV_DIR}/bin/activate > /dev/null 2>&1
                    pytest descarga.py --html=report.html --self-contained-html --alluredir=test/report
               """
          }
        }
        stage('Ejecutar Pytest Selenium POM') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                sh """
                    . ${VENV_DIR}/bin/activate > /dev/null 2>&1
                    cd tests
                    pytest --html=report.html --self-contained-html --alluredir=test/report
               """
                }
            }
        }
    }
    post {
        always {
            script {
                allure includeProperties: false, jdk: '', reportBuildPolicy: 'ALWAYS', results: [[path: 'test/report']]
                // Publica la URL del reporte en la consola de Jenkins
                def allureReportUrl = "${env.BUILD_URL}allure"
                echo "El reporte de Allure está disponible en: ${allureReportUrl}"
                def reportpy = "${env.BUILD_URL}execution/node/3/ws/tests/report.html"
                echo "El reporte de PYTest está disponible en: ${reportpy}"
            }
        }
    }
}
