from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.link import TCLink

def start_network():
    # Create Mininet network
    net = Mininet(controller=Controller, switch=OVSSwitch, link=TCLink)
    
    
    # Add hosts, switch, controller and links to network
    controller = net.addController('c0')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    s1 = net.addSwitch('s1')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    
    # Start network and assign IP addresses to hosts
    net.start()
    s1.start([controller])
    
    h1.cmd('ifconfig h1-eth0 10.0.0.1 netmask 255.255.255.0')
    h2.cmd('ifconfig h2-eth0 10.0.0.2 netmask 255.255.255.0')
    
    # Define flow rules for all available header fields in OVS 2.9.8 and OpenFlow 1.5
   fields = {
          'in_port': 1,
          'in_phy_port': 1,
          'metadata': 0x1234567890abcdef,
          'eth_dst': '00:00:00:00:00:02',
          'eth_src': '00:00:00:00:00:01',
          'eth_type': 2048,
          'vlan_vid': 4096,
          'vlan_pcp': 3,
          'ip_dscp': 10,
          'ip_ecn': 3,
          'ip_proto': 6,
          'ipv4_src': '10.0.0.1',
          'ipv4_dst': '10.0.0.2',
          'tcp_src': 1234,
          'tcp_dst': 80,
          'udp_src': 1234,
          'udp_dst': 80,
          'sctp_src': 1234,
          'sctp_dst': 80,
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
          'ipv6_nd_tll': '00:00:00:00:00:00',
          'mpls_label': 0x1234,
          'mpls_tc': 3,
          'mpls_bos': 1,
          'pbb_isid': 0x123456,
          'tunnel_id': 0x12345678,
          'ipv6_exthdr': 0x123456,
          'pbb_uca': 1,
          'tcp_flags': 0x3f,
          'ip_frag': 0x01,
          'icmpv6_nd_tll': '00:00:00:00:00:00',
          'mpls_ttl': 64,
          'mpls_bos': 0
   }
   for key, value in fields.items():
        if isinstance(value, str):
            value_str = '"{}"'.format(value)
        elif isinstance(value, int) and value > 0xFFFF:
            value_str = "0x{:X}".format(value)
        else:
            value_str = str(value)
        net.controllers[0].cmd("ovs-ofctl add-flow s1 in_port={0},dl_vlan_pcp={1},actions=output:2".format(fields['in_port'], fields['vlan_pcp']))



    # Dump OpenFlow flows and display 25 header fields
    flows = net.controllers[0].cmd('ovs-ofctl dump-flows s1')
    print(flows)
    
    # Stop network
    net.stop()

if __name__ == '__main__':
    start_network()

