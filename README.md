FinalProject
1 - BUILD A PYTHON FLASK APP WITH A PING-PONG FUNCTION A PING PONG FUNCTION IS A GET FUNCTION THAT RECEIVES THE GET REQUEST AS A SERVER THE BODY OF THIS REQUEST IS A JSON WITH A CONTENT PING THE FLAK APP SHROUD RETURNS A 200 RESPONSE WITH A PONG JSON

2 - BUILD AN IMAGE THAT RUNS THE APPLICATION IN PORT 5005

3 - BUILD A CLUSTER IN MINIKUBE TO RUN 4 INSTANCES OF THIS CONTAINER

4 - THE INSTANCE SHOULD BE A DEPLOYMENT WITH A 4 REPLICAS USING ANSIBILE BUILD A CRON JOB IN JENKINS TO ADD 2 REPLICAS AT 8:00 AND DELETE 2 REPLICAS AT 13:00

DevSecOps Final Project (RED)

BY : Daniel , Eli Levy , Ofek , Lior

Prerequisite:

Launch EC2 instance - t2.medium ,2 cpu ,volume 30GB - os linux (ubuntu server 20.04) . Install : Docker , Minikube, Jenkins , Ansible , Git . In Jenkins install the kubernetes plugin . Edit the ~/.kube/config file (explained below) . Configure the Jenkins jobs . Configure the Ansible to create the Cron jobs .

Setup jenkins to work with Minikube *

setup the kube config file * cd ~/.kube
Nano config Presentation: https://docs.google.com/presentation/d/1MDQYuNCN6X-G2nUq_HQn7s7g8NwcqyNE

Config File:

Replace in the lines certificate-authority: , client-certificate , certificate-authority: add -date like so certificate-authority-data:

Instead of the path to the file replace with the actual key like so: $ Cat /home/eli/.minikube/ca.crt | base64 -w 0 ; echo And copy the outcome to the config file in the place of the path

Exposing pods in Minikube to world * Listen on port 5005 on all addresses, forwarding to 5005 in the pod : $ kubectl port-forward --address 0.0.0.0 deployment.apps/server-deploy 5005:5005
Use this config file in the Jenkins job that deployed in Minikube

Remove and add replicas from Minikube Run command to see running Pods: $ kubectl get all

If 4 replicas are running and you want to stop 2 kubectl scale --current-replicas=4 --replicas=2 deployment.apps/server-deploy

add 2 replicas from 2 to 4 kubectl scale --current-replicas=2 --replicas=4 deployment.apps/server-deploy

Jenkins jobs: ** clone git Finale project ** Source Code Management - git Repository URL: https://github.com/harpazofek/FinalProject Branch Specifier (blank for 'any')=*/main Build Steps - Execute shell : $ git status $git switch main $docker build -t eli/ping-pong .

** deploy-ping-pong ** Source Code Management : Git Repository URL = https://github.com/harpazofek/FinalProject To deploy the app we are using a cron job to build and push the latests to the claud

Build Environment: Credentials = the config file defined above Kubernetes API endpoint = https://192.168.49.2:8443 Cluster name = minikube Namespace = default Build Steps: Execute shell: $ kubectl apply -f ./K8S/* # You can change it to any file name inside the dir. $ sleep 5

** Add-2-replicas0800 **

Will be build from Ansible Build Triggers: Schedule: TZ=Asia/Jerusalem H 08 * * *

Build Environment: (As above)

Build Steps: Execute shell: $ export numRelicas=$(kubectl describe deployments server-deploy | grep available | awk '{print
Extra close brace or missing open brace
$2}' | head -n1)
$export newRelicasNum=$((
 kubectl scale --current-replicas=$numRelicas --replicas=$newRelicasNum deployment.apps/server-deploy

** Remove-2-replicas1300 ** As add 2 replicas Build Steps: Execute shell: $ export numRelicas=$(kubectl describe deployments server-deploy | grep available | awk '{print
Extra close brace or missing open brace
$2}' | head -n1)
$export newRelicasNum=$((
 kubectl scale --current-replicas=$numRelicas --replicas=$newRelicasNum deployment.apps/server-deploy

minikube start --extra-config=apiserver.service-node-port-range=5000-40000
