from pyspark.sql import Row, functions as F
from pyspark.sql.window import Window
from pyspark import SparkContext
from pyspark.sql import SQLContext
sc = SparkContext("local[3]", "test data frame on 2.0")
rddData = sc.parallelize( (Row(c="class1", s=50), Row(c="class2", s=40), Row(c="class3", s=70), Row(c="class2", s=49), Row(c="class3", s=29), Row(c="class1", s=78)))
sqlContext = SQLContext(sc)
testDF = rddData.toDF()
result = (testDF.select("c", "s", F.row_number().over(Window.partitionBy("c").orderBy("s")).alias("rowNum")))
finalResult = result.where(result.rowNum <= 1).show()
