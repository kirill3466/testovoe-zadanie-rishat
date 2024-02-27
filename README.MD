# testovoe-zadanie-rishat

## Задание:
Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:
 - [✔]	Django Модель Item с полями (name, description, price) 
 - [✔]	API с двумя методами:
   - GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса
   -	GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее  с помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id)
 - [✔]	Залить решение на Github, описать запуск в Readme.md
 - [✔]	Опубликовать свое решение чтобы его можно было быстро и легко протестировать.

## Дополнительные задачи: 
 - [✔]	Запуск используя Docker
 - [✔]	Использование environment variables
 - [✔]	Просмотр Django Моделей в Django Admin панели
 - [❌]	Запуск приложения на удаленном сервере, доступном для тестирования
 - [✔]	Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
 - [✔]	Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
 - [✔]	Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме. 
 - [❌]	Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
 - [✔]	Реализовать не Stripe Session, а Stripe Payment Intent.
## Как проверить:
Склонировать репозиторий:
```
git clone https://github.com/kirill3466/testovoe-zadanie-rishat.git
```
Собрать контейнер:
```
docker-compose up --build
```
Либо сразу запустить сервер после установки зависимостей:
```
venv\Scripts\Activate
pip install -r requirements.txt
python manage.py runserver
```
## Вход в админку дефолтный: admin admin
## Выполняем запросы, в бд уже есть данные по 1, 2 id:

### GET item / order:
```
curl -X GET http://localhost:8000/item/1
curl -X GET http://localhost:8000/order/1
```
Тут выдает простые документы
### GET buy item / order:
```
curl -X GET http://localhost:8000/buy/1


curl -X GET http://localhost:8000/buy_order/1
```
Должно выдавать айдишники сессий
### GET payment intent:
```
-X GET http://localhost:8000/payment_intent/1
```
Тут выдает айди "Намерения о покупке" (В лк страйпа появляется незавершенный платеж)

# Важно:
При создании новых объектов order, items должны иметь одинаковую валюту
Для проверки вручную можно использовать 5454 5454 5454 5454 в поле для карты

# Мои результаты (история оплаты в лк страйпа, запросы) скриншотами:
https://imgur.com/a/xIdyS4O
