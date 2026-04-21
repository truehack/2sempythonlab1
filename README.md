# lab4

## Цель работы
```Научиться реализовывать приложения с асинхронной моделью управления```

## Ход работы с репозиторием:
```
1) git clone https://github.com/truehack/2sempythonlab1.git
2) cd 2sempythonlab1
3) cd 4pythonlabsem2
4) pip install pytest pytest-cov typing-extensions
5) python main.py
6) python -m pytest --cov=main test_main.py -v  (запуск тестов с покрытием)
7) python -m pytest test_main.py  (запуск тестов без покрытия)
```

## Запуск с помощью Docker:
```
1) сборка образа: docker build -t lab4-tests .
2) Запуск тестов с покрытием: docker run --rm lab4-tests
```
