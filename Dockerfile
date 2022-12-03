FROM python:3.10.8

WORKDIR /home/blog-simples

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -U

VOLUME [ "/home/blog-simples" ]

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]
