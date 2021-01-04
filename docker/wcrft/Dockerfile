FROM clarinpl/cpp

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install ssh python-pip -y

RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
        python3.6-dev \
        morfeusz \
        crfpp \
        corpus2-python3.6 \
        morphanalyser \
        pwrutils \
        wccl-python3.6

WORKDIR /home/install
RUN git clone https://gitlab.clarin-pl.eu/syntactic-tools/morphological/wcrft2.git
RUN mkdir wcrft2/bin && \
    cd wcrft2/bin && \
    cmake .. && \
    make -j && \
    make install && \
    ldconfig && \
    cd /home/install && \
    rm -r ./wcrft2/

RUN pip install -i http://pypi.clarin-pl.eu iobber --trusted-host pypi.clarin-pl.eu

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT /entrypoint.sh
