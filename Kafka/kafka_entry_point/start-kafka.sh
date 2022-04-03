#!/bin/bash

rm -rf "/tmp/kafka-logs"
sleep 30
exec "/kafka/bin/kafka-server-start.sh" "/kafka/config/server.properties"