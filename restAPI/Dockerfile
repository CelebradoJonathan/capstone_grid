FROM python:3

WORKDIR /app
COPY . /app
RUN pip install flask gunicorn
RUN pip install -r requirements.txt
ENV FLASK_ENV=development
ENV DATABASE_URL=postgres://postgres:pgijtsaMS@host.docker.internal:5432/joborderdb
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]