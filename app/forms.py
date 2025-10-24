from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms import IntegerField, TextAreaField, MultipleFileField, SelectField
from wtforms.validators import NumberRange

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество')
    submit = SubmitField('Зарегистрироваться')


class RecipeForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    cook_time = IntegerField('Время приготовления (в минутах)', validators=[DataRequired(), NumberRange(min=1)])
    portions = IntegerField('Количество порций', validators=[DataRequired(), NumberRange(min=1)])
    ingredients = TextAreaField('Ингредиенты', validators=[DataRequired()])
    steps = TextAreaField('Шаги приготовления', validators=[DataRequired()])
    images = MultipleFileField('Изображения', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Только изображения!')])
    submit = SubmitField('Сохранить')

class ReviewForm(FlaskForm):
    rating = SelectField('Оценка', choices=[
        (5, 'отлично'),
        (4, 'хорошо'),
        (3, 'удовлетворительно'),
        (2, 'неудовлетворительно'),
        (1, 'плохо'),
        (0, 'ужасно')
    ], coerce=int, default=5)
    text = TextAreaField('Текст отзыва', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
