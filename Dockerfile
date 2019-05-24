FROM python:3.7.3-slim

ENV APP_PATH /usr/src/app
ENV TIMEZONE 'America/Manaus'
WORKDIR $APP_PATH

RUN mkdir -p $APP_PATH \
  && apt-get update && apt-get install -y \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    build-essential \
    ncurses-dev \
    libjpeg62-turbo-dev \
    libpq-dev \
    libpng-dev \
    gettext \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/* \
  && echo $TIMEZONE > /etc/timezone \
  && rm /etc/localtime \
  && ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime \
  && dpkg-reconfigure -f noninteractive tzdata


COPY . $APP_PATH

RUN pip install --upgrade pip setuptools \
  && pip install --no-cache-dir -r requirements.txt \
  && mkdir -p assets/static \
  && python manage.py collectstatic --noinput

#ENTRYPOINT ['python', '/usr/src/app/manage.py', 'runserver', '0.0.0.0:9000']
