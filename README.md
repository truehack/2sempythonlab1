# lab2

## Цель работы
```Освоить управление доступом к атрибутам и защиту инвариантов доменной модели```

## Ход работы с репозиторием:
```
1) git clone -b lab2 https://github.com/truehack/2sempythonlab1.git
2) cd 2sempythonlab1
3) pip install pytest pytest-cov typing-extensions
4) python main.py
5) python -m pytest --cov=main test_main.py -v  (запуск тестов с покрытием)
6) python -m pytest test_main.py -v  (запуск тестов без покрытия)
```

## Запуск с помощью Docker:
```
1) сборка образа: docker build -t lab2-python .
2) Запуск тестов: docker run --rm lab2-python
```
