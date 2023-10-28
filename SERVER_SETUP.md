## SETUP Instructions

### Installations
1. prepare for app:

    ```bash
    sudo apt install python3-dev
    sudo apt-get install build-essential -y
    ```
2. install nginx and certbot:
    ```bash
    sudo apt install nginx
    sudo apt install certbot python3-certbot-nginx 
    ```
install nginx, pip and certbot
Assuming you have an EC2 instance with Nginx and Certbot already installed, follow these commands to deploy your FastAPI application:

### Configuring and running the server
1. edit set nginx config file:
    ```bash
    cd /etc/nginx
    sudo nano nginx.conf 
    ```

    Inside the file, add the following Nginx server configuration:

    ```nginx
    user www-data;
    worker_processes auto;
    pid /run/nginx.pid;
    include /etc/nginx/modules-enabled/*.conf;

    events {
            worker_connections 768;
            # multi_accept on;
    }

    http {

            ##
            # Basic Settings
            ##

            sendfile on;
            tcp_nopush on;
            types_hash_max_size 2048;
            # server_tokens off;

            # server_names_hash_bucket_size 64;
            # server_name_in_redirect off;

            include /etc/nginx/mime.types;
            default_type application/octet-stream;

            ##
            # SSL Settings
            ##

            ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
            ssl_prefer_server_ciphers on;

            ##
            # Logging Settings
            ##

            access_log /var/log/nginx/access.log;
            error_log /var/log/nginx/error.log;

            ##
            # Gzip Settings
            ##

            gzip on;

            # gzip_vary on;
            # gzip_proxied any;
            # gzip_comp_level 6;
            # gzip_buffers 16 8k;
            # gzip_http_version 1.1;
            # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

            ##
            # Virtual Host Configs
            ##

            include /etc/nginx/conf.d/*.conf;
            include /etc/nginx/sites-enabled/*.*;
    }
    ```

2. Create or edit the Nginx server configuration file for your domain:

    ```bash
    cd /etc/nginx/sites-available/
    sudo nano api4mariosoftware.xyz
    ```

    Inside the file, add the following Nginx server configuration:

    ```nginx
    server {
        server_name api4mariosoftware.xyz www.api4mariosoftware.xyz;

        location / {
            if ($request_method = OPTIONS) {
                # Respond with 200 OK for OPTIONS requests
                add_header 'Access-Control-Allow-Origin' 'https://mariosoftware.solutions';
                add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
                add_header 'Access-Control-Allow-Headers' '*';
                add_header 'Content-Length' 0;
                return 200;
            }
            # CORS headers for non-OPTIONS requests
            add_header 'Access-Control-Allow-Origin' 'https://mariosoftware.solutions';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' '*';

            # Handle other HTTP methods and CORS headers
            proxy_pass http://127.0.0.1:8000; # Assuming your FastAPI app runs on port 8000
            proxy_set_header X-Real-IP $remote_addr;

            # Allow the use of websockets
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
    ```


3. Obtain an SSL certificate for your domain using Certbot:

    ```bash
    sudo certbot --nginx -d api4mariosoftware.xyz -d www.api4mariosoftware.xyz
    ```

4. After obtaining the SSL certificate, open the Nginx configuration file again and make the following changes outside location, inside servers:

    ```
    nginx
    ...
    location {
        ...
    }
    ...
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/api4mariosoftware.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api4mariosoftware.xyz/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    ```


5. Create a symbolic link to enable the Nginx site configuration:

    ```bash
    sudo ln -s /etc/nginx/sites-available/api4mariosoftware.xyz /etc/nginx/sites-enabled/ -f
    ```

6. Restart Nginx to apply the changes:

    ```bash
    sudo systemctl restart nginx
    ```
7. Navigate to your FastAPI application folder:

    ```bash
    cd /path/to/your/app
    ```

9. Run the FastAPI application using `uvicorn`, assuming you have `nohup` installed to run the command in the background:

    ```bash
    nohup uvicorn main:app --workers 8 > uvicorn.log 2>&1 &
    ```

Your FastAPI application should now be up and running, accessible via HTTPS at `https://api4mariosoftware.xyz` and `https://www.api4mariosoftware.xyz`.
                                          
Remember to replace `/path/to/your/app` with the actual path to your application folder and adjust the domain and SSL paths as necessary.
