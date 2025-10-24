import os
import uuid
import markdown2
import bleach

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.models import db, Recipe, RecipeImage
from app.forms import RecipeForm

recipe_bp = Blueprint('recipe', __name__)

def sanitize(text):
    allowed_tags = set(bleach.sanitizer.ALLOWED_TAGS).union({'p', 'br', 'ul', 'li', 'strong', 'em'})
    return bleach.clean(markdown2.markdown(text), tags=allowed_tags)


@recipe_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', recipes=recipes)

@recipe_bp.route('/recipe/<int:recipe_id>')
def view(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe/view.html', recipe=recipe)

@recipe_bp.route('/recipe/create', methods=['GET', 'POST'])
@login_required
def create():
    form = RecipeForm()
    if form.validate_on_submit():
        try:
            recipe = Recipe(
                title=form.title.data,
                description=sanitize(form.description.data),
                cook_time=form.cook_time.data,
                portions=form.portions.data,
                ingredients=sanitize(form.ingredients.data),
                steps=sanitize(form.steps.data),
                author_id=current_user.id
            )
            db.session.add(recipe)
            db.session.flush()  # Получить ID рецепта до коммита

            upload_path = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_path, exist_ok=True)  # Создаём папку, если нет

            for img in form.images.data:
                if img:
                    filename = f"{uuid.uuid4().hex}_{secure_filename(img.filename)}"
                    filepath = os.path.join(upload_path, filename)
                    img.save(filepath)
                    db.session.add(RecipeImage(
                        filename=filename,
                        mimetype=img.mimetype,
                        recipe_id=recipe.id
                    ))

            db.session.commit()
            flash('Рецепт успешно добавлен!', 'success')
            return redirect(url_for('recipe.view', recipe_id=recipe.id))

        except Exception as e:
            db.session.rollback()
            print(f'[ERROR] Ошибка при создании рецепта: {e}')
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')

    return render_template('recipe/create.html', form=form)


@recipe_bp.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.author_id != current_user.id and current_user.role.name != 'администратор':
        flash('У вас недостаточно прав для выполнения данного действия.', 'warning')
        return redirect(url_for('recipe.index'))

    form = RecipeForm(obj=recipe)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            recipe.title = form.title.data
            recipe.description = sanitize(form.description.data)
            recipe.cook_time = form.cook_time.data
            recipe.portions = form.portions.data
            recipe.ingredients = sanitize(form.ingredients.data)
            recipe.steps = sanitize(form.steps.data)
            db.session.commit()
            flash('Рецепт успешно обновлён!', 'success')
            return redirect(url_for('recipe.view', recipe_id=recipe.id))
        except Exception:
            db.session.rollback()
            flash('Ошибка при сохранении изменений.', 'danger')
    return render_template('recipe/create.html', form=form)

@recipe_bp.route('/recipe/<int:recipe_id>/delete')
@login_required
def delete(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.author_id != current_user.id and current_user.role.name != 'администратор':
        flash('У вас недостаточно прав для выполнения данного действия.', 'warning')
        return redirect(url_for('recipe.index'))

    try:
        # Удалим изображения с диска
        for image in recipe.images:
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename)
            if os.path.exists(filepath):
                os.remove(filepath)

        db.session.delete(recipe)
        db.session.commit()
        flash(f'Рецепт «{recipe.title}» успешно удалён.', 'success')
    except Exception:
        db.session.rollback()
        flash('Ошибка при удалении рецепта.', 'danger')

    return redirect(url_for('recipe.index'))
