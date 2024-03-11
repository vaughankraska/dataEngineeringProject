FROM ubuntu:22.04

RUN apt-get update --fix-missing
RUN apt-get -y upgrade

RUN apt-get install -y openjdk-17-jdk
RUN apt-get install -y python3-pip

RUN echo "export PYSPARK_PYTHON=python3" >> ~/.bashrc

RUN python3 -m pip install matplotlib 
RUN python3 -m pip install pyspark==3.5.1
RUN python3 -m pip install pandas
RUN python3 -m pip install numpy
RUN python3 -m pip install jupyterlab

WORKDIR /app
COPY test.ipynb .
COPY finn.ipynb .
EXPOSE 4040-4060 9999 8888 10005

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root"]
