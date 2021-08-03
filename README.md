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

### I- Containers

To make everything easier, i setup one zookeeper head and 2 brokers throught docker.
Please note that you could add as much brokers as you want by simply modifying docker-compose and also add kafka properties files accordingly.

As a requirement, you should have docker installed.

Command to build and run the containers : 

* __docker compose build__
* __docker compose up__

Please note that you could have these following Troubleshooting : 

   * On start, if you modify the logs file, Kafka could be not able to read the new log directory. 
     Just delete everything who refer to log before create a clean base of log files. 
     Add the new log path to server.properties.
     
   * It could have some ephemeral connection to znode. In other words, the node already exist so it's engender a fatal error and the broker die. To clean everything and run on clean base you could use the following commands:
     __"docker compose rm -svf"__.
   * If the previous command does'nt work, try to add more time sleep on the kafka's containers creation. You could find it in ./Kafka/kafka_entr_point/start-kafka.sh

Well that's all you need.

How to start to get tweets  : 

   * Start the script run.py in scripts/run.py
   * Open a new command-line. Navigate to scripts. And run "consummer.py" script

Limitations :

   * The limits are on number of keywords / user ids etc you can track - these are in the docs.
     
     The limit on tweets received, is 1% of the firehose, which is variable. If the volume of tweets is less than 1% of all tweets posted, you will get all tweets matching. Once you start missing tweets you will start receiving limit notices in the stream.
     
     Depending on what you’re tracking, you may not get any tweets for a while, instead, blank lines are sent to keep the connection alive. You should aim to keep a stable, open connection and not reconnect frequently - however, if no activity or an error occurs you should reconnect, but with exponential backoff (exponentially increasing the delay between reconnect attempts)


Kafka_cheat_sheet : https://ronnieroller.com/kafka/cheat-sheet#listing-messages-from-a-topic

Explanation on communication of brokers IN container : [link](https://stackoverflow.com/questions/51630260/connect-to-kafka-running-in-docker)
### II- Real-time prediction

Navigate to spark bin directory and run :

* spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.2 Streaming.py localhost:2181 Twitter

### III- Tableau visualization 

Well you just have to connect tableau to messages.xlsx. This file will be present in scripts/ressources/