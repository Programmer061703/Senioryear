import sys
from pyspark import SparkConf, SparkContext

def my_split(line):
    return line.split(" ")

def my_map(word):
    return (word, 1)
    
def my_sum(x, y):
    return x + y

if __name__ == "__main__":
    conf = SparkConf()
    sc = SparkContext(conf=conf)

    lines = sc.textFile(sys.argv[1])

    words = lines.flatMap(my_split)
    pairs = words.map(my_map)

    counts = pairs.reduceByKey(my_sum)

    counts.saveAsTextFile(sys.argv[2])
    sc.stop()