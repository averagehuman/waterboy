from django.db import models
from django.db.models import signals
from django.core.exceptions import ImproperlyConfigured

from django.utils.translation import ugettext_lazy as _

try:
    from picklefield import PickledObjectField
except ImportError:
    raise ImproperlyConfigured("Couldn't find the the 3rd party app "
                               "django-picklefield which is required for "
                               "the felicity database backend.")


class Config(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = PickledObjectField()

    class Meta:
        verbose_name = _('felicity')
        verbose_name_plural = _('felicitys')
        db_table = 'felicity_config'

    def __unicode__(self):
        return self.key


def create_perm(app, created_models, verbosity, db, **kwargs):
    """
    Creates a fake content type and permission
    to be able to check for permissions
    """
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    if ContentType._meta.installed and Permission._meta.installed:
        content_type, created = ContentType.objects.get_or_create(
            name='config',
            app_label='felicity',
            model='config')

        permission, created = Permission.objects.get_or_create(
            name='Can change config',
            content_type=content_type,
            codename='change_config')


signals.post_syncdb.connect(create_perm, dispatch_uid="felicity.create_perm")
