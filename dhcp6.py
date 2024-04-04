from mininet.net import Mininet
from mininet.cli import CLI
import time
from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.node import Node
import os

def start_dhcp_server(first_IP, last_IP):
    dhcp_server = Node('dhcp', inNamespace=False)
    dhcp_server.cmd(f'/usr/sbin/dnsmasq --interface=dhcp-eth0 --dhcp-range=192.168.1.{first_IP},192.168.1.{last_IP},255.255.255.0 --no-daemon &')

def generate_ip_pool(first_IP, last_IP):
    pool = [f'192.168.1.{i}' for i in range(first_IP, last_IP+1)]
    return pool

def assign_ip_addresses(net, ip_pool):
    for i, host in enumerate(net.hosts):
        intf = host.defaultIntf()
        host_ip = ip_pool[i]
        intf.cmd(f'ifconfig {intf.name} {host_ip} netmask 255.255.255.0')
        intf.updateIP()

def getHostsInformations(net):
    for host in net.hosts:
        intf = host.defaultIntf()
        print("IP address of host {}: {}".format(host.name, intf.IP()))

def startControllerOnSwitches(controller, switches):
    for i, switch in enumerate(switches):
        switch.start([controller])
        switch.cmd('ovs-vsctl set bridge s{} protocols=OpenFlow14'.format(i+1))

def clear_mininet_environment():
    os.system('sudo mn -c')

def topology():
    clear_mininet_environment()
    net = Mininet(controller=Controller, switch=OVSSwitch, link=TCLink)

    onos = net.addController(name='c0',
                             controller=RemoteController,
                             ip='172.17.0.2',
                             protocol='tcp',
                             port=6633,
                             executable='/opt/onos/bin/onos')

    s1, s2, s3,s4 = [net.addSwitch(i) for i in ('s1', 's2', 's3','s4')]

    lan1 = []

    for i in range(0, 20):
        h1 = net.addHost(f'h{i+1}', intfName='eth0', cls=Node)
        lan1.append(h1)

    for j in range(0, len(lan1)):
        switch_index = j // 5  # Użyj dzielenia całkowitego, aby uzyskać indeks switcha
        net.addLink(lan1[j], net.switches[switch_index])
        
    
    net.addLink(s1,s2)
    net.addLink(s1,s3)
    net.addLink(s2,s3)
    net.addLink(s1,s4)
    net.addLink(s2,s4)
    net.addLink(s3,s4)

    #first_IP = int(input("Podaj adres pierwszego hosta: 192.168.1."))
    #last_IP = int(input("Podaj adres ostatniego hosta: 192.168.1."))
    first_IP = 130
    last_IP = 160
    net.build()
    onos.start()
    time.sleep(2)
    startControllerOnSwitches(onos, net.switches)
    print("\nDefault IP addresses of hosts:")
    getHostsInformations(net)
    time.sleep(2)

    start_dhcp_server(first_IP, last_IP)
    ip_pool = generate_ip_pool(first_IP, last_IP)
    assign_ip_addresses(net, ip_pool)
    time.sleep(1)
    print("\nIP addresses of hosts after DHCP assignment")
    getHostsInformations(net)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

