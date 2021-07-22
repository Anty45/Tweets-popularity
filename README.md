# Twitter - NLP - Data Mining

## Tableau visualization 
![alt text](https://github.com/Anty45/FIL-ROUGE/blob/master/scripts/tableau_viz/Twitter%20%23tableau.png?raw=true)

## __Pipeline :__ 
* Get Twitter accreditations
* Setup Zookeeper and Kafka
* Fetch Data 
* Store Data 
* Clean Data 
* Data analysis
* Modeling 
* Tests

### I- Setup Zookeeper and Kafka

__Prerequisites :__
* JDK
* Install in local Kafka and zookeeper

__How to Start Zookeeper server__:

   * Move to Zookeeper directory
   * Run : ./zkServer.sh start ._PATH_TO_ZOOKEEPER_/conf/zookeeper.properties
   * __On windows :__ open a command-line, navigate to zookeeper bin directory, and run _zkServer.cmd_ or zkServer.sh on unix
   * If everything is ok you should see : __Server started__
   
How to start a Kafka server : 
   
   * Move to Kafka directory 
   * Run : ./kafka-server-start.sh ./_PATH_TO_KAFKA_/config/server.properties
   * kafka-server-start.bat  ./_PATH_TO_KAFKA_/config/server.properties 

How to start to get tweets  : 

   * Start Zookeeper server
   * Start kafka server
   * Start the script run.py in scripts/run.py
   * Open a new command-line. Navigate to scripts. And run "consummer.py" script

Limitations :

   * The limits are on number of keywords / user ids etc you can track - these are in the docs.
     
     The limit on tweets received, is 1% of the firehose, which is variable. If the volume of tweets is less than 1% of all tweets posted, you will get all tweets matching. Once you start missing tweets you will start receiving limit notices in the stream.
     
     Depending on what you’re tracking, you may not get any tweets for a while, instead, blank lines are sent to keep the connection alive. You should aim to keep a stable, open connection and not reconnect frequently - however, if no activity or an error occurs you should reconnect, but with exponential backoff (exponentially increasing the delay between reconnect attempts)

TroubleShooting : 

   * On start, if you modify the logs file, Kafka could be not able to read the new log directory. 
     Just delete everything who refer to log before create a clean base of log files. 
     Add the new log path to server.properties.
     
   * It could have some ephemeral connection to znode. In other words, the node already exist so it's engender a fatal error and the broker die. To clean everything and run on clean base you could use the following commands:
     __"docker compose rm -svf"__.
   * If the previous command does'nt work, try to add more time sleep on the kafka's containers creation. You could find it in ./Kafka/kafka_entr_point/start-kafka.sh
Topic creation : 

   * example : ./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic sample_test
   * Replica number == number of brokers 

Kafka_cheat_sheet : https://ronnieroller.com/kafka/cheat-sheet#listing-messages-from-a-topic

### II- Real-time prediction

Navigate to spark bin directory and run :

* spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.2 Streaming.py localhost:2181 Twitter

