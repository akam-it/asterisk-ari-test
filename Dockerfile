FROM centos:7

#EXPOSE 5060/udp
#EXPOSE 25000-30000/udp
COPY files/ /
RUN rpm --import https://ast.tucny.com/repo/RPM-GPG-KEY-dtucny \
    && rpm --import http://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-7 \
    && yum update -y \
    && yum install -y epel-release \
    && yum install -y asterisk asterisk-sip asterisk-sounds-core-ru asterisk-sounds-core-ru-alaw \
    && yum install -y python36 python36-pip python-pip \
    && pip install ari \
    && rm -rf /var/cache/yum/*

#ENTRYPOINT ["/usr/sbin/asterisk","-vvvvvvvvvv"]
#CMD python /etc/asterisk/scripts/test-task.py
CMD /usr/sbin/asterisk -vvvvvvvv && sleep 3 && python /etc/asterisk/scripts/test-task.py
