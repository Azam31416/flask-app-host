# Hosting Method for Flask App
Host a flask app on a linux server on a VM with nginx and https (self signed cert) support with NAT port forwarding.

## How to setup
1. Download Ubuntu server and install it on Oracle VM VirtualBox.

2. Go to network section of the Ubuntu VM's settings and select NAT.

3. Click the advanced settings and set settings for the port forwarding as-

  | Name | Protocol | Host IP | Host Port | Guest IP | Guest Port |
  | ---- | -------- | ------- | --------- | -------- | ---------- |
  | Rule 1 | TCP |  | 8080 |  | 22 |
  | Rule 2 | TCP |  | 8443 |  | 443 |

  Here we are mapping port 22 of ssh to 8080 of Host machine and port 443 to 8443 for the web server. Note that we are setting larger ports because Host ports lesser than 1024 are not available without root privilege (see [this](https://askubuntu.com/questions/95499/portforwarding-from-host-to-guest-using-port-80-but-it-doesnt-work)) which is not recommended.

4. Check whether the port for ssh is working by opening terminal and typing-

```console
user@ubuntu:~$ ssh user@localhost -p 8080
```

If you successfully log in then close the VM and then restart it in headless mode to open it without the screen. Headless mode can be started by first clicking the small arrow button just besides the start VM button.

5. Set proper permissons for the folders and files. (EXPAND)

6. Run the `/var/www/project_name/app.py` on the server and fix the issues/fulfill the dependencies. If it runs on Guest port 8080 that we set in step 3, check on host port 9090 whether it is working or not.

7. Request an SSL certificate (self signed) for any domain you like using-

```console
user@ubuntu:~$ (EXPAND)
```
8. Download nginx and make the following settings in (EXPAND) for setting up secure reverse proxy-
EXPAND

9. Go to `/etc/hosts` file and add an entry-

   `127.0.0.1  example-domain.com`

for localhost mapping it to the domain we got a self signed certificate for in step 7.

10. Check if the website is working in guest by using-

 ```console
user@ubuntu:~$ curl https://localhost --insecure
```

11. Open the browser and chck the domain name is working on ssl on port 8443 by typing-

`https://example-domain.com:8443`

in the browser search bar. There will be a warning. Skip it by clicking advanced settings and then make an exception for this site. This is because our certificate is self signed. Import the SSL certificate in the browser and set it as trusted (EXPAND). Open the website again and use it. It should work fine. Also click the lock before the URL and check it. The website should be using https with a valid but untrusted certificate (because it is self signed).
