from groupy import Client
import os

client = Client.from_token(os.environ.get("GROUPME_API_TOKEN"))

def get_group(group_id):
    return client.groups.get(group_id)

def get_user_id_from_group(group_id, nickname):
    user_id = None
    group = get_group(group_id)
    for member in group.members:
        member_nickname = member.__getattr__("nickname")
        if member_nickname.lower() == nickname.lower():
            user_id = member.__getattr__("user_id")
    return user_id


