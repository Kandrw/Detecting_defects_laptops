    Проект по Опознованию Дефектов Ноутбуков
    Описание
    Данный проект представляет собой систему для опознования дефектов на ноутбуках с использованием нейронной сети. Он включает в себя как бэкенд, так и фронтенд компоненты, позволяющие пользователям загружать фотографии ноутбуков и получать результаты проверки.
    
    Создание окружения
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    
    Запуск backend
    python3 manage.py runserver
    
    Запуск frontend
    Тестовая сборка:
    npm install
    npm run dev
    
    Продакшн сборка:
    npm run build
    npm install -g serve
    serve -s build
    
    Структура backend
    back-frontend/
    |
    ├── Detecting_defects_laptops/
    │   └── init.py
    │   └── asgi.py
    │   └── settings.py
    │   └── urls.py
    │   └── wsgi.py
    │
    ├── detecting_defects_laptops_soft/
    │   ├── migrations/
    │   │   └── 0001_initial.py
    │   │   └── init.py
    │
    │   └── init.py
    │   └── admin.py
    │   └── apps.py
    │   └── models.py
    │   └── serializers.py
    │   └── tests.py
    │   └── urls.py
    │   └── views.py
    │
    └── db.sqlite3
    └── manage.py
    
    Структура ml
    hacaton/
    │
    ├── configs/                          # Папка с конфигурационными файлами
    │   ├── classification/
    │   │   └── hyperparams.json           # Гиперпараметры для классификации
    │   ├── detection/
    │   │   └── hyperparams.json           # Гиперпараметры для детекции
    │   └── data.yaml                      # Конфигурация данных для YOLO
    │
    ├── data/                              # Папка с исходными и разбитыми данными
    │   ├── source/                        # Исходные данные (изображения и лейблы)
    │   │   ├── images/                    # Изображения
    │   │   └── labels/                    # Текстовые файлы лейблов (аннотации YOLO)
    │   ├── train/                         # Тренировочные данные
    │   ├── valid/                         # Валидационные данные
    │   └── test/                          # Тестовые данные
    │
    ├── models/                            # Папка с моделями
    │   ├── classification.py              # Реализация модели классификации
    │   ├── detection.py                   # Реализация модели детекции
    │   └── save_model/                    # Папка для сохранения обученных моделей
    │       ├── classification_model.pth   # Сохраненная модель классификации
    │       └── detection_model.pth        # Сохраненная модель детекции
    │
    ├── utils/                             # Вспомогательные утилиты
    │   ├── custom_image_dataset.py        # Файл с реализацией кастомного датасета
    │   ├── data_loader.py                 # Загрузчик данных для тренировки и валидации
    │   ├── train_helper.py                # Вспомогательные функции для тренировки
    │   └── split_data.py                  # Скрипт для разбиения данных на train/valid/test
    │
    ├── runs/                              # Директория с результатами детекции YOLOv5
    │
    ├── train.py                           # Основной файл для тренировки обеих моделей
    ├── run_predictions.py                 # Файл для прогноза по загруженному изображению
    ├── fine_tune.py                       # Скрипт для дообучения моделей на новых данных
    ├── split_data.py                      # Скрипт для разбиения данных перед обучением
    ├── requirements.txt                   # Список зависимостей для проекта
    └── README.md                          # Описание проекта
