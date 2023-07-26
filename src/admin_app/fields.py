

from typing import Any
from markdown import markdown
from markupsafe import Markup
from starlette.requests import Request
from starlette_admin import RequestAction, TextAreaField, StringField

from admin_app.models import User


class MarkdownField(TextAreaField):

    async def serialize_value(
        self, request: Request, value: Any, action: RequestAction
    ) -> Any:
        if action == RequestAction.DETAIL:
            return markdown(Markup.escape(value))
        return await super().serialize_value(request, value, action)

class CommentCounterField(StringField):
    async def parse_obj(self, request: Request, obj: Any) -> Any:
        assert isinstance(obj, User)
        return len(obj.comments)