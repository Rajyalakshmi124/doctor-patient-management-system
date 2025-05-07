FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install flask pymysql
RUN pip install cryptography
EXPOSE 8000
ENV DB_HOST=db
ENV DB_USER=root
ENV DB_PASSWORD=root
ENV DB_NAME=trainingPoc
ENV DB_PORT=3306
CMD ["python3", "main.py"]
