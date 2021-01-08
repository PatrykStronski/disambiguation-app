FROM rapidsai/rapidsai

ENV DOCKERIZE_VERSION v0.6.1

RUN umask 022
RUN apt update --fix-missing && apt -y upgrade
RUN apt-get install -y wget
RUN apt-get install -y ssh software-properties-common
RUN wget -O - http://sgjp.pl/apt/sgjp.gpg.key | apt-key add -
RUN apt-add-repository http://download.sgjp.pl/apt/ubuntu
RUN apt update
RUN apt install python-xmltodict -y
#RUN apt install morfeusz2 -y
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
WORKDIR /app
RUN pip install redis pandas numpy flask neo4j spacy pytest toolz xmltodict
#RUN pip install -U spacy[cuda]
RUN python -m spacy download en_core_web_sm
RUN apt -y install build-essential apt-transport-https lsb-release ca-certificates curl
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt -y install nodejs
RUN npm i -g pm2

#RUN wget http://download.sgjp.pl/morfeusz/20201227/Linux/18.04/64/morfeusz2-1.9.17-cp37-cp37m-linux_x86_64.whl
#RUN pip install ./morfeusz2-1.9.17-cp37-cp37m-linux_x86_64.whl
ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT /entrypoint.sh
