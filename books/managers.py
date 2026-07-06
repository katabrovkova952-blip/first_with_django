from django.db import models


class BookQuerySet(models.QuerySet):

    def for_user(self, user):
        return self.filter(user=user)