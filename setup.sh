# Setup the local mount of the CLEAR_Vesper
sshfs cern_cleardaq:/home/pietro/work/ /home/pietro/cleardaq/
# Setup the port forwarding for the socket
#screen -S portForward -d -m ssh -R 65432:localhost:65432 -R 50007:localhost:50007 cern_cleardaq
