# Data engineering group project 2024
<i>authors: Finn Vaughankraska, Oscar Boman (@osbo8060), Yagna Karthik Vaka (@Karthik1000)</i>
### Warning: Running the project will download a ~20GB data file automatically. Also, the purpose of the query written in the pyspark was to find subreddits with hate speech and slurs. The file contains offensive language.

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
ssh -i ~/path/to/your/ssh/dir/YOUR_PEM_FILE.pem -L 8080:localhost:8080 \
        -L 9870:localhost:9870 \
        -L 7077:localhost:7077 \
        -L 8888:localhost:8888 \
        ubuntu@host.ip.address
```
- note: if you do not want to run this on a host machine and want to run this locally, you can ignore the above step. and instead just run the docker compose commands.
- Open the jupyter lab on port 8888, get access via the token, and run something like this to create a session:
```python
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.functions import *

spark_session = SparkSession \
    .builder \
    .master("spark://spark-master:7077") \
    .appName("Finn Test") \
    .config("spark.dynamicAllocation.enabled", True) \
    .config("spark.dynamicAllocation.shuffleTracking.enabled",True) \
    .config("spark.shuffle.service.enabled", False) \
    .config("spark.driver.port", 9999) \
    .config("spark.blockManager.port", 10005) \
    .config("spark.dynamicAllocation.executorIdleTimeout","30s") \
    .getOrCreate()
```
- note: there should be two scripts loaded into the driver automatically so visiting localhost:8888 will put you in the driver containers jupyter instane with two files there.
- note: there is no volume attached to the driver so restarting the container will delete changes you make in the driver's notebook files.
# Architecture

```text
          +-------------------------------+
          | Spark Driver VM (submits jobs)|
          +-------------------------------+
                  |
                  | Submit Spark Job
                  V
         +-------------------+         +-------------------------------+
         | Spark Cluster     |  <--->  | HDFS Cluster with reddit data |
         +-------------------+         +-------------------------------+
               |
               | Spark Session Creation
               V
          +---------+   +---------+   +---------+   +---------+
          |         |   |         |...|         |   |         |
          | Worker  |   | Worker  |   | Worker  |   | Worker  |
          +---------+   +---------+   +---------+   +---------+
                 |           |           |           |         |
                 |
             Write Time Results (Back to HDFS or other storage)
```
