FROM jenkins/jenkins:lts
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false

USER root
RUN apt-get update && apt-get install -y python3 python3-pip docker.io
RUN usermod -aG docker jenkins
USER jenkins

COPY plugins.txt .
RUN jenkins-plugin-cli -f /plugins.txt
COPY . .

EXPOSE 8080
EXPOSE 50000

# ENTRYPOINT [ "python3","logconfig.py" ]