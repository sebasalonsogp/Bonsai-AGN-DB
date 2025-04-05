FROM mariadb:10.11

# Environment variables for MariaDB
ENV MYSQL_DATABASE=agndb
ENV MYSQL_USER=agndb_user
ENV MYSQL_PASSWORD=agndb_password
ENV MYSQL_ROOT_PASSWORD=root_password

# Copy initialization scripts
COPY ./scripts/ /docker-entrypoint-initdb.d/

# Set the character set and collation
RUN echo "[mysqld]" > /etc/mysql/conf.d/charset.cnf \
    && echo "character-set-server = utf8mb4" >> /etc/mysql/conf.d/charset.cnf \
    && echo "collation-server = utf8mb4_unicode_ci" >> /etc/mysql/conf.d/charset.cnf

# Copy Python requirements
COPY requirements.txt /requirements.txt

# Install Python and dependencies
RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && pip3 install -r /requirements.txt \
    && mkdir -p /scripts

# Make Python script executable
RUN chmod +x /docker-entrypoint-initdb.d/03_generate_data.py

# Expose MariaDB port
EXPOSE 3306

# Start the database
CMD ["mysqld"] 