## Configuring Nginx as a reverse proxy

This gets Nginx forwarding requests to a backend app. The whole thing takes about five minutes.

### Install Nginx

```bash
sudo apt update && sudo apt install nginx
```

### Create the configuration

Add a new file at `/etc/nginx/sites-available/myapp`:

```nginx
server {
    listen 80;
    server_name myapp.example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }
}
```

The `proxy_pass` directive tells Nginx where to forward requests. `proxy_set_header Host` passes the original hostname through so your backend knows which domain was requested.

### Enable and test

Link the config into `sites-enabled`, then test before reloading:

```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

`nginx -t` checks for syntax errors without touching the running server. If it reports OK, the reload is safe. Hit your domain in a browser to confirm requests are reaching the backend.
