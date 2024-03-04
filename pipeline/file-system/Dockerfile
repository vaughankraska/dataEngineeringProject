# dockerfile for our file system container/cluster (Hadoop)
FROM ubuntu:22.04
RUN apt-get update
RUN apt-get -y upgrade
RUN apt install -y openjdk-8-jre-headless
RUN apt-get -y install wget

# Setup Hadoop NameNode
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
RUN wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
RUN tar -zxvf hadoop-3.3.6.tar.gz
RUN mv hadoop-3.3.6 hadoop
RUN hadoop/bin/hdfs namenode -format
RUN hadoop/bin/hdfs --daemon start namenode
# TODO: configure the core-site.xml hdfs-site.xml file for both namenode and datanodes
# TODO: copy those files to docker container and run format
# TODO: start daemon and copy the music data to HDFS using the fs command from a volume *I think*
