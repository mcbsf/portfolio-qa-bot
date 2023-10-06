# portfolio-qa-bot

nginx server:
                 
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

        # Handle other HTTP methods and CORS headers
        proxy_pass http://127.0.0.1:8000; # Assuming your FastAPI app runs on port 8000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 60;
        proxy_connect_timeout 60;
        proxy_redirect off;

        # CORS headers for non-OPTIONS requests
        add_header 'Access-Control-Allow-Origin' 'https://mariosoftware.solutions';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' '*';

        # Allow the use of websockets
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}


then
sudo certbot --nginx -d api4mariosoftware.xyz -d www.api4mariosoftware.xyz

then change certbot options to:




.
.
.

    # SSL certificate configuration managed by Certbot
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/api4mariosoftware.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api4mariosoftware.xyz/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = www.api4mariosoftware.xyz) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    if ($host = api4mariosoftware.xyz) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    # HTTP server configuration (redirect to HTTPS)
    server_name api4mariosoftware.xyz www.api4mariosoftware.xyz;
    listen 80;
    return 404; # managed by Certbot
}