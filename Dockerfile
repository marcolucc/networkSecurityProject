FROM ubuntu:latest
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install dsniff python3 python3-pip net-tools nano tcpdump
# tcpdump -i eth0 -w nome.pcap
RUN pip install pymodbus scapy 
#RUN echo 0 > /proc/sys/net/ipv4/ip_forward
# Disable SSL verification for dnf equivalent in Ubuntu (apt-get)
RUN echo "Acquire::https::Verify-Peer \"false\";" > /etc/apt/apt.conf.d/99verify-ssl
COPY . /app
WORKDIR /app
EXPOSE 502
CMD ["tail", "-f", "/dev/null"]
