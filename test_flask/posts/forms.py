from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Текст поста', validators=[DataRequired()])
    submit = SubmitField('Отправить')
    picture = FileField('Приложите фото к посту',
                        validators=[FileAllowed(['jpg', 'png'])])


class CommentForm(FlaskForm):
    comment = StringField('Комментарий', validators=[DataRequired()])
