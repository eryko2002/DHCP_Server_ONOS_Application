# How to download:
## Download Mininet
It can be downloaded from 
## Download Docker
```
sudo apt install docker.io -y
```
## Download ONOS image for Docker
```
docker pull onosproject/onos
```

# How to run:
## Run containerized ONOS application in Docker:
```
docker run -itd --rm -p 8181:8181 -p 8101:8101 --name onos-application onosproject/onos
```
To open ONON web service type : http://localhost:8181/onos/ui - username: onos, password: rocks

## Log into Karaf - username: karaf, password: karaf
```
 ssh -p 8101 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null karaf@localhost
```
### In Karaf environment run below commands:
```
app activate org.onosproject.openflow
app activate org.onosproject.cli
app activate org.onosproject.fwd
```
#### To check up and running karaf apps:
```
apps -a -s
```
## Run Mininet application:
```
sudo python dhcp6.py
```
