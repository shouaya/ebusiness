#!/bin/sh
if [[ ! -d ebusiness ]]; then
  #mkdir ebusiness
  git clone https://github.com/ebusiness/ebusiness.git #./
fi

cd ebusiness

git pull

if [[ ! -d log ]]; then
  mkdir log
fi

if [[ ! -d log/batch ]]; then
  mkdir log/batch
fi

python manage.py runserver 0.0.0.0:80
