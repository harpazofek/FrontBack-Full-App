# Kubernetes Manifests for Jenkins Deployment
1. Create a Namespace
2. Create a service account with Kubernetes admin permissions.
3. Create local persistent volume for persistent Jenkins data on Pod restarts.
4. Create a deployment YAML and deploy it.
5. Create a service YAML and deploy it.
6. Access the Jenkins application on a Node Port.



###Setup Jenkins On Kubernetes Cluster###

Start with: kubectl delete -f .

Step 1: Create a Namespace for Jenkins. It is good to categorize all the devops tools as a separate namespace from other applications.
    kubectl create namespace 'any name spece you want'


Step 2: Create a serviceAccount.yaml file and copy the following admin service account manifest.
    kubectl apply -f serviceAccount.yaml

    The serviceAccount.yaml creates a jenkins-admin clusterRole, jenkins-admin ServiceAccount and binds the clusterRole to the service account.
    The jenkins-admin cluster role has all the permissions to manage the cluster components. You can also restrict access by specifying individual resource actions.


Step 3: Create volume.yaml and copy the following persistent volume manifest.
    Important Note: Replace worker-node01 with any one of your cluster worker nodes hostname.
    kubectl create -f volume.yaml
    or
    kubectl apply -f volume.yaml

    kubectl get svc --all-namespaces -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name,NODE_PORT:.spec.ports[*].nodePort"


    For volume, I have used the local storage class for the purpose of demonstration. Meaning, it creates a PersistentVolume volume in a specific node under /mnt location.

    As the local storage class requires the node selector, you need to specify the worker node name correctly for the Jenkins pod to get scheduled in the specific node.

    If the pod gets deleted or restarted, the data will get persisted in the node volume. However, if the node gets deleted, you will lose all the data.

    Ideally, you should use a persistent volume using the available storage class with the cloud provider or the one provided by the cluster administrator to persist data on node failures.

Step 4: Create a Deployment file named deployment.yaml and copy the following deployment manifest.
    In this Jenkins Kubernetes deployment we have used the following.

    securityContext for Jenkins pod to be able to write to the local persistent volume.
    Liveliness and readiness probe.
    Local persistent volume based on local storage class that holds the Jenkins data path /var/jenkins_home
    Note: The deployment file uses local storage class persistent volume for Jenkins data. For production use cases, you should add a cloud-specific storage class persistent volume for your Jenkins data. See the sample implementation of persistent volume for Jenkins in Google Kubernetes Engine

    If you don’t want the local storage persistent volume, you can replace the volume definition in the deployment with the host directory as shown below.

    volumes:
        - name: jenkins-data
            emptyDir: {}
    Create the deployment using kubectl.

    kubectl apply -f deployment.yaml
    Check the deployment status.

    kubectl get deployments -n k8s-jenkins
    Now, you can get the deployment details using the following command.

    kubectl  describe deployments --namespace=k8s-jenkins
    Also, You can get the details from the kubernetes dashboard as shown below.



Refer https://devopscube.com/setup-jenkins-on-kubernetes-cluster/ for step by step process to use these manifests.
