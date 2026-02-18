# Process Mining Data Generator

Генератор синтетических event logs для Process Mining.
Создает реалистичные CSV-данные с бизнес-процессами, аномалиями, рабочим календарем и пулом сотрудников.

---

## Возможности

- **5 бизнес-процессов** с несколькими сценариями каждый (всего 17 вариантов)
- **9 предустановленных конфигов** — от 50MB до 50GB
- **Бизнес-календарь** — рабочие часы по типу процесса, пропуск выходных
- **Сезонные коэффициенты** — Q1-Q4 влияют на длительность и ожидание
- **Пул сотрудников** — 76 постоянных сотрудников с ролями и efficiency-рейтингом
- **Аномалии и rework** — 6 типов аномалий, 3 типа переделок
- **Адаптивный батчинг** — генерация батчами с точностью ~100.5% от целевого размера
- **Воспроизводимость** — параметр `--seed` для повторяемых результатов

---

## Установка

```bash
git clone <repo-url>
cd Process_mining_generator
pip install -r requirements.txt
```

Или через pyproject.toml (с dev-зависимостями для тестов):

```bash
pip install -e ".[dev]"
```

> **Зависимости:** Python 3.8+, tqdm

---

## Использование

```bash
# Предустановленный конфиг
python main.py --config 1GB

# Доступные конфиги: 50MB, 500MB, 750MB, 1GB, 5GB, 10GB, 20GB, 30GB, 50GB
python main.py --config 50MB
python main.py --config 5GB

# Кастомный размер
python main.py --config custom --size 2.5

# Указать выходную директорию
python main.py --config 1GB --output ./my_data/

# Воспроизводимая генерация (seed)
python main.py --seed 42 --config 1GB      # фиксированный seed — одинаковый результат
python main.py --seed 123 --config 1GB     # другой seed → другие данные
python main.py --config 1GB                # без seed → случайные данные каждый раз
```

### CLI-аргументы

| Аргумент   | Описание                                                                 |
|------------|--------------------------------------------------------------------------|
| `--config` | Пресет размера: `50MB`, `500MB`, `750MB`, `1GB`, `5GB`, `10GB`, `20GB`, `30GB`, `50GB`, `custom` |
| `--size`   | Размер в GB (только для `--config custom`)                               |
| `--output` | Выходная директория (по умолчанию `./dataset/`)                          |
| `--seed`   | Seed для воспроизводимости результатов                                   |

---

## Бизнес-процессы

| Процесс              | Сценариев | Рабочие часы | Сезонный пик |
|-----------------------|-----------|--------------|--------------|
| **OrderFulfillment**  | 5 (вкл. отмену, retry платежа, QC)       | 8:00–22:00  | Q4 (x1.5) |
| **CustomerSupport**   | 3 (вкл. эскалацию, доп. поддержку)       | 8:00–20:00  | Q4 (x1.2) |
| **LoanApplication**   | 3 (вкл. доп. документы, отказ)            | 9:00–18:00  | Q1 (x1.2) |
| **InvoiceProcessing** | 3 (вкл. ошибку валидации, отклонение)     | 9:00–17:00  | Q4 (x1.3) |
| **HRRecruitment**     | 3 (вкл. доп. собеседование, отказ)        | 9:00–18:00  | Q1 (x1.3) |

---

## Аномалии и переделки

### Аномалии (вероятность 2–3% по конфигу)

| Тип                  | Длительность | Применяется к                                                      |
|----------------------|--------------|--------------------------------------------------------------------|
| Manual Override      | 30–120 мин   | Payment Processing, Document Review, Invoice/Loan Approval         |
| Fraud Investigation  | 4–24 часа    | Payment Processing, Credit Check, Application Review               |
| System Outage        | 1–8 часов    | Payment Processing, Data Entry, Application Review, Ticket Created |
| Quality Issue        | 15–180 мин   | Quality Check, Pick Items, Document Review, Data Entry             |
| Technical Problem    | 30–240 мин   | Issue Investigation, Credit Check, Data Entry, Payment Processing  |
| Data Inconsistency   | 1–6 часов    | Document Review, Data Entry, Application Review, Invoice Received  |

