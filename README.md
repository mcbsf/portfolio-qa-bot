# portfolio-qa-bot

nginx server:
                 
server {
    server_name api4mariosoftware.xyz www.api4mariosoftware.xyz;

    location / {
        proxy_pass http://127.0.0.1:8000; # Assuming your FastAPI app runs on port 8000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout     60;
        proxy_connect_timeout  60;
        proxy_redirect         off;

                # Allow the use of websockets
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

then
sudo certbot --nginx -d api4mariosoftware.xyz -d www.api4mariosoftware.xyz