FROM ubuntu:18.04

# Setting locales
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y locales \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8 
ENV LC_ALL en_US.UTF-8

# Install software-properties-common (needed to do apt-add-repository)
RUN apt-get update && apt-get install -y --no-install-recommends \
software-properties-common

# Add repository for swipl
RUN apt-add-repository ppa:swi-prolog/stable

# Install stuff
RUN apt-get update && apt-get install -y --no-install-recommends \
python3 \
python3-pip \
curl \
swi-prolog

# Make microservice directories
RUN mkdir -p /ms/reasoning /ms/reasoning/static /ms/reasoning/templates /ms/reasoning/uploads

# Copy flask stuff
COPY static/. /ms/reasoning/static/
COPY templates/. /ms/reasoning/templates/
COPY reasoning-task.py requirements.txt /ms/reasoning/

# Copy reasoning stuff
RUN mkdir -p /opt/cturtle-1.0.6 /opt/carl-1.0.3 /opt/eye
COPY reasoner/carl-1.0.3/. /opt/cturtle-1.0.6/
COPY reasoner/cturtle-1.0.6/. /opt/cturtle-1.0.6/
COPY reasoner/eye/. /opt/eye/

# Add path environment variables for cturtle and carl
ENV PATH "$PATH:/opt/cturtle-1.0.6"
ENV PATH "$PATH:/opt/carl-1.0.3"

# Set wd
WORKDIR /ms/reasoning

# Setup flask microservice
RUN pip3 install setuptools
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --upgrade lxml

# Run microservice
CMD [ "python3", "reasoning-task.py" ]