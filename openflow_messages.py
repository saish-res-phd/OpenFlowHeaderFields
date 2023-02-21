from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch, Host
from mininet.cli import CLI
from time import time
import socket
import struct

class MyTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1', cls=OVSSwitch)
        h1 = self.addHost('h1', cls=Host, ip='10.0.0.1')
        h2 = self.addHost('h2', cls=Host, ip='10.0.0.2')
        self.addLink(h1, s1)
        self.addLink(s1, h2)

def send_openflow_msgs():
    # Open a TCP connection to the controller
    controller_ip = '127.0.0.1'
    controller_port = 6633
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((controller_ip, controller_port))

    # Build the OpenFlow messages
    header_fields = {
        'in_port': 1,
        'eth_src': '00:00:00:00:00:01',
        'eth_dst': '00:00:00:00:00:02',
        'eth_type': 2048,
        'ipv4_src': '10.0.0.1',
        'ipv4_dst': '10.0.0.2',
        'ip_proto': 6,
        'tcp_src': 1234,
        'tcp_dst': 80,
        'udp_src': 1234,
        'udp_dst': 80,
        'icmpv4_type': 8,
        'icmpv4_code': 0,
        'arp_op': 1,
        'arp_spa': '10.0.0.1',
        'arp_tpa': '10.0.0.2',
        'arp_sha': '00:00:00:00:00:01',
        'arp_tha': '00:00:00:00:00:00',
        'ipv6_src': '2001:db8::1',
        'ipv6_dst': '2001:db8::2',
        'ipv6_flabel': 1234,
        'icmpv6_type': 128,
        'icmpv6_code': 0,
        'ipv6_nd_target': '2001:db8::1',
        'ipv6_nd_sll': '00:00:00:00:00:01',
        'ipv6_nd_tll': '00:00:00:00:00:00'
    }
    ofp_version = 1
    xid = 1
    for field, value in header_fields.items():
        msg_type = 10  # OFPT_FLOW_MOD
        msg_len = 72
        if isinstance(value, str):
            value = value.encode('utf-8')
        match = struct.pack('!I4s4sH', field_to_oxm[field], value, b'\x00\x00\x00', 0)
        instructions_len = 16
        instruction = b'\x00\x01\x00\x08\x00\x00\x00\x00'  # Output to port 1
        payload = struct.pack('!BBHLHH4sH4s', ofp_version, msg_type, msg_len, xid, 0, instructions_len, match, 0, instruction)
        sock.sendall(payload)
        xid += 1

    sock.close()
    

if __name__ == '__main__':
    # Start the Mininet network
    topo = MyTopo()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()

    # Wait for the switches to connect to the controller
    time.sleep(5)

    # Send the OpenFlow messages from h1 to h2 via s1
    h1 = net.get('h1')
    h2 = net.get('h2')
    h1.cmd('ping -c 1', h2.IP())  # Trigger ARP to learn MAC addresses
    send_openflow_msgs()

    # Print the flows in h2's switch s1
    s1 = net.get('s1')
    flows = s1.dpctl('dump-flows')
    print(flows)

    # Stop the Mininet network
    net.stop()
