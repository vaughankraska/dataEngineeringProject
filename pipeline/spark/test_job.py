from pyspark.sql import SparkSession

# New API
spark_session = SparkSession.builder \
    .master("spark://localhost:7077") \
    .appName("DE_proj_script") \
    .config("spark.dynamicAllocation.enabled", True) \
    .config("spark.dynamicAllocation.shuffleTracking.enabled",True) \
    .config("spark.shuffle.service.enabled", True) \
    .config("spark.dynamicAllocation.executorIdleTimeout","30s") \
    .getOrCreate()


# Old API (RDD)
spark_context = spark_session.sparkContext

spark_context.setLogLevel("ERROR")

data = spark_context.textFile("hdfs://localhost:9000/user/ubuntu/corpus-webis-tldr-17.json")
json_df = spark.read.json(data)
json_df.printSchema()
instance_count = json_df.count()

print(f'num instances: {instance_count}')

spark_session.stop()