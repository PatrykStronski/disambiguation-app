FROM clarinpl/nlptools

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install ssh -y

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT /entrypoint.sh
