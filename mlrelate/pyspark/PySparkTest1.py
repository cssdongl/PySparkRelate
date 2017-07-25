from pyspark import SparkContext

sc = SparkContext("local[2]","test some spark context funcs")
rdd = sc.parallelize([("a",1),("a",2),("b",1)])
keyvaluerdd = rdd.countByKey().items()
value = sc.getConf().get("spark.dynamicAllocation.executorIdleTimeout")
print(value)
