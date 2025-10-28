## Содержание

* [Быстрый старт](#быстрый-старт)
* [JWT-аутентификация](#jwt-аутентификация)
* [RBAC и модель прав](#rbac-и-модель-прав)
  * [Сущности и связи](#сущности-и-связи)
  * [Примеры матрицы доступов](#примеры-матрицы-доступов)
* [Схема БД](#схема-бд)
* [Эндпойнты API](#эндпойнты-api)




---

## Быстрый старт

```bash
# 0) Установка зависимостей
pip install -e .

# 1) Конфиг
cp .env.example .env   # отредактируйте DATABASE_URL и JWT_SECRET

# 2) Миграции
python manage.py makemigrations accounts access
python manage.py migrate

# 3) Демоданные
python seed_demo.py

# 4) Запуск сервера
python manage.py runserver 0.0.0.0:8000
```

## JWT-аутентификация

**Поток:**

1. `POST /api/auth/login/` → выдаёт `access` (короткоживущий) и `refresh` (долгоживущий).
2. `POST /api/auth/logout/` — делает текущий access-токен недействительным (добавляет его в blacklist или помечает как отозванный).


Проверка подписи — по `JWT_SECRET`. Алгоритм — `HS256` (по умолчанию).

---

## RBAC и модель прав

### Сущности и связи

* **Permission**:

  * `resource`: строка, например `project`, `document`
  * `action`: `create | read | update | delete `
  * `scope`: `own | any`
* **Role** — логические наборы прав.
* **UserRole** — присвоение роли пользователю (уникально по `(user, role)`).



### Примеры матрицы доступов

| Роль     | Право                                                                                | Описание                       |
| -------- | ------------------------------------------------------------------------------------ | ------------------------------ |
| `admin`  | `project:read:any`, `project:create:any`, `project:update:any`, `project:delete:any` | Полный доступ к проектам       |
| `editor` | `project:read:any`, `project:update:own`                                             | Читает все, правит только свои |
| `viewer` | `project:read:any`                                                                   | Только чтение                  |

---

## Схема БД



| Таблица                   | Назначение                  | Основные поля / связи                                                                                |
| ------------------------- | --------------------------- | ---------------------------------------------------------------------------------------------------- |
| **accounts_user**         | Пользователь                | `email`, `password_hash`, `is_active`, `created_at`                                                  |
| **access_role**           | Роль                        | `name`, `description`                                                                                |
| **access_permission**     | Право доступа               | `resource`, `action`, `scope` (`own` / `any`)                                                        |
| **access_userrole**       | Связь *пользователь ↔ роль* | `user_id → accounts_user.id`, `role_id → access_role.id`, `UNIQUE(user_id, role_id)`                 |
| **access_rolepermission** | Связь *роль ↔ право*        | `role_id → access_role.id`, `permission_id → access_permission.id`, `UNIQUE(role_id, permission_id)` |
| **access_revokedtoken**   | Отозванные JWT-токены       | `jti (PK)`, `user_id → accounts_user.id`, `revoked_at`                                               |



---

## Эндпойнты API


```text
/api/
├── auth/                     # аутентификация и профиль
│   ├── register/             (POST) регистрация
│   ├── login/                (POST) вход, выдаёт access/refresh
│   ├── logout/               (POST) делает текущий access-токен недействительным (добавляет его в blacklist или помечает как отозванный)
│   └── profile/              (GET/PATCH/DELETE) профиль пользователя

├── admin/                    # управление ролями и правами
│   ├── roles/                                (GET, POST) список / создание роли
│   ├── permissions/                          (GET, POST) список / создание прав
│   ├── roles/<role_id>/permissions/          (GET, POST) права роли / выдать право роли
│   └── users/<user_id>/roles/                (GET, POST) роли пользователя / назначить роль пользователю

├── resources/                # мок-ресурсы для проверки own/any
│   ├── projects/             (GET)
│   └── documents/            (GET)

└── health/                   (GET) health check — проверка доступности сервиса
```