### Переделки / rework (вероятность 6–8%, длительность 15–90 мин)

| Тип                     | Применяется к                                          |
|-------------------------|--------------------------------------------------------|
| Re-check                | Quality Check, Document Review, Data Entry, Credit Check |
| Re-approval             | Invoice Approval, Loan Approval, Offer Extended        |
| Additional Verification | Document Review, Application Review, Credit Check      |

---

## Конфигурации

| Конфиг  | Размер   | Период данных | Аномалии | Rework | Начало     |
|---------|----------|---------------|----------|--------|------------|
| `50MB`  | 0.05 GB  | 90 дней       | 3%       | 8%     | 2024-01-01 |
| `500MB` | 0.5 GB   | 180 дней      | 3%       | 8%     | 2023-07-01 |
| `750MB` | 0.75 GB  | 270 дней      | 3%       | 8%     | 2023-04-01 |
| `1GB`   | 1.0 GB   | 365 дней      | 3%       | 8%     | 2023-01-01 |
| `5GB`   | 5.0 GB   | 2 года        | 3%       | 8%     | 2022-01-01 |
| `10GB`  | 10.0 GB  | 3 года        | 3%       | 8%     | 2022-01-01 |
| `20GB`  | 20.0 GB  | 3 года        | 3%       | 8%     | 2022-01-01 |
| `30GB`  | 30.0 GB  | 5 лет         | 2.5%     | 7%     | 2021-01-01 |
| `50GB`  | 50.0 GB  | 7 лет         | 2%       | 6%     | 2019-01-01 |

**Распределение процессов** (конфиги 50MB–20GB):
OrderFulfillment 40% | CustomerSupport 25% | LoanApplication 15% | InvoiceProcessing 12% | HRRecruitment 8%

---

## Формат CSV

Выходной файл: `<output_dir>/process_log_<size>GB.csv`

### Поля (17 колонок)

| Поле              | Тип       | Описание                                      |
|-------------------|-----------|-----------------------------------------------|
| `case_id`         | int       | Уникальный ID кейса                           |
| `timestamp_start` | datetime  | Начало активности                             |
| `timestamp_end`   | datetime  | Окончание активности                          |
| `process`         | str       | Тип процесса                                  |
| `activity`        | str       | Название активности                           |
| `duration_minutes`| int       | Длительность в минутах                        |
| `role`            | str       | Роль исполнителя (Clerk, Manager, System и др.) |
| `resource`        | str       | Имя сотрудника ("Иванов А.")                  |
| `resource_id`     | str       | ID сотрудника (EMP-0001) или SYSTEM           |
| `anomaly`         | bool      | Флаг аномалии                                 |
| `anomaly_type`    | str/null  | Тип аномалии                                  |
| `rework`          | bool      | Флаг переделки                                |
| `user_id`         | str       | ID пользователя (case-level)                  |
| `department`      | str       | Отдел (case-level)                            |
| `priority`        | str       | Приоритет: low / medium / high / critical / urgent |
| `cost`            | float     | Стоимость кейса                               |
| `comment`         | str       | Бизнес-комментарий                            |

> Поля `user_id`, `department`, `priority`, `cost`, `comment` — одинаковые для всех событий одного кейса.

---

## Архитектура

```
main.py              — CLI и оркестрация генерации (адаптивный батчинг)
config.py            — 9 предустановленных конфигов, модели процессов, сезонные множители
constants.py         — длительности активностей, аномалии, rework, стоимости, комментарии
case_generator.py    — генерация кейсов и событий, роли, аномалии, rework
business_calendar.py — рабочие часы по процессам, пропуск выходных
resource_pool.py     — пул из 76 сотрудников с efficiency-рейтингом
csv_writer.py        — запись в CSV с форматированием
utils.py             — сезонность, длительности, вероятности аномалий/rework
logger.py            — логирование + tqdm прогресс-бар
```

---

## Тесты

```bash
# Запуск всех тестов
python -m pytest tests/ -v

# С покрытием
python -m pytest tests/ --cov=. --cov-report=term
```

132 теста: бизнес-логика, бизнес-календарь, генерация кейсов, CSV-запись, конфигурации, интеграция.

---

## Лицензия

MIT
