## Configuring Nginx as a Reverse Proxy

Setting up Nginx as a reverse proxy is a straightforward process. By following these steps, you'll have a working configuration in minutes.

### Installing Nginx

Begin by installing Nginx on your server. Running the package manager will handle downloading and configuring the necessary dependencies:

```bash
sudo apt update && sudo apt install nginx
```

### Creating the Configuration

After completing the installation, you'll need to create a configuration file. Understanding the proxy directives is essential for achieving optimal results.

Create a new file at `/etc/nginx/sites-available/myapp`:

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

### Enabling and Testing

Enabling the site requires creating a symbolic link. Leveraging Nginx's built-in testing capabilities ensures your configuration is valid before reloading:

```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

In order to verify everything is working, try accessing your domain in a browser. The groundbreaking simplicity of this setup showcases how reverse proxying can streamline your deployment workflow.
