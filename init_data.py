from app import create_app
from app.models import db, User, Role

def create_roles_and_users():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Создание ролей
        admin_role = Role(name='администратор', description='Суперпользователь')
        user_role = Role(name='пользователь', description='Обычный пользователь')
        db.session.add_all([admin_role, user_role])
        db.session.commit()

        # Создание пользователей
        users = [
            User(login='admin', last_name='Иванов', first_name='Админ', role_id=admin_role.id),
            User(login='user1', last_name='Петров', first_name='Алексей', role_id=user_role.id),
            User(login='user2', last_name='Сидорова', first_name='Мария', role_id=user_role.id),
            User(login='user3', last_name='Козлов', first_name='Игорь', role_id=user_role.id),
            User(login='user4', last_name='Орлова', first_name='Екатерина', role_id=user_role.id),
        ]

        for u in users:
            u.set_password('password123')  # пароль одинаковый для всех: password123
            db.session.add(u)

        db.session.commit()
        print("Пользователи и роли успешно добавлены.")

if __name__ == '__main__':
    create_roles_and_users()
