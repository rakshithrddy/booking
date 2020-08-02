FROM python:3.6-alpine

RUN apk add make automake gcc g++ subversion
RUN apk add libc-dev
RUN apk update
RUN apk add python3-dev
RUN apk add py-pip
RUN pip install -U pip

WORKDIR /home/bookingblog

COPY . /home/bookingblog

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn pymysql

EXPOSE 8080

ENTRYPOINT ["python3"]
CMD ["booking.py"]