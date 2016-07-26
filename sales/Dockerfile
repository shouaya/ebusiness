FROM python:2.7-alpine

COPY enterpoint.sh /root/enterpoint.sh

RUN apk add --update git py-mysqldb mysql-dev gcc musl-dev && \
    pip --no-cache-dir install django && \
    pip --no-cache-dir install xlsxwriter && \
    pip --no-cache-dir install MySQL-python && \
    pip --no-cache-dir install xlrd && \
    chmod +x /root/enterpoint.sh && \
    apk del gcc musl-dev mysql-dev && \
    rm -rf /var/cache/apk/*


EXPOSE 80

ENTRYPOINT ["/root/enterpoint.sh"]
