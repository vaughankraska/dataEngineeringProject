FROM ubuntu:22.04

# Update and install required packages
RUN apt-get update && apt-get -y upgrade && \
    apt-get -y install openjdk-8-jre-headless wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Setup Java environment
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
ENV PATH=$JAVA_HOME/bin:$PATH

# Download and setup Hadoop
RUN wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz && \
    tar -zxvf hadoop-3.3.6.tar.gz && \
    rm hadoop-3.3.6.tar.gz

RUN wget https://github.com/osbo8060/hadoopfiles/archive/refs/heads/main.zip
RUN unzip *.zip

# Copy modified configuration files into Hadoop configuration directory
RUN mv hadoopfiles-main/core-site.xml /hadoop-3.3.6/etc/hadoop/core-site.xml
RUN mv hadoopfiles-main/hdfs-site.xml /hadoop-3.3.6/etc/hadoop/hdfs-site.xml

# Format HDFS and start NameNode
RUN /hadoop-3.3.6/bin/hdfs namenode -format && \
    /hadoop-3.3.6/bin/hdfs --daemon start namenode
