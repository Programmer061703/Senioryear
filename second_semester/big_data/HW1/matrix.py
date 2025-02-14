from pyspark import SparkContext


sc = SparkContext("local", "MatrixMultiplication")

# Load the data files
m_data = sc.textFile("./M.txt")
n_data = sc.textFile("./N.txt")

# 
m_kv = m_data.map(lambda line: line.strip().split(",")) \
             .map(lambda tokens: (tokens[1].strip(), (tokens[0].strip(), float(tokens[2]))))


n_kv = n_data.map(lambda line: line.strip().split(",")) \
             .map(lambda tokens: (tokens[0].strip(), (tokens[1].strip(), float(tokens[2]))))


joined = m_kv.join(n_kv)

partialProducts = joined.map(lambda x: ((x[1][0][0], x[1][1][0]),
                                          x[1][0][1] * x[1][1][1]))
result = partialProducts.reduceByKey(lambda a, b: a + b)

nonZeroResult = result.filter(lambda x: x[1] != 0)

# For example, collect and print the results (or save to a file)
for ((i, k), value) in nonZeroResult.collect():
    print("P[{}, {}] = {}".format(i, k, value))

# Stop the SparkContext when done
sc.stop()
