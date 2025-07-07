# CSV Processor

Скрипт для обработки CSV файлов с возможностью фильтрации и агрегации данных.

## Функции

- **Фильтрация**: Поддержка операторов `>`, `<`, `=` для любых колонок
- **Агрегация**: Расчет среднего (`avg`), минимального (`min`) и максимального (`max`) значений для числовых колонок
- **Красивый вывод**: Форматированные таблицы в консоли

## Использование

### Фильтрация данных

```bash
python csv_processor.py sample_data.csv --where "price>500"
python csv_processor.py sample_data.csv --where "brand=xiaomi"
python csv_processor.py sample_data.csv --where "rating<4.5"
```

### Агрегация данных

```bash
python csv_processor.py sample_data.csv --aggregate "price=avg"
python csv_processor.py sample_data.csv --aggregate "rating=min"
python csv_processor.py sample_data.csv --aggregate "price=max"
```

## Примеры запуска

### Фильтрация по цене больше 500

```bash
python csv_processor.py sample_data.csv --where "price>500"
```

Результат:
```
Filtered results for: price > 500
Found 4 records:

+----------------+----------+-------+--------+
| name           | brand    | price | rating |
+================+==========+=======+========+
| iphone 15 pro  | apple    | 999   | 4.9    |
+----------------+----------+-------+--------+
| galaxy s23 ultra| samsung  | 1199  | 4.8    |
+----------------+----------+-------+--------+
| pixel 7 pro    | google   | 599   | 4.7    |
+----------------+----------+-------+--------+
| oneplus 11     | oneplus  | 699   | 4.5    |
+----------------+----------+-------+--------+
```

### Агрегация - средняя цена

```bash
python csv_processor.py sample_data.csv --aggregate "price=avg"
```

Результат:
```
Aggregation results:

+-----------+----------+
| Metric    | Value    |
+===========+==========+
| Operation | Average  |
+-----------+----------+
| Column    | price    |
+-----------+----------+
| Value     | 632.50   |
+-----------+----------+
```

## Тестирование

Запуск тестов:

```bash
pytest test_csv_processor.py -v
```

Запуск с покрытием:

```bash
pytest test_csv_processor.py --cov=csv_processor --cov-report=html
```

## Требования

- Python 3.11+
- tabulate (для красивого вывода)
- pytest (для тестирования)
- pytest-cov (для покрытия тестами)

## Архитектура

Проект использует модульную архитектуру, что позволяет легко добавлять новые операции агрегации или команды:

- `CSVProcessor` - основной класс для обработки CSV
- Функции парсинга условий отделены от логики обработки
- Легко расширяемая система операторов и агрегаций
