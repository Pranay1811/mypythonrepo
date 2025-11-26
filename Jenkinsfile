pipeline {
  agent any

  environment {
    REGISTRY = "docker.io/yourdockerhubusername"   // change this
    IMAGE_NAME = "${REGISTRY}/add-python"
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    DOCKER_CREDENTIALS_ID = "docker-hub-creds"
    KUBECONFIG_CREDENTIALS_ID = "kubeconfig-creds"
    K8S_NAMESPACE = "test"
    K8S_DEPLOYMENT = "add-app-deployment"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install & Unit tests') {
      steps {
        sh '''
          python -m venv venv
          . venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          pytest -q
        '''
      }
    }

    stage('Build Docker image') {
      steps {
        script {
          def image = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
          docker.withRegistry("https://${REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
            image.push()
            image.push('latest')
          }
        }
      }
    }

    stage('Deploy to k8s (test)') {
      steps {
        withKubeConfig([credentialsId: "${KUBECONFIG_CREDENTIALS_ID}"]) {
          sh """
            # try updating the image; if deployment not exists, apply manifests
            set -e
            kubectl -n ${K8S_NAMESPACE} get deployment ${K8S_DEPLOYMENT} >/dev/null 2>&1 && \
              kubectl -n ${K8S_NAMESPACE} set image deployment/${K8S_DEPLOYMENT} add-app-deployment=${IMAGE_NAME}:${IMAGE_TAG} || \
              kubectl apply -f k8s/deployment.yaml -n ${K8S_NAMESPACE} && kubectl apply -f k8s/service.yaml -n ${K8S_NAMESPACE}
            kubectl rollout status deployment/${K8S_DEPLOYMENT} -n ${K8S_NAMESPACE}
            kubectl get pods -n ${K8S_NAMESPACE} -o wide
          """
        }
      }
    }
  }

  post {
    success {
      echo "Successfully built and deployed ${IMAGE_NAME}:${IMAGE_TAG}"
    }
    failure {
      echo "Pipeline failed"
    }
  }
}
