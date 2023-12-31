import json
from typing import Any, Dict, List
from sqlalchemy_file import File
from sqlalchemy_file.storage import StorageManager
from helpers import get_assets

# from models import Post, User, Comment
from models.user import User
from models.post import Post
from models.comment import Comment
from core.base import Base
from core.database import engine, Session


def read_users(data: List[Dict[str, Any]]) -> List[User]:
    return [
        User(
            **value,
            avatar=File(open(get_assets(f"images/avatar{(i % 5) + 1}.jpg"), "rb")),
        )
        for (i, value) in enumerate(data)
    ]


def read_posts(data: List[Dict[str, Any]]) -> List[Post]:
    return [Post(**value, content=DUMMY_POST) for value in data]


def read_comments(data: List[Dict[str, Any]]) -> List[Comment]:
    return [Comment(**value) for value in data]


def clear_storage():
    container = StorageManager.get("user-avatar")
    for obj in container.list_objects():
        obj.delete()


async def fill_database():
    # clear_storage()
    # url = str(DATABASE_URL)
    # engine = create_engine(url)
    # # create_database(url)  # Create the test database.
    Base.metadata.create_all(engine)
    # print(engine)
    data = json.load(open(get_assets("seed/blog.json")))
    # print(data)
    with Session() as session:
        session.add_all((read_users(data["users"])))
        session.add_all(read_posts(data["posts"]))
        session.add_all(read_comments(data["comments"]))
        session.commit()


DUMMY_POST = """
Lorem ipsum dolor sit amet consectetur adipisicing elit, sed do eiusmod tempor
incididunt ut labore et **dolore magna aliqua**: Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
deserunt mollit anim id est laborum.

  * Ut enim ad minim veniam
  * Quis nostrud exercitation *ullamco laboris*
  * Nisi ut aliquip ex ea commodo consequat

Praesent id fermentum lorem. Ut est lorem, fringilla at accumsan nec, euismod at
nunc. Aenean mattis sollicitudin mattis. Nullam pulvinar vestibulum bibendum.
Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos
himenaeos. Fusce nulla purus, gravida ac interdum ut, blandit eget ex. Duis a
luctus dolor.

Integer auctor massa maximus nulla scelerisque accumsan. *Aliquam ac malesuada*
ex. Pellentesque tortor magna, vulputate eu vulputate ut, venenatis ac lectus.
Praesent ut lacinia sem. Mauris a lectus eget felis mollis feugiat. Quisque
efficitur, mi ut semper pulvinar, urna urna blandit massa, eget tincidunt augue
nulla vitae est.

Ut posuere aliquet tincidunt. Aliquam erat volutpat. **Class aptent taciti**
sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Morbi
arcu orci, gravida eget aliquam eu, suscipit et ante. Morbi vulputate metus vel
ipsum finibus, ut dapibus massa feugiat. Vestibulum vel lobortis libero. Sed
tincidunt tellus et viverra scelerisque. Pellentesque tincidunt cursus felis.
Sed in egestas erat.

"""
