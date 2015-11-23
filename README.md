# UDPPinger
===========
This is a UDP Ping Utility for CSc 6220 (Networks) at Georgia State University.

Requirements
============
0. Python 2.7.x 

Setup and testing
=================
0. Clone this repository (```git clone https://github.com/nwautomator/UDPPinger.git```)
1. Start the "server"  (```python udpping_server.py```)
2. Use the client to ping the server (```python udpping.py 127.0.0.1```)
3. Rinse/repeat step 2.

Notes
=====
- The server can induce random packet loss if you pass the -R argument
- The client has many options. Run ```python udpping.py -h`` for details
- The latest version of this repository is always here: `https://github.com/nwautomator/UDPPinger`
