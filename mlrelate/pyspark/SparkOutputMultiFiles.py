from pyspark import SparkContext
from pyspark.sql import SQLContext
sc = SparkContext("local[5]","multi fie ouputs on spark2.1")
people_rdd = sc.parallelize([(1,'alice'),(1,'alex'),(2,'Charle')])
sqlContext = SQLContext(sc)

people_df = people_rdd.toDF(["number","name"])
people_df.write.partitionBy("number").text("people")
people_df.write.partitionBy("number").json("people-json")
people_df.write.partitionBy("number").parquet("people-parquet")

