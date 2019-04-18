# based on https://www.revsys.com/tidbits/keeping-django-model-objects-ordered/
from django.db import models, transaction
from django.db.models import F, Max
from django.contrib.auth.models import User

class NoteManager(models.Manager):
    """ Manager to encapsulate bits of business logic """

    def reorder_by(self, field):
        users = User.objects.all()
        for user in users:
            qs = self.get_queryset().filter(owner=user).order_by(field)
            for index, note in enumerate(qs):
                note.order = index + 1
                note.save()

    def move(self, obj, new_order):
        """ Move an object to a new order position """

        qs = self.get_queryset()

        with transaction.atomic():
            if obj.order > int(new_order):
                qs.filter(
                    order__lt=obj.order,
                    order__gte=new_order,
                ).exclude(
                    pk=obj.pk
                ).update(
                    order=F('order') + 1,
                )
            else:
                qs.filter(
                    order__lte=new_order,
                    order__gt=obj.order,
                ).exclude(
                    pk=obj.pk,
                ).update(
                    order=F('order') - 1,
                )

            obj.order = new_order
            obj.save()

    def create(self, **kwargs):
        instance = self.model(**kwargs)

        with transaction.atomic():
            # Get our current max order number
            results = self.filter(owner=kwargs['owner']).aggregate(Max('order'))

            # Increment and use it for our new object
            current_order = results['order__max'] + 1
            if current_order is None:
                current_order = 0

            value = current_order + 1
            instance.order = value
            instance.save()

            return instance