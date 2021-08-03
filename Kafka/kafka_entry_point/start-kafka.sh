#!/bin/bash -e

sleep 30
exec "/kafka/bin/kafka-server-start.sh" "/kafka/config/server.properties"