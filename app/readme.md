# k8s deployment exercise 1 

## in this repo you have 2 files one is a python falsk code and the other is the requirements

### the flask app 
#### you need to build dockerfile and build an image of this backend 
#### the server run on port 5200 
#### you need to download the packages usig pip install -r requimrements.txt after copy command
### run the flask app
#### you can enter the <host:port>**/welcome** resource to see the message hidden 
#### upload the image to your dockerhub repo

#k8s section
build a pod configuration app using yaml formant
and build a nodeport service so we can access the code from our pc
make the code runs on port 31311

delete the pod using kubectl command 
and now build a deployment app with 3 pods of your image 
build a nodeport service to access the code

