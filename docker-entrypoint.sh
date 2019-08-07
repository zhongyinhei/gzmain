#!/bin/sh
nginx -g "daemon on;" && uwsgi --ini /programe/uwsgi.ini