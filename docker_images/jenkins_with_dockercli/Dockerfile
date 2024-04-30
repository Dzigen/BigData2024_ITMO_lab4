FROM jenkins/jenkins:latest

USER root

RUN curl -sSL https://get.docker.com/ | sh
RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose

RUN apt-get -y install pip && apt-get -y install python3-full
RUN python3 --version

RUN python3 -m venv /home/jenkins_venv
RUN . /home/jenkins_venv/bin/activate
RUN pip install --break-system-packages dvc
RUN pip install --break-system-packages dvc_gdrive

USER jenkins