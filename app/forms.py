from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

current_year = datetime.today().year
months = [
    (1, "Января"),
    (2, "Февраля"),
    (3, "Марта"),
    (4, "Апреля"),
    (5, "Мая"),
    (6, "Июня"),
    (7, "Июля"),
    (8, "Августа"),
    (9, "Сентября"),
    (10, "Октября"),
    (11, "Ноября"),
    (12, "Декабря"),
]


class QueryForm(FlaskForm):
    link = StringField(
        "Ссылка на профиль или группу", validators=[DataRequired()]
    )
    day = SelectField("День", choices=[i for i in range(1, 31)])
    month = SelectField("Месяц", choices=months)
    year = SelectField(
        "Год", choices=[i for i in range(current_year, 2005, -1)]
    )
    submit = SubmitField("Отправить")
