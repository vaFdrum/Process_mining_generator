# Process Mining Generator

Гибкий генератор синтетических событий для задач **Process Mining**.  
Поддерживает как **однопроцессные сценарии** (отдельные бизнес-процессы), так и **мультипроцессные цепочки** (сквозные сценарии, например Order-to-Cash).

---

## 🚀 Установка

```bash
pip install tqdm pandas
```

---

## 🛠️ Использование

### 1. Генерация отдельных процессов

Запуск генерации кейсов для одного процесса или набора процессов по распределению:

```bash
python -m process_mining_generator.main --config custom --cases 200
```

- `--config` — выбор конфигурации (`20GB`, `30GB`, `50GB`, `custom`)  
- `--cases` — количество кейсов для генерации  
- `--output` — опционально задать директорию для сохранения CSV  

Результат: файл `dataset/events.csv`.

---

### 2. Генерация мультипроцессных цепочек

Модуль `multi_process_generator` поддерживает сквозные сценарии, например:

- **Order-to-Cash** (от заказа до оплаты)  
- **Lead-to-Opportunity** (от маркетинга до сделки)  

Пример кода:

```python
from process_mining_generator.multi_process_generator.cross_process_generator import CrossProcessGenerator, create_cross_process_summary
from process_mining_generator.multi_process_generator.config import MultiProcessType

gen = CrossProcessGenerator(MultiProcessType.ORDER_TO_CASH)
df = gen.generate(1000)  # 1000 кейсов
summary = create_cross_process_summary(df)

print(df.head())
print(summary)
```

---

## 📂 Структура проекта

```
process_mining_generator/
├── logger.py                 # Логгер с поддержкой прогресс-бара
├── main.py                   # CLI и точка входа
├── config.py                 # Конфигурации (20GB, 30GB, 50GB, custom)
├── constants.py              # Константы (роли, ресурсы, поля CSV)
├── utils.py                  # Утилиты (waiting time, распределение)
├── case_generator.py          # Генератор кейсов
├── csv_writer.py              # Запись в CSV
├── dataset/                  # Директория для результатов
└── multi_process_generator/  # Поддержка мультипроцессных сценариев
    ├── config.py             # Конфиги мультипроцессов
    ├── case_linker.py        # Связка кейсов между процессами
    ├── cross_process_generator.py # Генератор и метрики
    └── utils.py              # Утилиты
```

---

## 📊 Примеры использования

### Сгенерировать 500 кейсов с дефолтным конфигом:
```bash
python -m process_mining_generator.main --cases 500
```

### Сгенерировать 1000 кейсов и сохранить в другую папку:
```bash
python -m process_mining_generator.main --config 20GB --cases 1000 --output ./my_dataset
```

### Сгенерировать мультипроцессный сценарий Order-to-Cash:
```python
from process_mining_generator.multi_process_generator.cross_process_generator import CrossProcessGenerator
from process_mining_generator.multi_process_generator.config import MultiProcessType

gen = CrossProcessGenerator(MultiProcessType.ORDER_TO_CASH)
df = gen.generate(200)
print(df.head())
```

---

## 📝 TODO

- Добавить аномалии и реворки  
- Поддержка генерации через multiprocessing  
- Unit-тесты и CI
