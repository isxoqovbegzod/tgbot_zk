from users.models import User, Category, Product


def get_user(chat_id):
    users = User.objects.filter(chat_id=chat_id)
    if not users.exists():
        return None
    return users.first()


def get_user_product(chat_id):
    users = Product.objects.create(chat_id)
    if not users.exists():
        return None
    return users.first()


def create_user(chat_id):
    User.objects.create(chat_id=chat_id)


def ask_user_language(user, lang):
    user.lang = lang
    user.save()


def ask_user_contact(user, phone_num):
    user.contact_number = phone_num[1:]
    user.save()



