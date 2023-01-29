FROM python:3.7-alpine3.12
WORKDIR /app
COPY requirements.txt /app
COPY /src/app /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]x
