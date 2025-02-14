import sys
from pyspark import SparkConf, SparkContext

if __name__ == "__main__":
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    
    R = sc.textFile(sys.argv[1])
    S = sc.textFile(sys.argv[2])
    
    Rkv = R.map(lambda t: (t.split(" ")[1], ['R',t.split(" ")[0]]))
    Skv = S.map(lambda t: (t.split(" ")[0], ['S',t.split(" ")[1]]))
    
    group = Rkv.union(Skv).groupByKey()
    
    
    def my_red(t):
        values_list = list(t[1])  # Convert ResultIterable to a list
        
        R_tuple = []
        S_tuple = []
        result = []
        
        for tuple in values_list:
            if tuple[0]=='R':
                R_tuple.append(tuple[1])
            elif tuple[0]=='S':
                S_tuple.append(tuple[1])
        if len(R_tuple)!=0 and len(S_tuple)!=0:
            for t1 in R_tuple:
                for t2 in S_tuple:
                    result.append([t1,t2])
        return result
    
    join = group.flatMap(my_red)    
    
    result = join.collect()
    print(result)
    
    sc.stop()