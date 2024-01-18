# Проект парсинга pep
В этом проекте реализован поиск информации о статусе всех существующих PEP, поиск ссылок на документацию, версии и статусы Python, поиск ссылок на документацию актуальной версии Python.

**Стек технологий:**
- Python 
- BeautifulSoup4 
#### Как запустить проект:

+ клонируем репозиторий
```
git clone `https://github.com/milkyaway13/bs4_parser_pep
```
+ переходим в корневую папку проекта
```
cd bs4_parser_pep
```
+ создаем виртуальное окружение
 ```
python -m venv env
```
+ активируем виртуальное окружение
```
source env/scripts/activate
```
 + устанавливаем зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
+ получаем информацию для справки
```
 python main.py -h
```

+ переходим в директорию с файлом main.py
```
cd src
```
+ запускаем парсер
```
python main.py pep -o file
```

## Автор
[Боярчук Василий](https://github.com/Milkyaway13/)
