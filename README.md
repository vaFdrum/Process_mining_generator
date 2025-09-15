# Process Mining Generator

Простая модульная заготовка генератора событий для process mining.
В проекте:
- core: case generation, csv writer, utils, configs
- multi_process_generator: поддержка мультипроцессных сценариев

## Запуск
Установите зависимости:
```
pip install tqdm pandas
```

Запуск простого генератора (внутри пакета):
```
python -m process_mining_generator.main --config custom --cases 200
```

Сгенерированные события сохраняются в папке `dataset/` по умолчанию.

## Структура
- process_mining_generator/
  - logger.py
  - config.py
  - constants.py
  - utils.py
  - case_generator.py
  - csv_writer.py
  - main.py
- multi_process_generator/
  - config.py
  - case_linker.py
  - cross_process_generator.py

Это стартовая версия — расширяй по необходимости.
