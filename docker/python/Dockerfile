FROM rapidsai/rapidsai

ENV DOCKERIZE_VERSION v0.6.1

RUN apt update && apt -y upgrade
RUN apt-get install -y wget

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

WORKDIR /app
RUN pip install neo4j pytest
RUN conda install redis pandas flask spacy
RUN python -m spacy download en_core_web_sm
RUN apt -y install build-essential apt-transport-https lsb-release ca-certificates curl
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt -y install nodejs
RUN npm i -g pm2

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT /entrypoint.sh
