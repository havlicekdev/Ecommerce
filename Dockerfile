# pull base image
FROM python:3.12.1-bookworm

# set environment variables

# set working directory
WORKDIR /app

# install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy app
COPY . .

# run server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
