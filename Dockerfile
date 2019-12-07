FROM ubuntu:latest
RUN apt-get update \
    && apt-get install -y \
        nmap \
        vim \
		python-pip
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
COPY requirements.txt requirements.txt
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install -r requirements.txt
CMD /bin/bash
