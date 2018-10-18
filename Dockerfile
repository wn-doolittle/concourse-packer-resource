FROM python:3.7.0-alpine3.8

RUN pip3 --no-cache-dir install --upgrade pip

ARG PACKER_VER=1.3.1

RUN wget -O /tmp/packer.zip \
    "https://releases.hashicorp.com/packer/${PACKER_VER}/packer_${PACKER_VER}_linux_amd64.zip" \
  && unzip -o /tmp/packer.zip -d /usr/local/bin \
  && rm -f /tmp/packer.zip

# COPY requirements.txt /app/requirements.txt

# RUN pip3 --no-cache-dir install -r /app/requirements.txt

# DEBUG -- copy test template file
# COPY test/data/template.json /opt/resource/

# copy scripts
COPY \
  bin/check \
  bin/in \
  bin/out \
  /opt/resource/

# copy library files
COPY \
  lib/__init__.py \
  lib/concourse.py \
  lib/log.py \
  lib/packer.py \
  /opt/resource/lib/
