# dockerfile for our file system container/cluster (Hadoop)
FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y openjdk-17-jre-headless
RUN apt-get install -y net-tools
RUN apt-get install -y wget

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64/

ARG HADOOP_DIST_ADRESS=https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
WORKDIR /home/ubuntu
RUN wget $HADOOP_DIST_ADRESS && tar -xzf hadoop-3.3.6.tar.gz && rm -rf hadoop-3.3.6.tar.gz
RUN mkdir hadoop && mv hadoop-3.3.6/* hadoop/ && rm -rf hadoop-3.3.6
RUN hadoop/bin/hadoop version

# TODO: configure the core-site.xml hdfs-site.xml file for both namenode and datanodes
# TODO: copy those files to docker container and run format
# TODO: start daemon and copy the music data to HDFS using the fs command from a volume *I think*