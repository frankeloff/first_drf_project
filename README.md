# Тестовое задание для: Python[Django] разработчика
## Быстрый старт
- Используйте .env файл. Вы можете скопировать .env.example
- Используйте `python3 -m venv ./.venv && source ./.venv/bin/activate && pip install -r requirements.txt` (необязательно, нужно только для того, если будет потребность в запуске без докера)
- Запустите команду `docker compose up -d --build`
- Выполните миграции `docker exec app python ./my_proj/manage.py migrate`
### Последующие запуски выполняются следующим образом
- Запускаете команду `sudo docker compose up -d`
## Запуск тестов
 - Выполните команду `docker exec my_app python ./my_proj/manage.py test comp`
 Тесты преднозначены для тестирования всех API.
## Описание API
### PS: Заведение, которое есть на рынке - это значит, что данное предприятие есть в таблице EnterpriseService, т.е. оно связано с каким-то товаром/услугой (у предприятия есть на рынке какие-то товары/услуги). Товары/услуги, которые есть в продаже - это значит, что товары/услуги есть в таблице EnterpriseService, т.е. связаны с каким-то предприятием (товар/услуга есть в наличии у какого-то предприятия => есть в продаже).
- `api/v1/service/add/` - Добавление тоавара/услуги
- `api/v1/organizations/<int:district_id>/` - Список заведений с условием заранее выбранного района. Для данного API доступны следующие фильтры:
    - Поиск по категории, например: `api/v1/organizations/1/?category_name=Для%20ухода`
    - Поиск по цене (меньше, больше), например: `api/v1/organizations/1/?price__lt=200`
    - Одновременный поиск по категории и цене, например: `api/v1/organizations/1/?category_name=Для%20ухода&price__gt=200`
- `api/v1/organizations/all/details/` - Детальная информация о заведениях
- `api/v1/organizations/all/details/<int:pk>/` - Детальная информация о заведении
- `api/v1/organizations/active/details/` - Детальная информация о заведениях, которые есть на рынке
- `api/v1/organizations/active/details/<int:pk>/` - Детальная информация о заведении, которое есть на рынке
- `api/v1/services/all/details/` - Детальная информация о товарах/услугах
- `api/v1/services/all/details/<int:pk>/` - Детальная информация о товаре/услуге
- `api/v1/services/active/details/` - Детальная информация о товарах/услугах, которые есть в продаже
- `api/v1/services/active/details/<int:pk>/` - Детальная информация о товаре/услугe, который/которая есть в продаже