# Modbus
## History
Communication protocol developed by Modicon systems in 1979
In simple terms, it is a method used for transmitting information over serial lines between electronic devices 

The device requesting the information is called the Modbus Master and the devices supplying information are Modbus Slaves. 

In a standard Modbus network, there is one Master and up to 247 Slaves, each with a unique Slave Address from 1 to 247

## open Modbus
Modbus is an open protocol
Meaning that it's free for manufacturers to build into their equipment without having to pay royalties

You could pay MODBUS Foundation to get you device certified, but it is not mandatory
Modbus is typically used to transmit signals from instrumentation and control devices back to a main controller or data gathering system

## Vulnerabilities
The MODBUS/TCP protocol implementation contains multiple vulnerabilities that could allow an attacker to perform reconnaissance activity or issue arbitrary commands.

1. Lack of Confidentiality: All MODBUS messages are transmitted in clear text across the transmission media.
1. Lack of Integrity: There are no integrity checks built into the MODBUS application protocol. As a result, it depends on lower layer protocols to preserve integrity
1. Lack of Authentication: There is no authentication at any level of the MODBUS protocol. One possible exception is some undocumented programming commands.
1. Simplistic Framing: MODBUS/TCP frames are sent over established TCP connections. While such connections are usually reliable, they have a significant drawback. TCP connection is more reliable than UDP but the guarantee is not complete.
1. Lack of Session Structure: Like many request/response protocols (i.e. SNMP, HTTP, etc.) MODBUS/TCP consists of short-lived transactions where the master initiates a request to the slave that results in a single action. When combined with the lack of authentication and poor TCP initial sequence number (ISN) generation in many embedded devices, it becomes possible for attackers to inject commands with no knowledge of the existing session.

These vulnerabilities allow an attacker to perform reconnaissance activity on the targeted network. The first vulnerability exists because a SCADA MODBUS slave device may return Illegal Function Exception responses for queries that contain an unsupported function code. An unauthenticated, remote attacker could exploit this vulnerability by sending crafted function codes to carry out reconnaissance on the targeted network.

An additional reconnaissance vulnerability is due to multiple Illegal Address Exception responses generated for queries that contain an illegal slave address. An unauthenticated, remote attacker could exploit this vulnerability by sending queries that contain invalid addresses to the targeted network and gathering information about network hosts from returned messages.

Another vulnerability is due to lack of sufficient security checks in the SCADA MODBUS/TCP protocol implementation. The protocol specification does not include an authentication mechanism for validating communication between MODBUS master and slave devices. This flaw could allow an unauthenticated, remote attacker to issue arbitrary commands to any slave device via a MODBUS master.

The SCADA MODBUS/TCP protocol contains another vulnerability that could allow an attacker to cause a denial of service (DoS) condition on a targeted system.

The vulnerability is due to an implementation error in the affected protocol when processing Read Discrete Inputs request and response messages.

An unauthenticated, remote attacker could exploit the vulnerability by sending request or response parameters that contain malicious values for the data field option to a system that contains a vulnerable MODBUS/TCP implementation. The processing of the messages could trigger a DoS condition on the vulnerable system.

Another attack on Modbus can be Modbus TCP packet that exceeds the maximum length.

Modbus TCP is a protocol commonly used in SCADA and DCS networks for process control. MODBUS limits the size of the PDU to 253 bytes to allow the packet to be sent on a serial line, RS-485 interface. Modbus TCP prepends a 7-byte MODBUS Application Protocol (MBAP) header to the PDU, and the MBAP_PDU is encapsulated in a TCP packet. This places an upper limit on legal packet size.

An attacker creates a specially crafted packet longer than 260 bytes and sends it to a MODBUS client and server. If the client or server were programmed incorrectly, this could lead to a successful buffer overflow or a denial-of-service attack.