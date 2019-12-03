FROM python:3

WORKDIR /app
COPY . /app
RUN pip install flask gunicorn
RUN pip install -r requirements.txt
ENV FLASK_ENV=development
ENV DATABASE_URL=postgres://postgres:pgijtsaMS@db-docker:5432/apidb
RUN chmod u+x ./scripts.sh
EXPOSE 8000
CMD ["./scripts.sh"]
