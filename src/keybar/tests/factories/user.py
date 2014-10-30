import factory
from django.contrib.auth.hashers import make_password

from keybar.models.user import User


class UserFactory(factory.DjangoModelFactory):
    email = factory.Sequence(lambda i: '{0}@none.none'.format(i))
    is_active = True

    class Meta:
        model = User

    @classmethod
    def _prepare(cls, create, **kwargs):
        raw_password = kwargs.pop('raw_password', 'secret')
        if not 'password' in kwargs:
            kwargs['password'] = make_password(raw_password, hasher='md5')
        return super(UserFactory, cls)._prepare(create, **kwargs)
