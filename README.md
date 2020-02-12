# FIL-ROUGE
Data engineering

##__Procédé :__ 
* Recuperation des accreditations auprès de Twitter 
* Recupération des données 
* Stockage des données 
* Nettoyage des données 
* Analyse des  données
* Mise en place du modele 
* Test

### I- Pour recuperer les données, nous avons décidé de nous connecter à l'API Twitter via le bus de message Apache Kafka. 


* Mise en place du bus : aka Kafka

Nous avons besoin d'un gestionnaire de brokers. Et comme mentionné dans la documentation, nous nous sommes tournés 
vers Apache Zookeeper. Les commandes suivantes permettent ainsi de : 

Lancement d'un serveur Zookeeper : 
    
   *   ./zkServer.sh start /home/akoffi/Bureau/Tools_fil_rouge/apache-zookeeper-3.5.6-bin/conf/zookeeper.properties
   * Vous devriez voir la mention __Server started__
   
Lancement d'un serveur kafka : 
   
   * ./kafka-server-start.sh /home/akoffi/Bureau/Tools_fil_rouge/kafka_2.12-2.3.0/config/server.properties

Creation d'un Topic : 

   * ./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic sample_test
   * Le nombre de replica correspond à notre nombre de brokers. 

Instancier une fenetre pour le consumer : 
   * kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic Twitter --from-beginning

Pour lancer la recuperation de la data : 

   * Demarrer le serveur Zookeeper 
   * Demarrer un serveur kafka 
   * Lancer un consumer kafka pour visualiser les données ( optionel)
   * Lancer l'application java 

Limitations :

   * The limits are on number of keywords / user ids etc you can track - these are in the docs.
     
     The limit on tweets received, is 1% of the firehose, which is variable. If the volume of tweets is less than 1% of all tweets posted, you will get all tweets matching. Once you start missing tweets you will start receiving limit notices in the stream.
     
     Depending on what you’re tracking, you may not get any tweets for a while, instead, blank lines are sent to keep the connection alive. You should aim to keep a stable, open connection and not reconnect frequently - however, if no activity or an error occurs you should reconnect, but with exponential backoff (exponentially increasing the delay between reconnect attempts)

Kafka_cheat_sheet : https://ronnieroller.com/kafka/cheat-sheet#listing-messages-from-a-topic

### II- Couche persistance 

Une fois la data collectée, on l'écrit dans une base mongo pour faire un traitement par batch. 





