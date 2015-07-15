#!/bin/bash
./script1.sh&
./script2.sh&
for server in server1 server2 server3 
do
    echo "Connecting to server $server"
done

