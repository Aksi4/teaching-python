#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
import os

form = cgi.FieldStorage()

# Отримання значення лічильника з кукі
count = 0
if "HTTP_COOKIE" in os.environ:
    cookies = os.environ["HTTP_COOKIE"].split('; ')
    for cookie in cookies:
        name, value = cookie.strip().split('=')
        if name == "count":
            count = int(value)

# Перевірка, чи користувач натиснув кнопку для скидання лічильника
if "reset_count" in form:
    # Видаляємо куку
    print("Set-Cookie: count=0; path=/")

# Якщо користувач відправив форму, збільшимо лічильник
if "name" in form:
    count += 1
    print(f"Set-Cookie: count={count}; path=/")

print("Content-type: text/html\n")

# Отримання даних з форми
name = form.getvalue("name")
email = form.getvalue("email")
gender = form.getvalue("gender")
country = form.getvalue("country")
subscribe = form.getvalue("subscribe")

# Виведення даних користувача
print(f"<h1>Ваші дані:</h1>")
print(f"<p>Ім'я: {name}</p>")
print(f"<p>Email: {email}</p>")
print(f"<p>Стать: {gender}</p>")
print(f"<p>Країна: {country}</p>")
if subscribe:
    print("<p>Приколіст з почуттям гумору: Погодженно</p>")
else:
    print("<p>Приколіст з почуттям гумору: Провалено</p>")

# Виведення лічильника та кнопки для видалення cookies
print(f"<h1>Лічильник заповнених форм: {count}</h1>")

print('<form method="post" action="/cgi-bin/process_form.py">')
print('<input type="hidden" name="count" value="0">')
print('<input type="submit" value="Скинути лічильник" name="reset_count">')
print('</form>')


# Додамо кнопку для повторного заповнення форми
print('<form method="get" action="/form.html">')
print('<input type="submit" value="Повторно заповнити форму">')
print('</form>')
