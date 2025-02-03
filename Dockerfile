FROM python:3.11.3
WORKDIR /opt/services/djangoapp/src
ENV PYTHONUNBUFFERED 1
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "Roulette/manage.py", "runserver", "0.0.0.0:8000"]