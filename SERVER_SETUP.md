{{

## Server Setup – Nginx + HTTPS (Let’s Encrypt) + Route 53

> **Scope:** This doc assumes:
>
> * App build, clone, Docker, etc. are handled by CI/CD.
> * Your app is exposed on the EC2 instance at **[http://127.0.0.1:8000](http://127.0.0.1:8000)** (via Docker or directly with Uvicorn).
> * You just need to configure **Nginx**, **Certbot**, and **DNS (Route 53)** for `api4mariosoftware.xyz`.

---

## 0. One-time checks (run on EC2)

Run these once to understand your environment (for debugging / future reference):

```bash
# Check OS (Ubuntu etc.)
lsb_release -a || cat /etc/os-release

# Check Nginx status
sudo systemctl status nginx

# See what’s listening on ports 80 and 8000
sudo ss -ltnp | egrep ':80|:8000' || true
```

You want this final state after setup:

* `nginx` listening on **80** and **443**
* Your app (or Docker proxy) listening on **127.0.0.1:8000**

---

## 1. Route 53 – DNS configuration

In Route 53, for the hosted zone `api4mariosoftware.xyz`:

1. **A record for root domain**

   * **Name:** `api4mariosoftware.xyz`
   * **Type:** `A`
   * **Value:** EC2 public IP (e.g. `34.228.56.179`)
   * **TTL:** `300` (or similar)

2. **CNAME for `www`**

   * **Name:** `www.api4mariosoftware.xyz`
   * **Type:** `CNAME`
   * **Value:** `api4mariosoftware.xyz`
   * **TTL:** `300`

Wait a few minutes so DNS propagates, then test locally:

```bash
nslookup api4mariosoftware.xyz
nslookup www.api4mariosoftware.xyz
```

Both should resolve to the EC2 public IP.

---

## 2. Install Nginx & Certbot on EC2

On the EC2 instance (Ubuntu):

```bash
sudo apt update

# Install Nginx
sudo apt install -y nginx

# Install Certbot + Nginx plugin
sudo apt install -y certbot python3-certbot-nginx

# Enable and start Nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

Also make sure the EC2 **Security Group** allows inbound:

* **HTTP (TCP 80, 0.0.0.0/0)**
* **HTTPS (TCP 443, 0.0.0.0/0)**

---

## 3. Create Nginx site for `api4mariosoftware.xyz`

Create a site config:

```bash
sudo nano /etc/nginx/sites-available/api4mariosoftware.xyz
```

Paste this:

```nginx
# HTTP server – used for ACME challenge and redirects
server {
    listen 80;
    server_name api4mariosoftware.xyz www.api4mariosoftware.xyz;

    # Let’s Encrypt validation path
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # For everything else, redirect to HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS server – reverse proxy to app on 127.0.0.1:8000
server {
    listen 443 ssl;
    server_name api4mariosoftware.xyz www.api4mariosoftware.xyz;

    # Certbot will manage these lines after first run, but keep placeholders:
    ssl_certificate /etc/letsencrypt/live/api4mariosoftware.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api4mariosoftware.xyz/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # CORS + proxy to backend
    location / {
        # Preflight
        if ($request_method = OPTIONS) {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' '*';
            add_header 'Content-Length' 0;
            return 200;
        }

        # CORS for actual requests
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' '*';

        # Reverse proxy to app on 127.0.0.1:8000
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto https;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable the site and test Nginx:

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/api4mariosoftware.xyz /etc/nginx/sites-enabled/ -f

# Optional: disable default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test config and reload
sudo nginx -t
sudo systemctl reload nginx
```

Now `curl http://api4mariosoftware.xyz` should return a `301` redirect (will fail for HTTPS until we get a cert).

---

## 4. Obtain and configure HTTPS certificate (Let’s Encrypt)

With Nginx serving on port 80 and DNS pointing correctly:

```bash
sudo certbot --nginx -d api4mariosoftware.xyz -d www.api4mariosoftware.xyz
```

When prompted:

* **Choose** option **2: Redirect** to force HTTP → HTTPS.

Certbot will:

* Validate the domain via HTTP-01 on port 80.
* Install certificates under `/etc/letsencrypt/live/api4mariosoftware.xyz/`.
* Update the HTTPS server block with correct `ssl_certificate` and `ssl_certificate_key` lines.
* Create/adjust an HTTP server block for redirection if needed.

Verify:

```bash
sudo nginx -t
sudo systemctl reload nginx
sudo certbot certificates
```

You should see:

* A certificate for `api4mariosoftware.xyz` and `www.api4mariosoftware.xyz`
* An expiry date ~90 days in the future

Also check that Certbot auto-renew is active:

```bash
sudo systemctl status certbot.timer
```

---

## 5. Final checks

From your local machine:

```bash
# Check HTTP → HTTPS redirect
curl -I http://api4mariosoftware.xyz

# Check HTTPS directly
curl -I https://api4mariosoftware.xyz

# Optionally, hit an API route
curl -X POST https://api4mariosoftware.xyz/get_answer \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'
```

In the browser:

* Visit `https://api4mariosoftware.xyz`
* Inspect the certificate:

  * Issued by Let’s Encrypt
  * Valid (not expired)
  * Correct domain name

At this point:

* EC2 + Nginx + Certbot + Route 53 are fully configured.
* Your CI/CD only needs to ensure the app is running on `127.0.0.1:8000` (e.g., Docker container with `-p 8000:8000`), and Nginx will handle HTTPS and routing.

}}
