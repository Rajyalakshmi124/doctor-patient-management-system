FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install flask pymysql cryptography flask_jwt_extended google-auth requests
EXPOSE 8000
ENV DB_PORT=3306
CMD ["python3", "main.py"]
