#### If working in local machine, google colab please use below code
import time
import pandas as pd
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import matplotlib.pyplot as plt

start_time = time.time()
# Create a Spark session
spark = SparkSession.builder.appName("Swear_words_Frequency").getOrCreate()
# spark
spark_context = spark.sparkContext

### If working in Instances please use below code
# from pyspark.sql import SparkSession
# from operator import add

# spark_session = SparkSession\
#         .builder\
#         .master("spark://192.168.2.250:7077") \
#         .appName("Group_17")\
#         .config("spark.dynamicAllocation.enabled", True)\
#         .config("spark.dynamicAllocation.shuffleTracking.enabled",True)\
#         .config("spark.shuffle.service.enabled", False)\
#         .config("spark.dynamicAllocation.executorIdleTimeout","240s")\
#         .config("spark.executor.cores",2)\
#         .config("spark.driver.port",9999)\
#         .config("spark.blockManager.port",10005)\
#         .getOrCreate()

# # RDD API
# spark_context = spark_session.sparkContext

# spark_context.setLogLevel("OFF")
# json_file_path = 'new_small_corpus-webis-tldr-17.json'
# df = spark.read.json(f"hdfs://192.168.2.250:9000/{json_file_path}")


from pyspark.sql.functions import explode, split, desc, col, lower, when
from pyspark.ml.feature import StopWordsRemover
# Specify the path to your large JSON file
json_file_path = 'new_small_corpus-webis-tldr-17.json'

df = spark.read.json(json_file_path)

# print(df.take(1))
# Explode the array of words in the "content" column
# Split the 'content' column into an array of words
df_split = df.withColumn("content_array", split(col("content"), " "))

# print(df_split.take(1))
# Explode the array of words in the "content" column
df_exploded = df_split.select("id", "subreddit", explode("content_array").alias("word"))
# df_exploded.take(10)

# Apply the logic to preserve "I" and convert other words to lowercase
df_exploded_lower = df_exploded.withColumn("word", when(col("word") == "I", col("word")).otherwise(lower(col("word"))))
# df_exploded_lower.take(10)
# Filter out non-alphanumeric and null or spaces tokens if needed
df_filtered = df_exploded_lower.filter(~col("word").rlike("[^a-zA-Z0-9]")).filter(col("word").isNotNull() & (col("word") != ""))

# df_filtered.take(20)
## filter out stopwords
# stop_words = StopWordsRemover().getStopWords()
# df_filtered_stopWords = df_filtered.filter(~col("word").isin(stop_words))
# # df_filtered_stopWords.take(10)

# word_frequencies = df_filtered_stopWords.groupBy("word").count().sort(desc("count"))
# # Show the top words and their frequencies
# word_frequencies.show()

## filter out swear words
df_swear_list = ['anal', 'anus', 'arse', 'ass', 'balls', 'ballsack', 'bastard', 'biatch', 'bitch', 'bloody', 'blow job', 'blowjob', 'bollock', 'bollok', 'boner', 'boob', 'bugger', 'bum', 'butt', 'buttplug', 'clitoris', 'cock', 'coon', 'crap', 'cunt', 'damn', 'dick', 'dildo', 'dyke', 'f u c k', 'fag', 'feck', 'felching', 'fellate', 'fellatio', 'flange', 'fuck', 'fudge packer', 'fudgepacker', 'God damn', 'Goddamn', 'hell', 'homo', 'jerk', 'jizz', 'knob end', 'knobend', 'labia', 'lmao', 'lmfao', 'muff', 'nigga', 'nigger', 'omg', 'penis', 'piss', 'poop', 'prick', 'pube', 'pussy', 'queer', 's hit', 'scrotum', 'sex', 'sh1t', 'shit', 'slut', 'smegma', 'spunk', 'tit', 'tosser', 'turd', 'twat', 'vagina', 'wank', 'whore', 'wtf']
df_filtered_swearWords = df_filtered.filter(col("word").isin(df_swear_list))
# df_filtered_stopWords.take(10)

word_frequencies = df_filtered_swearWords.groupBy("word").count().sort(desc("count"))
# Show the top words and their frequencies
# word_frequencies.show()

# # Convert PySpark DataFrame to Pandas DataFrame for local plotting
# pandas_df = word_frequencies.limit(10).toPandas()

# # Plot the top word frequencies
# plt.figure(figsize=(10, 6))
# plt.bar(pandas_df["word"], pandas_df["count"])
# plt.xlabel("Words")
# plt.ylabel("Frequency")
# plt.title("Top Swear word Frequencies")
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()
# plt.show()
end_time = time.time()
### Time calculating and store results in csv
elapsed_time = end_time - start_time
print(f"Processing time: {elapsed_time} seconds")

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

word_frequencies.write.csv(f'word_frequencies_{timestamp}.csv', header=True, mode='overwrite')

# Save processing time to a CSV file using PySpark with timestamp
time_results = spark.createDataFrame([(timestamp, elapsed_time)], ["timestamp", "processing_time"])
time_results.write.csv(f'time_results_{timestamp}.csv', header=True, mode='overwrite')

# import pandas as pd

# csv_file_path = 'DirtyWords.csv'

# # Read the CSV file into a DataFrame
# df_swear_words = pd.read_csv(csv_file_path)

# df_swear_list = df_swear_words[df_swear_words['language'] == 'en']['word'].tolist()
# print(df_swear_list)

