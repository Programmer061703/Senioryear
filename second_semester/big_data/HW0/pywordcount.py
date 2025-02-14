import sys
 
from pyspark import SparkContext, SparkConf
 
if __name__ == "__main__":
    
    # create Spark context with necessary configuration
    sc = SparkContext("local","PySpark Word Count Exmaple")
    
    # read data from text file and split each line into words
    
    def func(line):
        return line.split(" ")
        
    words = sc.textFile("./pg100.txt").flatMap(func)
    
    # count the occurrence of each word
    wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)
    
    # save the counts to output
    wordCounts.saveAsTextFile("./counts/")
    sc.stop()