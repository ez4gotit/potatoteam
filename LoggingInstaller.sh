/bash

# Install PostgreSQL if not already installed
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create a PostgreSQL database for storing Nginx logs
sudo -u postgres psql -c "CREATE DATABASE nginx_logs;"

# Create a table to store Nginx logs
sudo -u postgres psql -d nginx_logs -c "CREATE TABLE access_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    remote_addr VARCHAR(50) NOT NULL,
    request_method VARCHAR(10) NOT NULL,
    request_uri TEXT NOT NULL,
    status_code INT NOT NULL,
    bytes_sent INT NOT NULL
);"

# Grant necessary permissions to the database user
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE nginx_logs TO your_username;"

# Setting up log rotation for Nginx logs
sudo nano /etc/logrotate.d/nginx

# Add the following configuration to the file
/path/to/nginx/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 your_username your_groupname
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 cat /var/run/nginx.pid
    endscript
}

# Restart Nginx to apply log rotation changes
sudo systemctl restart nginx

echo "PostgreSQL database and log rotation for Nginx logs setup complete."

