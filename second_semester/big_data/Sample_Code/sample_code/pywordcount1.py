import sys
from pyspark import SparkConf, SparkContext

if __name__ == "__main__":
    conf = SparkConf()
    sc = SparkContext(conf=conf)

    lines = sc.textFile(sys.argv[1])

    words = lines.flatMap(lambda l: l.split("[^\\w]+"))
    pairs = words.map(lambda w: (w, 1))

    counts = pairs.reduceByKey(lambda n1, n2: n1 + n2)

    counts.saveAsTextFile(sys.argv[2])
    sc.stop()