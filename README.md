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
* Для запуска приложения необходимо запустить файл `py snake_engine.py`
* Запуск Vanilla версии: `py snake_engine.py --vanilla` 

### Управление
* `W-A-S-D` или `Up-Down-Left-Right` - управление «змейкой»
* `Enter` или `Space` - перезапуск игры после ее окончания

### Правила игры
Данная реализация отличается от Vanilla версии. Змейка «ест» различную еду, отличающюся по цвету и по бонусам, `Красный блок`: стандартная еда (+1 к очкам), `Синий блок`: ускорение на 3 секунды (+2 к очкам), `Зеленый блок`: увеличение змейки в 2 раза (x2 очков), `Фиолетовый блок`: изменение направление змейки (+2 к очкам).    

### Изменение настроек
* В конфигурационном файле `config.py` должны выставляться значения `WIDTH` и `HEIGHT`, делящиеся нацело на `BLOCK_SIZE ** 2`, скорость змейки `SNAKE_SPEED` может быть установлена любая.
*  `DEFAULT_FOOD_PROBABILITY` - вероятность появления обычной еды (+1 к очкам).
*  `DOUBLE_LENGTH_PROBABILITY` - вероятность появление еды, которая увеличивает змейку вдвое (x2 очков).
*  `BOOST_PROBABILITY` - вероятность появления ускоряющей еды (+1 к очкам).
*  `BOOST_COEFFICIENT` - коэффициент ускорения.
*  `REVERSE_PROBABILITY` - вероятность появления еды, которая изменяет направление движения змейки на противоположное.