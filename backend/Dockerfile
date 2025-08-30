FROM python:3.11-slim
WORKDIR /code
COPY ./app /code/app
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Environments
ENV API_KEY=skilerbfzsiwldwk
ENV API_URL=https://nova.astrometry.net/api/
ENV MACHINE=docker
ENV TRACE=0

VOLUME /images
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]