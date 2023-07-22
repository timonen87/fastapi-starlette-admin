# from typing import Any, Dict
#
# from jinja2 import Template
# from sqlalchemy import desc, func, select
# from sqlalchemy.orm import Session
# from starlette.requests import Request
# from starlette.responses import Response
# from starlette.templating import Jinja2Templates
# from starlette_admin import CustomView, EmailField, TagsField
# from starlette_admin.contrib.sqla import ModelView
# from starlette_admin.exceptions import FormValidationError
#
# from blog.fields import CommentCounterField
# from .models import User
#
#
# class UserView(ModelView):
#     page_size_options = [15, 10, 25, -1]
#     fields = [
#         "id",
#         "full_name",
#         EmailField("username"),
#         "avatar",
#         "posts",
#         CommentCounterField("comments_counter", label="Number of Comments"),
#         "comments",
#     ]
#
#     # Only show the counter on list view
#     exclude_fields_from_list = ["comments"]
#     exclude_fields_from_create = ["comments_counter"]
#     exclude_fields_from_edit = ["comments_counter"]
#     exclude_fields_from_detail = ["comments_counter"]
#     # Sort by full_name asc and username desc by default
#     fields_default_sort = ["full_name", (User.username, True)]
#
#     async def select2_selection(self, obj: Any, request: Request) -> str:
#         template_str = "<span>{{obj.full_name}}</span>"
#         return Template(template_str, autoescape=True).render(obj=obj)
#
#     def can_delete(self, request: Request) -> bool:
#         return False
#
