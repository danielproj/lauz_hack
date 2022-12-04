#!/bin/bash

docker exec -it elastic_search /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic 
docker cp elastic_search:/usr/share/elasticsearch/config/certs/http_ca.crt . 
curl --cacert http_ca.crt -u elastic https://localhost:9200