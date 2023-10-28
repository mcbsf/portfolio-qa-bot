## SETUP Instructions

Assuming you have an EC2 instance with Nginx and Certbot already installed, follow these commands to deploy your FastAPI application:

1. Change directory to `/etc/nginx/sites-available/`:

    ```bash
    cd /etc/nginx/sites-available/
    ```

2. Create or edit the Nginx server configuration file for your domain:

    ```bash
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

4. After obtaining the SSL certificate, open the Nginx configuration file again and make the following changes:

    ```nginx
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/api4mariosoftware.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api4mariosoftware.xyz/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    ```

5. Save the Nginx configuration file and exit the text editor.

6. Create a symbolic link to enable the Nginx site configuration:

    ```bash
    sudo ln -s /etc/nginx/sites-available/api4mariosoftware /etc/nginx/sites-enabled/ -f
    ```

7. Restart Nginx to apply the changes:

    ```bash
    sudo systemctl restart nginx
    ```
8. Navigate to your FastAPI application folder:

    ```bash
    cd /path/to/your/app
    ```

9. Run the FastAPI application using `uvicorn`, assuming you have `nohup` installed to run the command in the background:

    ```bash
    nohup uvicorn main:app --workers 8 > uvicorn.log 2>&1 &
    ```

Your FastAPI application should now be up and running, accessible via HTTPS at `https://api4mariosoftware.xyz` and `https://www.api4mariosoftware.xyz`.

Remember to replace `/path/to/your/app` with the actual path to your application folder and adjust the domain and SSL paths as necessary.
