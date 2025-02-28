# Set your preferred Python 3 version here
ENV PYTHON_VERSION=3.10.16

# Updating, also setting as noninteractive for build purposes
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install wget \
    && apt-get -y install git

# Add MySQL repository through the special package
RUN wget -O /tmp/repo_package.deb "https://dev.mysql.com/get/mysql-apt-config_0.8.33-1_all.deb" && \
    dpkg -i /tmp/repo_package.deb && \
    rm -f /tmp/repo_package.deb

# With the repo added, install MySQL
RUN apt-get update \
    && apt-get install mysql-server -y

# Set a "home" folder for MySQL
RUN usermod -d /var/lib/mysql mysql

# Install python dependencies
RUN apt install -y \
    libffi-dev \
    libreadline-dev

# Download, compile, and install the specific python version
RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz && \
    tar xvf Python-$PYTHON_VERSION.tgz && \
    cd Python-$PYTHON_VERSION && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make install && \
    cd .. && rm -rf Python-$PYTHON_VERSION*

# Install pip
RUN python3 -m ensurepip --upgrade && \
    pip3 install --upgrade pip

# Install other tools
RUN pip3 install --no-cache-dir \
    virtualenv \
    setuptools \
    wheel

# Install MySQL connector
RUN pip3 install --no-cache-dir mysql-connector mysql-connector-python

# Copy initialization script
COPY init.sh /usr/local/bin/init.sh
RUN chmod +x /usr/local/bin/init.sh

# Set entrypoint to run the initialization script
ENTRYPOINT ["/usr/local/bin/init.sh"]

# Expose port
EXPOSE 3306

# Set up volume for MySQL data (not working at the moment)
# VOLUME /var/lib/mysql