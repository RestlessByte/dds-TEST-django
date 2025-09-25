# `[🇷🇺 RU]`
# 🚀 Веб-сервис учёта ДДС (движение денежных средств)

Тестовое задание: веб-приложение для учёта поступлений и списаний денежных средств.  
Полный стек: **Django 5**, **Django REST Framework**, **SQLite**, **Bootstrap 5** (UI), чистый JS (AJAX).

---

## ⚙️ Возможности

- CRUD по записям ДДС:
  - дата (авто + редактируемая),
  - статус (Бизнес, Личное, Налог + расширяемый),
  - тип (Пополнение/Списание + расширяемый),
  - категория → подкатегория (иерархия),
  - сумма ₽,
  - комментарий.
- Фильтрация записей: по датам, статусу, типу, категории, подкатегории.
- Управление справочниками:
  - статусы, типы, категории, подкатегории.
  - связи: категория → тип, подкатегория → категория.
- UI:
  - Bootstrap-таблицы и формы,
  - кнопки **＋** рядом с каждым селектом (создание новых статусов/типов/категорий/подкатегорий прямо из формы),
  - AJAX-зависимости (выбор типа фильтрует категории, выбор категории фильтрует подкатегории).
- API (REST, JSON):
  - `GET /api/statuses/` + `POST`,
  - `GET /api/types/` + `POST`,
  - `GET /api/categories/?type={id}` + `POST`,
  - `GET /api/subcategories/?category={id}` + `POST`,
  - `GET /api/transactions/` (с фильтрами) + `POST`.

---

## 🔧 Установка и запуск

```bash
git clone <repo-url> dds
cd dds

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py makemigrations core
python manage.py migrate
python manage.py seed        # создаёт статусы, типы, примеры категорий/подкатегорий
python manage.py createsuperuser  # (опционально) админ
python manage.py runserver 0.0.0.0:8000
```
# 🖥️ Интерфейсы

- UI: http://localhost:8000/dds/
Таблица записей + фильтры + CRUD 
- Создание записи: http://localhost:8000/dds/new/
Кнопки ＋ для добавления справочников.
- Справочники: http://localhost:8000/dds/dicts/
- Админка: http://localhost:8000/admin/
- API: http://localhost:8000/api/

# Примеры :
```
GET /api/statuses/ → [{"id":1,"name":"Бизнес"}, …]

POST /api/types/
{"name":"Инвестиции"} → {"id":3,"name":"Инвестиции"}

GET /api/categories/?type=2
→ [{"id":5,"name":"Маркетинг","type":2}]

POST /api/transactions/
{"date":"2025-09-25","status":1,"type":2,"category":5,"subcategory":7,"amount":1234.56,"comment":"тест"}
```