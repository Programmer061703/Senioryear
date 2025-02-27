import sys
 
from pyspark import SparkContext, SparkConf
 
if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    
    vector = []
    with open("./vector.txt", 'r') as f:
        for line in f.readlines():
            data = line.strip('\n')
            vector.append(float(data[0]))

    matrix = sc.textFile("./matrix.txt")
    elements = matrix.map(lambda l: l.split(","))
    
    kv = elements.map(lambda e: (int(e[0]), float(e[2])*vector[int(e[1])]))
    
    output = kv.reduceByKey(lambda n1, n2: n1 + n2)
    
    ec = output.collect()
    
    print(ec)
    
    sc.stop()