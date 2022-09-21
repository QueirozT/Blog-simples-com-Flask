FROM python:3.10-slim

RUN useradd blog-simples

WORKDIR /home/blog-simples

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -U


USER blog-simples

VOLUME [ "/home/blog-simples" ]

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]