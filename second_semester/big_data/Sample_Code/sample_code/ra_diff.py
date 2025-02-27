import sys
from pyspark import SparkConf, SparkContext

if __name__ == "__main__":
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    
    R = sc.textFile(sys.argv[1])
    S = sc.textFile(sys.argv[2])
    
    Rkv = R.map(lambda t: (t,'R'))
    Skv = S.map(lambda t: (t,'S'))
    
    group = Rkv.union(Skv).groupByKey()
    
    def my_red(t):
        values_list = list(t[1])  # Convert ResultIterable to a list
        if len(values_list) == 1 and values_list[0] == 'R':
            return [t[0]]  # Return a list with the key to match flatMap expectations
        else:
            return []
    
    diff = group.flatMap(my_red)
    
    result = diff.collect()
    print(result)
    
    sc.stop()