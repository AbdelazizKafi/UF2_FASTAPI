def user_schema(user) -> dict:
    return {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "age": user[3],

    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]
