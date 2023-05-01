FROM python:3.10

RUN groupadd --gid 1000 ggeasy && useradd --uid 1000 --gid ggeasy --shell /bin/bash -m ggeasy

RUN mkdir /root/server_dir

WORKDIR /root/server_dir

COPY Pipfile Pipfile.lock server.py run_server.sh ./

RUN mkdir database
RUN mkdir /home/ggeasy/.ssh

RUN pip install pipenv

RUN pipenv install --system --deploy

EXPOSE 5000

RUN apt update && apt upgrade -y
RUN apt-get install -y sudo
RUN apt install -y openssh-client
RUN apt install -y ssh
RUN apt install -y autossh
RUN apt-get install -y sqlite3 libsqlite3-dev

RUN chmod +x ./run_server.sh

ENTRYPOINT ["./run_server.sh"]