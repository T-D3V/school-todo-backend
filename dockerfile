FROM python:3-slim
COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8080
RUN flask migrate upgrade
RUN flask pre-populate
CMD ["gunicorn","--config","gunicorn_config.py", "app:create_app()"]