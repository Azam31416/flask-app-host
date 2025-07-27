# Hosting Method for Flask App
Host a flask app on a linux server on a VM with nginx and https (self signed cert) support with NAT port forwarding.

## How to setup
1. Download Ubuntu server and install it on Oracle VM VirtualBox.

2. Go to network section of the Ubuntu VM's settings and select NAT.

3. Click the advanced settings and set settings for the port forwarding as-

  | Name | Protocol | Host IP | Host Port | Guest IP | Guest Port |
  | ---- | -------- | ------- | --------- | -------- | ---------- |
  | ssh | TCP |  | 8080 |  | 22 |
  | https | TCP |  | 8443 |  | 443 |
  | http | TCP |  | 9090 |  | 8000 |

  Here we are mapping port 22 of ssh to 8080 of Host machine and port 443 to 8443 for the web server. Note that we are setting larger ports because Host ports lesser than 1024 are not available without root privilege (see [this](https://askubuntu.com/questions/95499/portforwarding-from-host-to-guest-using-port-80-but-it-doesnt-work)) which is not recommended.

4. Check whether the port for ssh is working by opening terminal and typing-

```console
user@ubuntu:~$ ssh user@localhost -p 8080
```

If you successfully log in then close the VM and then restart it in headless mode to open it without the screen. Headless mode can be started by first clicking the small arrow button just besides the start VM button.

5. Set proper permissons for the folders and files. For this make the files owned by the user and belonging to the group www-data which is generally used to run web servers as. Do not give write access to the www-data group in main folder but only give write permissions in the static folder where images will be created. Check [this](https://www.internalpointers.com/post/right-folder-permission-website) resource for setting this properly.

6. Run the `/var/www/project_name/app.py` on the server and fix the issues/fulfill the dependencies. Check if it runs as www-data user by running-

```console
user@ubuntu:/var/www/project_name$ sudo -u www-data python3 app.py
```

This should run the app on guest port 8000. Check on host port 9090 whether http is working or not as we set this port for http in step 3. 

7. Request an SSL certificate (self signed) for any domain you like using-

```console
user@ubuntu:~$ openssl req -x509 -nodes -days 365 -subj "/C=CA/ST=QC/O=Company, Inc./CN=example-domain.com" -addext "subjectAltName=DNS:example-domain.com" -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt;
```
Replace the values of `/C` `/ST` `/O` `/CN` with Country, State, Organization and Common Name. In place of `example-domain.com`, use any domain that you like. 

8. Go to `/etc/hosts` file and add an entry-

   `127.0.0.1  example-domain.com`

for localhost mapping it to the domain we got a self signed certificate for in step 7. Refer [this](https://codingwithmanny.medium.com/configure-self-signed-ssl-for-nginx-docker-from-a-scratch-7c2bcd5478c6) in case of an issue in doing step 7 and step 8.

9. Download nginx and make the following settings for setting up secure reverse proxy-
 Unlink the default configuration by-
 
 ```console
 user@ubuntu:~$ unlink /etc/nginx/sites-enabled/default
```
  In the sites-available folder, make a `reverse-proxy.conf` file

 ```console
 user@ubuntu:/etc/nginx/sites-available$ nano reverse-proxy.conf
```

and put this setting in it-

```
server {
      listen 443 ssl http2 default_server;
      listen [::]:443 ssl http2 default_server;
      ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
      ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
      access_log /var/log/nginx/reverse-access.log;
      error_log /var/log/nginx/reverse-error.log;
      
      location / {
        proxy_pass http://127.0.0.1:8000;
      }
      
      location /static/ {
        alias /var/www/project_name/static/;
      }
}
```

Link this setting to the sites-enabled directory by running-
 ```console
 user@ubuntu:~$ ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf
```
check the configuration by the `nginx -t` command and run `sudo systemctl restart nginx` if needed. See [this](https://www.linode.com/docs/guides/how-to-configure-nginx/) for more info.

11. Check if the website is working in guest by using-

 ```console
user@ubuntu:~$ curl https://localhost --insecure
```

11. Open the browser and check the domain name is working on ssl on port 8443 by typing-

`https://example-domain.com:8443`

in the browser search bar. There will be a warning. Skip it by clicking advanced settings and then make an exception for this site. This is because our certificate is self signed. Import the SSL certificate (located at `/etc/ssl/certs/nginx-selfsigned.crt` as done in step 7) in the browser settings to set it as trusted. Open the website again and use it. It should work fine. Also click the lock before the URL and check it. The website should be using https with a valid but untrusted certificate (because it is self signed).

12. You can configure cron tabs for taking backup of important files such as /var/www using the other project that I posted on this [link](https://github.com/Azam31416/backup-cron)
