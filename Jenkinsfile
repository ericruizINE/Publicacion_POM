pipeline {
    agent any    
    environment {
        VENV_DIR = '/var/jenkins_home/workspace/Publicacion_POM/venv'
        APP_VERSION = '1.0.0'
        PLATFORM = 'Ubuntu/Linux'
        BROWSER = 'Versión chromedriver: 130.0.6723.69'
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
                    def pytestdir = "tests/pytestreport"
                    sh "mkdir -p ${pytestdir}"
                    sh """
                        echo 'APP_VERSION=${env.APP_VERSION}' >> ${alluredir}/environment.properties
                        echo 'PLATFORM=${env.PLATFORM}' >> ${alluredir}/environment.properties
                        echo 'BROWSER=${env.BROWSER}' >> ${alluredir}/environment.properties
                    """
                }
            }
        }
        stage('Ejecutar Pytest Selenium POM') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                sh """
                    . ${VENV_DIR}/bin/activate > /dev/null 2>&1
                    cd tests
                    pytest test_descarga_csv.py --html=pytestreport/report1.html --self-contained-html --alluredir=report
                    pytest test_public_page.py --html=pytestreport/report2.html --self-contained-html --alluredir=report
                    pytest test_public_tcsv.py --html=pytestreport/report3.html --self-contained-html --alluredir=report
                    pytest_html_merger -i /var/jenkins_home/workspace/Publicacion_POM/tests/pytestreport -o /var/jenkins_home/workspace/Publicacion_POM/tests/pytestreport/report.html
               """
                }
            }
        }
    }
    post {
        always {
            script {
                allure includeProperties: false, jdk: '', reportBuildPolicy: 'ALWAYS', results: [[path: 'tests/report']]
                // Publica la URL del reporte en la consola de Jenkins
                def allureReportUrl = "${env.BUILD_URL}allure"
                echo "El reporte de Allure está disponible en: ${allureReportUrl}"
                def reportpy = "${env.BUILD_URL}execution/node/3/ws/tests/pytestreport/report.html"
                echo "El reporte de Pytest está disponible en: ${reportpy}"
                archiveArtifacts artifacts: 'tests/report.html', allowEmptyArchive: true
                archiveArtifacts artifacts: 'tests/data/PRES_2024.csv', allowEmptyArchive: true
            }
        }
    }
}
