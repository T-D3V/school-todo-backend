FROM python:3-slim
RUN pip3 install --upgrade pip
RUN adduser worker
USER worker
WORKDIR /home/worker
COPY --chown=worker:worker requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
ENV PATH="/home/worker/.local/bin:${PATH}"
WORKDIR /app
RUN mkdir log
WORKDIR /app/src
copy --chown=worker:worker . .
EXPOSE 8080
RUN flask migrate upgrade
RUN flask pre-populate
CMD ["gunicorn","-k","gevent","--config","gunicorn_config.py","app:create_app()"]