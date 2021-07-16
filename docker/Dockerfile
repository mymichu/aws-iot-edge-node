FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y \
    tftpd-hpa \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

VOLUME /tftpboot

EXPOSE 69

CMD /usr/sbin/in.tftpd --foreground --user nobody --address 0.0.0.0:69 --secure /tftpboot