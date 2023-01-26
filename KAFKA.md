```
kubectl run oh-kafka-my-kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.3.1-debian-11-r25 --namespace default --command -- sleep infinity
    
kubectl exec --tty -i oh-kafka-my-kafka-client --namespace default -- bash

kafka-console-producer.sh \
            --broker-list oh-kafka-my-kafka-0.oh-kafka-my-kafka-headless.default.svc.cluster.local:9092 \
            --topic locations

kubectl run oh-kafka-my-kafka-client-2 --restart='Never' --image docker.io/bitnami/kafka:3.3.1-debian-11-r25 --namespace default --command -- sleep infinity

kubectl exec --tty -i oh-kafka-my-kafka-client-2 --namespace default -- bash

kafka-console-consumer.sh \
            --bootstrap-server oh-kafka-my-kafka.default.svc.cluster.local:9092 \
            --topic locations \
            --from-beginning
```