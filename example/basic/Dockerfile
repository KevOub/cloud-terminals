FROM ubuntu:21.04
RUN apt-get update && apt-get install -y autoconf automake curl cmake git libtool make \
    && git clone --depth=1 https://github.com/tsl0922/ttyd.git /ttyd \
    && cd /ttyd && env BUILD_TARGET=x86_64 ./scripts/cross-build.sh

FROM ubuntu:21.04
COPY --from=0 /ttyd/build/ttyd /usr/bin/ttyd
ARG MYPORT=8080

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]
EXPOSE ${MYPORT}

CMD ["ttyd","bash"]
