FROM python:3-slim
RUN pip3 install --upgrade pip
RUN adduser -D worker
USER worker
WORKDIR /home/worker
COPY --chown=worker:worker requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
ENV PATH="/home/worker/.local/bin:${PATH}"
WORKDIR /app
copy --chown=worker:worker . .
EXPOSE 8080
RUN flask migrate upgrade
RUN flask pre-populate
CMD ["gunicorn","--config","gunicorn_config.py", "app:create_app()"]