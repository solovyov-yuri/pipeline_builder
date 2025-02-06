Пока зи5 лежит)
Написал скрипты для сборки потока на стенде. Пока сырой, потестите, если есть желание.
1. Копирует файлы на сервер.
2. Запускает сборку.
3. Пишет лог в папку logs.
4. Создает ресурсы в провайдере.
5. Создает сущности в БД.


``` cmd
py -m venv .venv
.\.venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r .\requirements.txt
```


Раскатать на develop
``` cmd
py .\pipelene_builder\build_pipeline.py develop
```
Раскатать zi5
``` cmd
py .\pipelene_builder\build_pipeline.py zi5
```

Подключение к серверу с помощью ssh ключа.

Можно поменять на подключение с помощью пароля.

Подключение к провайдеру с помощью ssl сертификата.