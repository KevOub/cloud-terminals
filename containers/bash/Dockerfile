FROM ubuntu:21.04

# install dependencies
ARG DEBIAN_FRONTEND=noninteractive
ARG OPTIONAL_PACKAGES
RUN apt-get update --yes && apt-get --yes install --no-install-recommends  build-essential cmake git libjson-c-dev libwebsockets-dev ca-certificates apt-transport-https sudo  rsync vim curl

RUN apt-get install --yes --no-install-recommends ${OPTIONAL_PACKAGES}

# make installation path
RUN mkdir /var/www/
WORKDIR /var/www
# install
RUN git clone https://github.com/tsl0922/ttyd.git .
RUN mkdir build && cd build && cmake .. && make && make install


# add dummy user (no sudo)
# RUN useradd -k /etc/skel -r -m -d /home/cyber -s /bin/bash -u 1000 cyber 

# remove if you do not want cyber in sudo groop
RUN useradd -k /etc/skel/ -r -m -d /home/cyber -s /bin/bash -u 1000 -g sudo cyber 
RUN echo 'cyber:cyber' | chpasswd
WORKDIR /home/cyber/

# add tldr (a better manpage)
# RUN curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
# RUN apt-get install -y nodejs
# RUN npm install -g tldr 


# Add levels as copy (not volume)
ADD ./challenges/ /root/
# RUN chmod +x /root/setup/cheat && cp /root/setup/cheat /usr/bin/
RUN chmod +x /root/setup/makelevels.sh && exec /root/setup/makelevels.sh    
RUN chmod +x /root/setup/healthy.sh
RUN chmod +x /root/setup/clean.sh 

# Now, get md5 hash of workdir and save it in root
RUN find /home/ -type f | grep -v cyber | xargs -i  sh -c 'cat {} && echo {}'  | md5sum | cut -d' ' -f1 > /root/home_checksum
# Create backup snapshot
# RUN mkdir /var/backups/home && rsync -a /home/ /var/backups/home/

# launch as dummy user
EXPOSE 8080
# LAUNCHES SHELL AS DUMMY
CMD ["ttyd","-p","8080","login"] 


