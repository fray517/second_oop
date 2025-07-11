import hashlib
import uuid
import sys

class User():
    """
    Базовый класс, представляющий пользователя
    """
    users = []
    usernames = set()
    
    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        User.users.append(self)
        User.usernames.add(username)
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def check_password(stored_password_hash, provided_password):
        """
        Проверка пароля
        """
        return stored_password_hash == User.hash_password(provided_password)
    
    def get_details(self):
        return f"Клиент: {self.username}, Email: {self.email}"
    
class Customer(User):
    """
    Класс, представляющий клиента, наследующий класс User.
    """
    def __init__(self, username, email, password_hash, address):
        super().__init__(username, email, password_hash)
        self.address = address

    def get_details(self):
        return f"Клиент: {self.username}, Email: {self.email}, Адрес: {self.address}"

class Admin(User):
    """
    Класс, представляющий администратора, наследующий класс User.
    """
    def __init__(self, username, email, password_hash, admin_level):
        super().__init__(username, email, password_hash)
        self.admin_level = admin_level

    def get_details(self):
        return f"Admin: {self.username}, Email: {self.email}, Admin-Level: {self.admin_level}"
    
    @staticmethod
    def list_users():
        """
        Выводит список всех пользователей.
        """
        for user in User.users:
            print(user.get_details())
    
    @staticmethod
    def delete_user(username):
        """
        Удаляет пользователя по username
        """
        user_to_delete = None
        for user in User.users:
            if user.username == username:
                user_to_delete = user
                break
        if user_to_delete:
            User.users.remove(user_to_delete)
            User.usernames.remove(username)
            print(f"Пользователь {username} удалён.")
        else:
            print(f"Пользователь {username} не найден.")

class AuthentificationService:
    """
    Сервис для управления регистрацией и аутентификацией пользователей.
    """
    def __init__(self):
        self.current_user = None

    def register(self, user_class, username, email, password, address=None, admin_level=None):
        """
        Регистрация нового пользователя с проверкой уникальности имени.
        """
        if username in User.usernames:
            print("Пользователь с таким именем уже существует!")
            return None
        password_hash = User.hash_password(password)
        if user_class == 5:
            print("Вы зарегистрировались как администратор")
            admin = Admin(username=username, email=email, password_hash=password_hash, admin_level=admin_level or 5)
            return admin
        else:
            customer = Customer(username=username, email=email, password_hash=password_hash, address=address)
            print("Пользователь зарегистрирован как клиент.")
            return customer

    def login(self, username, password):
        """
        Аутентификация пользователя.
        """
        for user in User.users:
            if user.username == username:
                if User.check_password(user.password_hash, password):
                    self.current_user = user
                    print(f"Пользователь {username} успешно вошёл в систему.")
                    return user
                else:
                    print("Неверный пароль!")
                    return None
        print("Пользователь не найден!")
        return None

    def logout(self):
        """
        Выход пользователя из системы
        """
        if self.current_user:
            print(f"Пользователь {self.current_user.username} вышел из системы.")
            self.current_user = None
        else:
            print("Нет активной сессии.")

    def get_current_user(self):
        """
        Возвращает текущего вошедшего пользователя.
        """
        return self.current_user

    def admin_actions(self):
        """
        Доступные действия для администратора
        """
        if not isinstance(self.current_user, Admin):
            print("Только администратор может выполнять эти действия!")
            return
        while True:
            action = input("Введите действие: 1 - Показать пользователей, 2 - Удалить пользователя, 3 - Выйти: ")
            if action == '1':
                Admin.list_users()
            elif action == '2':
                username = input("Введите имя пользователя для удаления: ")
                if username == self.current_user.username:
                    print("Нельзя удалить самого себя!")
                else:
                    Admin.delete_user(username)
            elif action == '3':
                break
            else:
                print("Неизвестное действие!")

# Пример использования:
if __name__ == "__main__":
    auth_service = AuthentificationService()
    while True:
        mode = input("1 - Регистрация, 2 - Вход, 3 - Выход: ")
        if mode == '1':
            user_class = int(input("Введите уровень допуска (5 - админ, иначе клиент): "))
            username = input("Имя пользователя: ")
            email = input("Email: ")
            password = input("Пароль: ")
            if user_class == 5:
                admin_level = int(input("Уровень админа (по умолчанию 5): ") or 5)
                auth_service.register(user_class=5, username=username, email=email, password=password, admin_level=admin_level)
            else:
                address = input("Адрес: ")
                auth_service.register(user_class=user_class, username=username, email=email, password=password, address=address)
        elif mode == '2':
            username = input("Имя пользователя: ")
            password = input("Пароль: ")
            user = auth_service.login(username, password)
            if isinstance(user, Admin):
                auth_service.admin_actions()
        elif mode == '3':
            auth_service.logout()
            sys.exit()
        else:
            print("Неизвестный режим!")

print("Работа завершена.")
sys.exit()
            