import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import calendar
from typing import List

# Класс для хранения пары символов (левый и правый)
class MarkerPair:
    def __init__(self, left_symbol=None, right_symbol=None):
        self.left_symbol = left_symbol  # Символ слева от числа
        self.right_symbol = right_symbol  # Символ справа от числа

# Класс для хранения атрибутов даты
class DateAttribute:
    def __init__(self, date:datetime.date, symbol:str=None, marker_pair:MarkerPair=None, is_disabled:bool=False, callback_data:str = None):
        self.date = date  # Дата
        self.symbol = symbol  # Символ для замены даты (один символ) 
        self.marker_pair = marker_pair  # Пара символов (левый и правый)
        self.is_disabled = is_disabled  # Заблокирована ли дата
        self.callback_data = callback_data # callback_data

# Класс для создания кнопок календаря
class CalendarButtonMaker:
    def __init__(self, out_of_range_text:str, empty_day_text:str, callback_data_out_of_range_and_disable:str, callback_data_default_prefix:str):
        self.out_of_range_text = out_of_range_text  # Текст для дат вне диапазона
        self.empty_day_text = empty_day_text  # Текст для пустых дней
        self.callback_data_default_prefix = callback_data_default_prefix #префикс для нажатия на допустимую дату
        self.callback_data_out_of_range_and_disable = callback_data_out_of_range_and_disable

    def _generate_marker_pair_text(self, symbol: str|int, marker_pair: MarkerPair)->str:
        """Генерация текста для пары символов."""
        left = marker_pair.left_symbol or ""
        right = marker_pair.right_symbol or ""
        return f"{left}{symbol}{right}"

    def _generate_text(self, day:int, date_attribute: DateAttribute)->str:
        if date_attribute:
            if date_attribute.symbol and date_attribute.marker_pair is None:
                return date_attribute.symbol
            elif date_attribute.marker_pair and date_attribute.symbol is None:
                return self._generate_marker_pair_text(day, date_attribute.marker_pair)
            elif date_attribute.marker_pair and date_attribute.symbol:
                return self._generate_marker_pair_text(date_attribute.symbol, date_attribute.marker_pair)
        return str(day)

    def _generate_button_text(self, day:int, date_attribute:DateAttribute, is_in_range: bool):
        """Генерация текста для кнопки на основе атрибутов даты."""
        if day == 0:
            return self.empty_day_text
        
        if not is_in_range:
            return self.out_of_range_text
    
        return self._generate_text(day, date_attribute)
    
    def _get_callback_date(self, date:datetime.date, date_attribute:DateAttribute, is_in_range:bool):
        if not is_in_range:
            return self.callback_data_out_of_range_and_disable
        
        if date_attribute:
            if date_attribute.is_disabled:
                return self.callback_data_out_of_range_and_disable
            if date_attribute.callback_data:
                return date_attribute.callback_data

        return self.callback_data_default_prefix(date)

    def create_button(self, day:int, date:datetime.date, date_attribute:DateAttribute=None, is_in_range:bool=True):
        return InlineKeyboardButton(text = self._generate_button_text(day, date_attribute, is_in_range), 
                                    callback_data=self._get_callback_date(date, date_attribute, is_in_range))

# Класс для работы с календарем
class Calendar:
    def __init__(self, min_date:datetime.date, max_date:datetime.date, callback_data_default_prefix:str, callback_data_next:str, callback_data_prev:str, date_attributes:List[DateAttribute]=[], callback_data_out_of_range_and_disable:str="0", out_of_range_text:str="❌", empty_day_text:str=" ", additional_btns=[]):
        self.min_date = min_date  # Минимальная допустимая дата
        self.max_date = max_date  # Максимальная допустимая дата
        self.date_attributes = date_attributes  # Список объектов DateAttribute
        self.out_of_range_text = out_of_range_text
        self.empty_day_text = empty_day_text
        self.callback_data_out_of_range_and_disable = callback_data_out_of_range_and_disable
        self.callback_data_default_prefix = callback_data_default_prefix
        self.callback_data_next = callback_data_next
        self.callback_data_prev = callback_data_prev
        self.additional_btns = additional_btns
        self.month_name = ["Декабрь","Январь","Февраль","Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь","Январь"]


    def is_date_in_range(self, date):
        """Проверка, находится ли дата в допустимом диапазоне."""
        return self.min_date <= date <= self.max_date

    def get_date_attribute(self, date):
        """Получить атрибуты для конкретной даты."""
        for attribute in self.date_attributes:
            if attribute.date == date:
                return attribute
        return None

    def create_navigation_buttons(self, year, month):
        """Создать кнопки для переключения месяцев."""
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1

        # Проверка, можно ли переключиться на предыдущий месяц
        prev_date = datetime.date(prev_year, prev_month, calendar.monthrange(prev_year, prev_month)[1])
        prev_button = InlineKeyboardButton(f"<< {self.month_name[prev_month]}", callback_data=self.callback_data_prev(prev_year, prev_month))
        if not self.is_date_in_range(prev_date):
            prev_button = InlineKeyboardButton(" ", callback_data="0")

        # Проверка, можно ли переключиться на следующий месяц
        next_date = datetime.date(next_year, next_month, 1)
        next_button = InlineKeyboardButton(f"{self.month_name[next_month]} >>", callback_data=self.callback_data_next(next_year, next_month))
        if not self.is_date_in_range(next_date):
            next_button = InlineKeyboardButton(" ", callback_data="0")

        list_btn = [prev_button]
        list_btn.extend(self.additional_btns)
        list_btn.append(next_button)

        return list_btn

    def create_calendar_buttons(self, year, month):
        """Создание кнопок для календаря."""
        keyboard = []

        # Заголовок с названием месяца и года
        month_name = self.month_name[month]
        header = f"{month_name} {year}"
        keyboard.append([InlineKeyboardButton(header, callback_data="0")])

        # Дни недели
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        keyboard.append([InlineKeyboardButton(day, callback_data="0") for day in days])

        # Ячейки календаря
        cal = calendar.Calendar()
        calendar_button_maker = CalendarButtonMaker(out_of_range_text=self.out_of_range_text,
                                                     empty_day_text=self.empty_day_text, 
                                                     callback_data_default_prefix=self.callback_data_default_prefix,
                                                     callback_data_out_of_range_and_disable=self.callback_data_out_of_range_and_disable)
        
        for week in cal.monthdays2calendar(year, month):
            row = []
            for day, weekday in week:
                current_date = datetime.date(year, month, day) if day != 0 else None
                date_attribute = self.get_date_attribute(current_date) if current_date else None
                is_in_range = self.is_date_in_range(current_date) if current_date else False

                button = calendar_button_maker.create_button(
                    day=day,
                    date= current_date,
                    date_attribute=date_attribute,
                    is_in_range=is_in_range
                )
                row.append(button)
            keyboard.append(row)

        # Добавляем кнопки переключения месяцев
        keyboard.append(self.create_navigation_buttons(year, month))

        return InlineKeyboardMarkup(keyboard)

