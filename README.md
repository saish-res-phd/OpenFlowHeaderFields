# OpenFlowHeaderFields


The above code will do the following:-
1. Create a topology in mininet with two nodes h1 and h2 and switch s1 and pox openflow controller is used to control switches
2. A list of 25 latest version of openflow protocol(v1.5) will be send from node h1 to h2 via switch s1.
3. To include the actual information of the OpenFlow header fields in the dump flows output, we used_openflow_msgs function to include the values 
of each field in the match field of the struct.pack call. 
4. The  dump-flows command will display these flows along with the actual values of these header fields. The output of dump-flows will include 25 fields,
one for each header field that was sent, and the values of these fields will be displayed in the output.
5. To measure the performance,  iperf tool is used to measure the TCP and UDP bandwidth.
6. To run code we made use of 'mn' command sudo mn --custom openflow_messages.py --topo mytopo --controller remote

Note:- This will start a Mininet network with the topology defined in MyTopo class in the openflow_messages.py file, and the POX OpenFlow controller 
will be used to control the switches. The --controller remote option specifies that the controller will run outside of Mininet.
Once the network is started, the code will send the OpenFlow messages from h1 to h2 via s1, and print the flows in h2's switch s1. 
The performance metrics like time taken, TCP and UDP bandwidth, and latency can be measured using the iperf tool

Glossary:-

'match' is an OpenFlow match structure that specifies the matching criteria for the flow rule. The struct.pack() function is used to pack the match structure into a byte string, which can be sent as part of the OpenFlow message.

The !I4s4sH format string passed to struct.pack() specifies the format of the byte string. Each character in the format string represents a data type, and the order of the characters determines the order in which the values are packed.

In this case, the format string includes:

    !: specifies that the byte string should be in network byte order (big-endian).
    I: specifies that the first value should be packed as an unsigned 4-byte integer (32 bits).
    4s: specifies that the second value should be packed as a string of 4 bytes.
    4s: specifies that the third value should be packed as a string of 4 bytes.
    H: specifies that the fourth value should be packed as an unsigned 2-byte integer (16 bits).

The field_to_oxm dictionary is used to map the header fields to their corresponding OpenFlow Extensible Match (OXM) headers. 
The value parameter is the value to match on for the specified field.

The resulting byte string is used to populate the match field of the OpenFlow message, which specifies the matching criteria for the flow rule.

'instruction' is a binary representation of an OpenFlow instruction to forward the packet out a specific port.

In this specific case, the instruction b'\x00\x01\x00\x08\x00\x00\x00\x00' represents the action to forward the packet out the port with number 1. 
It is structured as follows:

    00 01: the instruction type code, where 00 01 means "output to switch port"
    00 08: the length of the instruction in bytes
    00 00 00 00: the port number, in this case set to 0 to indicate that the switch should determine the output port on its own based on its flow table rules. 
    However, in the original code, it should have been set to 1 to match the in_port value in the match.
    
'payload' is a binary data structure representing an OpenFlow message that contains a flow modification. This is constructed by packing several fields 
into a binary format using struct.pack.

Here's what each field represents:

    !BBHL - format string for packing the message header, which includes:
        ! - network byte order (big-endian)
        B - 1-byte unsigned integer (message version)
        B - 1-byte unsigned integer (message type)
        H - 2-byte unsigned integer (message length)
        L - 4-byte unsigned integer (transaction ID)

    H - 2-byte unsigned integer (flags)

    H - 2-byte unsigned integer (length of the match structure)

    4s - 4-byte string (padding)

    H - 2-byte unsigned integer (length of the instruction)

    4s - 4-byte string (padding)

    !I4s4sH - format string for packing the match structure, which includes:
        ! - network byte order (big-endian)
        I - 4-byte unsigned integer (OXM field)
        4s - 4-byte string (OXM value)
        4s - 4-byte string (mask)
        H - 2-byte unsigned integer (length)


The resulting binary data structure is sent over a TCP socket to the OpenFlow controller. The controller then uses this message to modify the flow table
of the switch.
