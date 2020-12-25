FROM python:3.8

ENV DOCKERIZE_VERSION v0.6.1

RUN apt update && apt -y upgrade
RUN apt-get install -y wget

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN pip3 install --upgrade pip
RUN pip3 install redis pandas numpy flask neo4j spacy pytest rapids
RUN python3 -m spacy download en_core_web_sm
RUN apt -y install nodejs
RUN apt -y install npm
RUN npm i -g pm2

WORKDIR /app
ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT /entrypoint.sh
