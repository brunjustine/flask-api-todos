FROM python:latest
LABEL "Author"="Justine Brun brunjustin@eisti.eu"
WORKDIR /app/api

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python3" , "MyAPI/api.py"]