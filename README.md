# Игра «Змейка»

Автор: Подаруев Дмитрий (ddqof.vvv@gmail.com)

## Описание
Данное приложение является реализацией игры «Змейка»

## Требования
В программе используется только встроенные в Python модули

## Состав
* Основной модуль - `snake_engine.py`
* Модуль с реализацией компонентов змейки - `snake_components.py`
* Конфигурационный файл - `config.py`

## Запуск приложения
Для запуска приложения необходимо запустить файл `snake_engine.py`

### Управление
* `W-A-S-D` или `Up-Down-Left-Right` - управление «змейкой»
* `Enter` или `Space` - перезапуск игры после ее окончания

### Правила игры
Данная реализация отличается от Vanilla версии. Змейка «ест» разную еду, отличающюся по цвету и по бонусам, `Красный блок` - +1 к очкам, `Синий блок` - +1 к очкам, ускорение на 3 секунды, `Зеленый блок` - дает x2 к очкам, также увеличивает змейку в 2 раза.    

### Изменение настроек
В конфигурационном файле `config.py` должны выставляться значения `WIDTH` и `HEIGHT`, делящиеся нацело на `BLOCK_SIZE ** 2`, скорость змейки `SNAKE_SPEED` может быть установлена любая. Значения `DEFAULT_FOOD_PROBABILITY`, `DOUBLE_LENGTH_PROBABILITY`, `SPEED_UP_PROBABILITY` - вероятности появления обычной, увеличивающей вдвое очки, увеличивающей скорость на 3 секунды еды соответственно. Эти значения также могут иметь любые значения. 
