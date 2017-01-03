from mlrelate.pyspark import SparkContext
sc = SparkContext("local[3]", "First Spark App")
data = sc.textFile("file:///home/hadoop/testFiles/pythonTest/userPhcaseHistory.txt").map(lambda line:line.split(",")).map(lambda record: (record[0], record[1], record[2]))
numPurchases = data.count()
uniqueUsers = data.map(lambda record: record[0]).distinct().count()
totalRevenue = data.map(lambda record: float(record[2])).sum()
products = data.map(lambda record: (record[1], 1.0)).reduceByKey(lambda a, b: a + b).collect()
mostPopular = sorted(products, key=lambda x: x[1], reverse=True)[0]
print "Total purchases: %d" % numPurchases
print "Unique users: %d" % uniqueUsers
print "Total revenue: %2.2f" % totalRevenue
print "Most popular product: %s with %d purchases" % (mostPopular[0], mostPopular[1])