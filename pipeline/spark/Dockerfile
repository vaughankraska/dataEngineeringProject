# spark cluster docker file
# NOTE: we can change this to use the official docker image at https://hub.docker.com/r/apache/spark-py/tags
FROM ubuntu:22.04

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install pyspark

RUN apt-get install -y openjdk-17-jre-headless scala screen wget

WORKDIR home/ubuntu
RUN wget https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
RUN tar xvf spark-3.5.1-bin-hadoop3.tgz && mkdir spark && mv spark-3.5.1-bin-hadoop3/* spark/ && rm -rf spark-3.5.1-bin-hadoop3 spark-3.5.1-bin-hadoop3.tgz

ENV SPARK_HOME="spark"
ENV PATH="${PATH}:$SPARK_HOME/bin"
ENV SPARK_NO_DAEMONIZE="true"
ENV PYSPARK_PYTHON=python3
EXPOSE 8080 7077
CMD $SPARK_HOME/sbin/start-master.sh & $SPARK_HOME/sbin/start-worker.sh spark://spark-master:7077
