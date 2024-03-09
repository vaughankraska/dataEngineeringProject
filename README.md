# Data engineering group project 2024
#### note: this is just how I have initialized the project, we can change any and all of this as needed
## Dataset
```text
Data:
https://zenodo.org/records/1043504#.Wzt7PbhXryo

```
## Instructions for working locally
#### for file-system (and enter interactive terminal):
```bash
docker run -it <image id of filesystem>
```

#### for spark:
```bash
cd pipeline/spark
docker run -h spark-master -p 3000:8080 -d <image id>
```

#### for the whole pipeline:
##### 
- starting the whole pipeline
```bash
cd pipeline

docker compose up
```
- submitting a example job (assumes the whole pipeline has been started and is running)
```bash
docker ps

docker exec -it <spark-master container id> /bin/bash

$SPARK_HOME/bin/spark-submit --class org.apache.spark.examples.SparkPi --master spark://spark-master:7077 $SPARK_HOME/examples/jars/spark-examples_2.12-3.5.1.jar
```
- cleaning up
```bash
docker compose down
```

# For submitting python scripts to VM's spark master:
- On your local machine, set up port forwarding to the VM
```bash
ssh -i ~/path/to/your/ssh/dir/Group_17_project.pem -L 8080:localhost:8080 \
        -L 9870:localhost:9870 \
        -L 7077:localhost:7077 \
        -L 9000:localhost:9000 \
        ubuntu@130.238.28.94
```
- Start a python notebook and run something like this to create a session:
```python
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.functions import *

spark_session = SparkSession\
        .builder\
        .master("spark://localhost:7077") \
        .appName("tessst")\
        .config("spark.dynamicAllocation.enabled", True)\
        .config("spark.dynamicAllocation.shuffleTracking.enabled",True)\
        .config("spark.shuffle.service.enabled", False)\
        .config("spark.dynamicAllocation.executorIdleTimeout","30s")\
        .getOrCreate()
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
