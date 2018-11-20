ARG APP_IMAGE=snapkitchen/concourse-packer-resource:latest
FROM $APP_IMAGE

ENV PYTHONPATH=$PYTHONPATH:/opt/resource

# optionally install ptvsd
ARG PTVSD_INSTALL
RUN if [ -n "${PTVSD_INSTALL}" ]; then pip3 --no-cache-dir install ptvsd==4.1.4; fi
EXPOSE 5678/tcp

# TESTS -- copy test data
COPY test /opt/resource/test
