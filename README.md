# Data engineering group project 2024
#### note: this is just how I have initialized the project, we can change any and all of this as needed
## Dataset
```text
Data:
http://millionsongdataset.com/

Description:
http://millionsongdataset.com/pages/example-track-description/

Full Data (280 GB):
http://millionsongdataset.com/pages/getting-dataset

Subset of data (1.8 GB):
http://millionsongdataset.com/pages/getting-dataset#subset

```
#### Instructions for working locally
for file-system (and enter interactive terminal):
```bash
docker run -it <image id of filesystem>
```
for spark:
```bash
$ docker run -h spark-master -p 3000:8080 -d <image id>
```




# How I am thinking this will work
```text
          +---------------------+
          | Job Submission VM   |
          +---------------------+
                  |
                  | Submit Spark Job
                  | (Data Path, Logic)
                  V
         +-------------------+         +-----------------------+
         | Spark Cluster      |         | HDFS Cluster with song data|
         +-------------------+         +-----------------------+
               |
               | Spark Session Creation
               V
          +---------+   +---------+   +---------+   +---------+
          |         |   |         |   |         |   |         |
          | Executor |   | Executor |   | Executor |   | Executor |
          +---------+   +---------+   +---------+   +---------+
                 |           |           |           |           |
                 | Partition 1 | Partition 2 | Partition 3 | Partition N |
                 | (In Memory) | (In Memory) | (In Memory) | (In Memory) |
                 |           |           |           |           |
                 V           V           V           V
            +---------+   +---------+   +---------+   +---------+
            |         |   |         |   |         |   |         |
            | Executor |   | Executor |   | Executor |   | Executor |
            +---------+   +---------+   +---------+   +---------+
                 |
                 | In-memory Processing
                 V
            +---------+   +---------+   +---------+   +---------+
            |         |   |         |   |         |   |         |
            | Executor |   | Executor |   | Executor |   | Executor |
            +---------+   +---------+   +---------+   +---------+
                 |
             Write Time Results (Back to HDFS or other storage)
```