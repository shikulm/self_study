Приложение используется для поддержки самообучения студентов. 
В системе реализован функционал размещения обучющей инфорамции по прдеметам и их разделам, просмотр обучающих материалов, промежуточное и итоговое тестирование, вывод статистики с результатми тестирования  
Работать с программой могут только авторизованные пользователи.
Доступ к моделям (CRUD) осуществляется через API или административную панель (http://127.0.0.1:8000/admin/).
Для тестирования работы эндпоинтов рекомендуется использовать Postman.
Более подробную информацию по проекту, включая описание структуры моделей можно посмотреть в файле "docs/Описане программы.docx" или в документации по url "http://127.0.0.1:8000/redoc/"

![img_1.png](труктура БД)

<h3> Функции системы: </h3>

- Регистрация и авторизация пользователй
- Добавление, редактирование и просмотр справолчников и обучающих материалов (пользоватлей, предметов, их разделов, url-ссылок на дополнительные материалы, вопросов к разделам для тестирования)
- Поиск обучающих материалов по парамтерам
- Предоставление или запрет обучаюшимся доступа к материалам раздела для изучения и тестирования
- Просмотр обучающих матриеалов
- Генерация тестов
- Прохождение студентами тестирования
- Оценка результатов тестирования
- Вывод статистики по результатам тестирования


<h3> Разрешения </h3>
Все пользователи могут регистрироваться и авторизоваться в приложении. 

Также есть 3 категории пользователей с различными правами:

- Администратор имеет доступ ко всему функционалу системы. Он может редактировать все данные, просматривать списки зарегистрированных пользователей, получать информацию по всем предметам и разделам.
- Автор предмета – создает, редактирует и удаляет данные по предметам и их разделам, заполняет вопросы для тестирования по разделам, прикрепляет ссылки на дополнительные материалы для раздела, записывает студентов на свои предметы, также может получать списки предметов под его авторством и просматривать результаты тестирования студентов по своим предметам.
- Студент – может получить список всех предметов без детализации информации, просматривать детальную информацию по предметам и разделам, к которым ему предоставлен доступ. Студент может пройти промежуточное (по отдельному разделу) и итоговое (по всему курсу) тестирование и посмотреть результаты своего тестирования. 


<h3> Перед выполнением проекта в Ubuntu или терминале выполните команды </h3>

Активация среды окружения (для Linux):
> source env/bin/activate 

Установка библиотек (достаточно выполнить в первый раз):
> python -m pip install -r requirement.txt
 
Создание БД:

> sudo -u postgres psql

Создать БД (Если имя БД отдичается от ):

> create database self_study

Создать файл с настройками .env по аналогии с римером example.env


Последующие действия должны выполняться каждый раз при запуске приложения.

Запуск служб:
> sudo service postgresql start

> sudo service redis-server start 

Запуск сервера:
>  python manage.py runserver

<h3> Архитектура приложения </h3>
Программа представляет собой API-приложение. API-запросы пользователей и ответы на них передаются в json-формате. Для реализации программы используются DRF и СУБД Postgresql. Также можно работать со всеми моделями через панель администратора Django (только там сейчас не очень удобный интерфейс для некоторых объектов и не учитываются права пользователей). Документация по программе формируется автоматически с помощью Swagger.
Структура моделей базы данных приведена на рисунках 2-3.
Функционал системы распределен между тремя приложениями:

•	Users – регистрация, авторизация пользователей, вывод списка пользователей

•	Study – выполнение операций CRUD для справочников предметов, разделов и дополнительных материалов

•	Tests_study – генерация тестов, прохождение тестирования, оценка и вывод результатов тестирования.

Пользователи регистрируются по электронной почте. Также можно указать фамилию, имя пользователя, прикрепить аватар. Верификации почты на данный момент не предусмотрена. Для авторизации пользователей используется JWT (JSON Web Token).

Предмет состоит из разделов, к разделу могут быть прикреплены url-ссылки на дополнительные материалы (предусмотреть возможность прикрепления материалов и для всего курса? Разные виды материалов?). Все данные может создавать, редактировать, удалять автор предмета. Также возможен поиск по предметам и их разделам с применением параметров api-запроса для администратора, автора курса и подписанных студентов. Для поиска используются библиотеки SearchFilter, OrderingFilter, DjangoFilterBackend.

Для того, чтобы студент мог просматривать материалы предмета, автор добавляет ссылку на него в таблицу AccessSubjectGroup. Для запрета доступа автор удаляет из этой таблицы соответствующую запись.
Для каждого раздела можно добавить вопросы с вариантами ответов для тестирования. Количество вопросов, включаемых в тест из каждого раздела, настраиваются автором предмета (если вопросов будет недостаточно, то будут добавлены все имеющиеся вопросы раздела). Вопросы различаются по сложности (от 1 до 5, по умолчанию 1). В программе используются только вопросы с альтернативными ответами (можно выбрать только один вариант ответа из предложенных).

Тесты генерируются каждый раз заново из заполненных автором предмета вопросов. При генерации теста вопросы и ответы на них перемешиваются случайным образом. Тесты могут быть двух типов – промежуточные (по отдельному разделу) и итоговые (по всему предмету).

