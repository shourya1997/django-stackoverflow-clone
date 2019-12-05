from unittest.mock import patch

import factory

from qanda.models import Question
from user.factories import UserFactory

class QuestionFactory(factory.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Question #%d' % n)
    question = 'what is a question ?'
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Question

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        with patch('qanda.service.esearch.Elasticsearch'):
            return super()._create(model_class, *args, **kwargs)

    