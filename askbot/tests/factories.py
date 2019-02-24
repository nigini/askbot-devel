from builtins import object
import factory
from django.conf import settings


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')

    class Meta(object):
        model = settings.AUTH_USER_MODEL


class TagFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('word')
    created_by = factory.SubFactory(UserFactory)

    class Meta(object):
        model = 'askbot.Tag'


class PostFactory(factory.django.DjangoModelFactory):
    text = factory.Faker('paragraph')
    author = factory.SubFactory(UserFactory)

    class Meta(object):
        model = 'askbot.Post'


class QuestionFactory(PostFactory):
    post_type = 'question'


class AnswerFactory(PostFactory):
    post_type = 'answer'


class ThreadFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence')
    text = factory.Faker('paragraph', nb_sentences=10)
    author = factory.SubFactory(UserFactory)

    tagnames = factory.Faker('word')
    language = factory.Faker('language_code')

    added_at = factory.Faker('date_time')
    wiki = factory.Faker('boolean')

    class Meta(object):
        model = 'askbot.Thread'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        instance = manager.create_new(*args, **kwargs)
        return instance


class MessageFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    message = factory.Faker('paragraph')

    class Meta(object):
        model = 'askbot.Message'


class GroupFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('company')
    description = factory.SubFactory(PostFactory)

    class Meta(object):
        model = 'askbot.Group'


class GroupMembershipFactory(factory.django.DjangoModelFactory):
    group = factory.SubFactory(GroupFactory)
    user = factory.SubFactory(UserFactory)

    class Meta(object):
        model = 'askbot.GroupMembership'


class BulkTagSubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = 'askbot.BulkTagSubscription'


class EmailFeedSettingFactory(factory.django.DjangoModelFactory):
    subscriber = factory.SubFactory(UserFactory)

    class Meta(object):
        model = 'askbot.EmailFeedSetting'
