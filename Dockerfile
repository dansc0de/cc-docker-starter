# base image
FROM python:3.12-slim

# set working directory
WORKDIR /app

# copy dependencies first (better cache usage)
COPY app/requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY app/app.py .

# document the port
EXPOSE 5000

# run the application
CMD ["python", "app.py"]
