# cookbook/ingredients/schema.py
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Note


# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class NoteNode(DjangoObjectType):
    class Meta:
        model = Note
        filter_fields = ['title', 'content', 'color', 'pinned']
        interfaces = (relay.Node, )


class Query(object):
    note = relay.Node.Field(NoteNode)
    all_notes = DjangoFilterConnectionField(NoteNode)