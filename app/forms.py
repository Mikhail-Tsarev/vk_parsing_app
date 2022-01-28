from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, SubmitField
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
    day = SelectField("День", choices=[i for i in range(1, 32)])
    month = SelectField("Месяц", choices=months)
    year = SelectField(
        "Год", choices=[i for i in range(current_year, 2005, -1)]
    )
    id = BooleanField("Id записи", default=True)
    text = BooleanField("Текст", default=True)
    attachments = BooleanField("Количество вложений", default=True)
    links = BooleanField("Ссылки на вложения", default=True)
    likes = BooleanField("Количество лайков", default=True)
    reposts = BooleanField("Количество репостов", default=True)
    comments = BooleanField("Количество комментариев", default=True)
    submit = SubmitField("Запросить")


class GetCsv(FlaskForm):

    submit = SubmitField("Скачать данные в .csv")
