#!/usr/bin/env bash

sqlacodegen --noinflect postgresql+psycopg2://btrabon:btrabon@127.0.0.1/news_blog  > models_raw.py