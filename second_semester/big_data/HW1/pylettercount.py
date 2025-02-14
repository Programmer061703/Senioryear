import sys
import re
from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    sc = SparkContext("local", "PySpark First Letter Word Count")

    def extract_words(line):
        # Use regex to extract words
        return re.findall(r'\b[a-zA-Z]+\b', line)

    words = sc.textFile("./pg100.txt").flatMap(extract_words)

    first_letters = words.map(lambda word: (word.lower()[0], 1))

    letter_counts = first_letters.reduceByKey(lambda a, b: a + b)

    sorted_counts = letter_counts.sortByKey()

    sorted_counts.saveAsTextFile("./letter_counts/")


    sc.stop()
