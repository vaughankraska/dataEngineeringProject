# Data engineering group project 2024
#### note: this is just how I have initialized the project, we can change any and all of this as needed
## Dataset
```text
Data:
https://zenodo.org/records/1043504#.Wzt7PbhXryo

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

# Architecture
```text
          +-------------------------------+
          | Spark Driver VM (submits jobs)|
          +-------------------------------+
                  |
                  | Submit Spark Job
                  | (Data Path, Logic)
                  V
         +-------------------+         +-------------------------------+
         | Spark Cluster      |  <--->  | HDFS Cluster with reddit data|
         +-------------------+         +-------------------------------+
               |
               | Spark Session Creation
               V
          +---------+   +---------+   +---------+   +---------+
          |         |   |         |   |         |   |         |
          | Worker  |   | Worker  |   | Worker  |   | Worker  |
          +---------+   +---------+   +---------+   +---------+
                 |           |           |           |         |
                 |
             Write Time Results (Back to HDFS or other storage)
```
