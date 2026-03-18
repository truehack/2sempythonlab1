# lab1

## Цель работы
```Освоить duck typing и контрактное программирование на примере источников задач в платформе обработки задач.```

## Ход работы с репозиторием:
```
1) git clone https://github.com/truehack/2sempythonlab1.git
2) cd 2sempythonlab1
3) pip install pytest pytest-cov typing-extensions
4) python main.py
5) python -m pytest --cov=main test_lab1.py -v  (запуск тестов с покрытием)
6) python -m pytest test_lab1.py  (запуск тестов без покрытия)
```

## Запуск с помощью Docker:
```
1) сборка образа: docker build -t lab1-tests .
2) Запуск тестов с покрытием: docker run --rm lab1-tests
```
