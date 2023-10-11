#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
import os

form = cgi.FieldStorage()

count = 0
if "HTTP_COOKIE" in os.environ:
    cookies = os.environ["HTTP_COOKIE"].split('; ')
    for cookie in cookies:
        name, value = cookie.strip().split('=')
        if name == "count":
            count = int(value)

if "reset_count" in form:

    print("Set-Cookie: count=0; path=/")

if "name" in form:
    count += 1
    print(f"Set-Cookie: count={count}; path=/")

print("Content-type: text/html\n")

name = form.getvalue("name")
email = form.getvalue("email")
gender = form.getvalue("gender")
country = form.getvalue("country")
subscribe = form.getvalue("subscribe")

print(f"<h1>Ваші дані:</h1>")
print(f"<p>Ім'я: {name}</p>")
print(f"<p>Email: {email}</p>")
print(f"<p>Стать: {gender}</p>")
print(f"<p>Країна: {country}</p>")
if subscribe:
    print("<p>Приколіст з почуттям гумору: Погодженно</p>")
else:
    print("<p>Приколіст з почуттям гумору: Провалено</p>")

print(f"<h1>Лічильник заповнених форм: {count}</h1>")

print('<form method="post" action="/cgi-bin/process_form.py">')
print('<input type="hidden" name="count" value="0">')
print('<input type="submit" value="Скинути лічильник" name="reset_count">')
print('</form>')

print('<form method="get" action="/form.html">')
print('<input type="submit" value="Повторно заповнити форму">')
print('</form>')
