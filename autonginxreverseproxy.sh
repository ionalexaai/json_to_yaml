#!/bin/bash

set -e

echo "=========================================="
echo "   NGINX + CERTBOT Full Automation Script  "
echo "=========================================="

# Function to install NGINX if missing
install_nginx() {
    if ! command -v nginx &> /dev/null; then
        echo "NGINX not found. Installing..."
        sudo apt update
        sudo apt install -y nginx
        sudo systemctl enable nginx
        sudo systemctl start nginx
        echo "NGINX installed successfully."
    else
        echo "NGINX is already installed."
    fi
}

# Function to install Certbot
install_certbot() {
    if ! command -v certbot &> /dev/null; then
        echo "Certbot not found. Installing..."
        sudo apt update
        sudo apt install -y certbot python3-certbot-nginx
        echo "Certbot installed successfully."
    else
        echo "Certbot is already installed."
    fi
}

# Function to configure domain for NGINX and Certbot
configure_domain() {
    read -rp "Enter the domain name to configure (e.g., example.com): " DOMAIN
    if [ -z "$DOMAIN" ]; then
        echo "Invalid domain. Exiting."
        exit 1
    fi

    NGINX_CONF="/etc/nginx/sites-available/$DOMAIN"
    NGINX_ENABLED="/etc/nginx/sites-enabled/$DOMAIN"

    if [ -f "$NGINX_CONF" ]; then
        echo "Nginx configuration for $DOMAIN already exists. Skipping."
    else
        echo "Creating NGINX configuration for $DOMAIN..."

        sudo bash -c "cat > $NGINX_CONF" <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    root /var/www/$DOMAIN/html;
    index index.html index.htm;

}
EOF

        echo "Creating web root directory..."
        sudo mkdir -p /var/www/$DOMAIN/html
        sudo chown -R "$USER:$USER" /var/www/$DOMAIN/html
        echo "<html><head><title>Welcome to $DOMAIN</title></head><body><h1>Success! $DOMAIN is working!</h1></body></html>" | sudo tee /var/www/$DOMAIN/html/index.html > /dev/null

        echo "Enabling NGINX site..."
        sudo ln -s "$NGINX_CONF" "$NGINX_ENABLED"

        echo "Testing NGINX configuration..."
        sudo nginx -t

        echo "Reloading NGINX..."
        sudo systemctl reload nginx
    fi

    echo "Obtaining SSL certificate for $DOMAIN via Certbot..."
    sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m "admin@$DOMAIN" --redirect

    echo "Certificate setup completed for $DOMAIN."

    read -rp "Do you want to add a reverse proxy to this domain? (y/n): " REVERSE_RESPONSE
    if [[ "$REVERSE_RESPONSE" =~ ^[Yy]$ ]]; then
        read -rp "Enter the reverse proxy URL (e.g., http://localhost:5000/): " PROXY_URL
        if [ -z "$PROXY_URL" ]; then
            echo "Invalid proxy URL. Skipping reverse proxy setup."
        else
            echo "Adding reverse proxy to NGINX configuration..."

            sudo sed -i "/listen 443 ssl; # managed by Certbot/a \\\n    # Reverse Proxy Configuration\n    location / {\n        proxy_pass $PROXY_URL;\n        proxy_set_header Host \$host;\n        proxy_set_header X-Real-IP \$remote_addr;\n        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;\n        proxy_set_header X-Forwarded-Proto \$scheme;\n    }\n" "$NGINX_CONF"

            echo "Testing NGINX configuration..."
            sudo nginx -t

            echo "Reloading NGINX..."
            sudo systemctl reload nginx

            echo "Reverse proxy added to $DOMAIN."
        fi
    fi
}

# Function to finalize and restart services
finalize() {
    echo "Restarting NGINX..."
    sudo systemctl restart nginx
    echo "All done! $DOMAIN is live with SSL."
}

# Main execution
install_nginx
install_certbot

read -rp "Do you want to add a domain to NGINX and Certbot? (y/n): " RESPONSE
if [[ "$RESPONSE" =~ ^[Yy]$ ]]; then
    configure_domain
    finalize
else
    echo "Exiting without domain configuration."
fi

echo "=========================================="
echo " Script completed. Have a good day!"
echo " You can perform edits in this directory /etc/nginx/sites-available"
echo "=========================================="
