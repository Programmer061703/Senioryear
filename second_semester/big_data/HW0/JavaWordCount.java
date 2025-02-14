package sparkWC.spWC;

import java.util.Arrays;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;

public class JavaWordCount {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
	    JavaSparkContext sc = new JavaSparkContext("local[*]", "programname", 
	    		System.getenv("SPARK_HOME"), System.getenv("JARS"));

	    // Load the data
	    JavaRDD<String> data = sc.textFile("./pg100.txt");

	    // Parse the data into words
	    JavaRDD<String> words =
	          data.flatMap(line -> Arrays.asList(line.split(" ")).iterator());

	    // Convert each word into a tuple of its first letter and 1
	    JavaPairRDD<String, Integer> pairs =
	        words.mapToPair(word -> new Tuple2<>(word, 1));

	    // Sum the counts for each letter
	    JavaPairRDD<String, Integer> counts = pairs.reduceByKey((i1, i2) -> i1 + i2);
		
		// Save to disk
		counts.saveAsTextFile("./counts/");
		
		sc.stop();
	}

}
