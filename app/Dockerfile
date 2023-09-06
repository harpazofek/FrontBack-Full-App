FROM python:3.10.11-alpine3.17
WORKDIR /app
COPY req*.txt .
RUN pip install -r req*.txt
COPY . .
EXPOSE 5200
ENTRYPOINT [ "python3","ping-pong.py" ]