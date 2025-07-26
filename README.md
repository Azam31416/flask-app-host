# Hosting Method for Flask App
Host a flask app on a linux server on a VM with nginx and https (self signed cert) support with NAT port forwarding.

## How to setup
1. Download Ubuntu server and install it on Oracle VM VirtualBox.
2. Go to network section of the Ubuntu VM's settings and select NAT.
3. Click the advanced settings and set settings for the port forwarding as-

  | Name | Protocol | Host IP | Host Port | Guest IP | Guest Port |
  | ---- | -------- | ------- | --------- | -------- | ---------- |
  | Rule 1 | TCP |  | 8080 |  | 22 |
  | Rule 2 | TCP |  | 9090 |  | 8080 |

  Here we are mapping port 22 of ssh to 8080 of Host machine and port 8080 (on which we will run the webapp) to 9090 for the web server. Note that we are setting larger ports because Host ports lesser than 1024 are not available without root privilege (see [this](https://askubuntu.com/questions/95499/portforwarding-from-host-to-guest-using-port-80-but-it-doesnt-work)) which is not recommended.

4. Check whether the port for ssh is working by opening terminal and typing-

```console
user@ubuntu:~$ ssh user@localhost -p 8080
```

If you successfully log in then close the VM and then restart it in headless mode to open it without the screen. Headless mode can be started by first clicking the small arrow button just besides the start VM button 
