import markdown2
import bleach

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models import db, Recipe, Review
from app.forms import ReviewForm

review_bp = Blueprint('review', __name__)

def sanitize(text):
    allowed_tags = set(bleach.sanitizer.ALLOWED_TAGS).union({'p', 'br', 'ul', 'li', 'strong', 'em'})
    return bleach.clean(markdown2.markdown(text), tags=allowed_tags)


@review_bp.route('/recipe/<int:recipe_id>/review', methods=['GET', 'POST'])
@login_required
def create(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    # Проверка: не написал ли пользователь уже отзыв
    existing_review = Review.query.filter_by(recipe_id=recipe.id, user_id=current_user.id).first()
    if existing_review:
        flash('Вы уже оставили отзыв на этот рецепт.', 'warning')
        return redirect(url_for('recipe.view', recipe_id=recipe.id))

    form = ReviewForm()
    if form.validate_on_submit():
        try:
            review = Review(
                recipe_id=recipe.id,
                user_id=current_user.id,
                rating=form.rating.data,
                text=sanitize(form.text.data)
            )
            db.session.add(review)
            db.session.commit()
            flash('Отзыв успешно добавлен!', 'success')
            return redirect(url_for('recipe.view', recipe_id=recipe.id))
        except Exception:
            db.session.rollback()
            flash('Произошла ошибка при добавлении отзыва.', 'danger')
    return render_template('review/create.html', form=form, recipe=recipe)
