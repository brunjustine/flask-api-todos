FROM python:latest
LABEL "Author"="Justine Brun brunjustin@eisti.eu"
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY api.py /app/api.py 
COPY app /app/app

EXPOSE 5000

CMD [ "python3", "api.py" ]