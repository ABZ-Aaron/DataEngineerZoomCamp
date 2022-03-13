# Stream Processing ~ Kafka

Let's say we have source systems and target systems that exchange data. 

This can get complicated. We have considered protocols (TCP, HTTP, etc), data format, schemas etc.

Apache Kafka is a high throughput distributed messaging system that allows us to decouple our data streams and systems. So our source systems have their data end up in Kafka. And target systems will take data straight from Kafka.

Kafka can scale horizontally and is high performance.

So, essentially consumers and producers of data are not aware of each other. They are just using Kafka as a middleman. 

### Messages in Kafka

Consist of Key, Value and Timestamp.

### Topic in Kafka

Producer pushes messages to topic. Consumer consumes message from a topic.

### Kafka Broker

Physical machine on which Kafka is running.

### Logs

Data segments present in your disk. Stores messages in an order fashion. Assigns sequence id to each message before storing in logs. 

---

So Producer want's to talk to topic (e.g. ABC). Kafka then assigns a physical location for this topic on our hard disk called a log (e.g. Logs for topic ABC). 

Producer then sends messages to Kafka. These messages are physically written to logs represented on hard disk. Once written, Kafka send acknowledgement back to Producer.

Kafka consumer wants to read from particular topic (e.g. ABC). Kafka goes to logs, reads all messages, and then pushes them to Kafka consumer.

Once consumer has received messages, it acknowledges that it has received messages and read them.

---

Let's say we have Consumer1. Consumer1 wan't to read from topic ABC. Kafka will go to the logs and read some messages, and pushes these messages to Consumer1. 

Consumer1 then acknowledges. Kafka will then go on to the next logs and repeat. It wll also writes somewhere else saying that Consumer1 has read from topic ABC 10 messages. Then next 10 messages are sent to consumer, and Kafka writes Consumer1 from topic ABC has read 20 messages, and so on.

We may have another consumer, Consumer2. Kafka would add a new entry (e.g. Consumer2 has read 10 message from ABC).

This gives Kafka control over different consumers, what's been read by consumers, and what needs to be read next.

### Partitioning 

In Kafka, data is not static. In BigQuery, we use partitioning to reduce cost and time. In Kafka, we use it for scalability purposes.

We can also have consumer groups. A topic is usually a wrapper around different partitions. 

Kafka considers a consumer group as one entity. So Consumer1 might be receiving message 10, while Consumer2 is receiving message 11. So basically we are horizontally scaling.

So we have our producer, and a topic with 4 partitions (1, 2, 3, 4). We also have a consumer group (ConsumerGroup1) with Consumer1. Once Consumer1 attaches to Kafka, it will be assigned to all partitions. 

Let's introduce new Consumer (Consumer2). Here, some partitions would get reassigned (e.g. 3 and 4). This means we are reading messages at twice the speed. The maximum scalability we can have is 4 consumers (each reading from a single partition).

If we introduced a 5th consumer, this would stay idle. This is because all partitions are already assigned. However, if C1 dies, then C5 takes over.

Messages from producer goes to different partitions. 

## Configuration Terms

* retention.ms = Amount of time logs will stay before they get deleted
* cleanup.policy = either delete the messages from topic or compact count
* partition = scalability count
* replication = number of times the partition will be replicated

### Config for Consumer

* offset = What has already been read by the consumer
* consumer.group.id = identifier for consumer group
* auto.offset.reset = when consumer connects for first time to a topic

### Config for Producer

* acks (acknowledgment) = `0` means do not wait for leader or replica broker to write the message to disk. `1` means wait for leader broker to write message to disk. `all` means wait for leader and all replica to write message to disk.

## Zookeeper

Used by Kafka to store metadata

## Running Kafka

To run Kafka, we'll just use Docker. Navigate to the `docker` folder and run `docker compose up`. Kafka UI can then be accessed via `localhost:9021`