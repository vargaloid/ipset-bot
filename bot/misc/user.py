import json


users_file = 'users.json'


def get_users_ids():
    with open(users_file, 'r') as file:
        users = json.load(file)
    users_list = [int(id) for id in users.keys()]
    return users_list


def get_users():
    with open(users_file, 'r') as file:
        users = json.load(file)
    return users


def add_user(message):
    users_list = get_users_ids()
    if message.forward_from.id in users_list:
        return False
    else:
        name = ' '.join(filter(None, (message.forward_from.first_name, message.forward_from.last_name)))
        data = {message.forward_from.id: name}
        file_data = get_users()
        file_data.update(data)
        with open(users_file, 'w') as file:
            json.dump(file_data, file)
        return True


def del_user(user_id):
    users_list = get_users_ids()
    if int(user_id) in users_list:
        file_data = get_users()
        file_data.pop(user_id)
        with open(users_file, 'w') as file:
            json.dump(file_data, file)
        return True
    else:
        return None
