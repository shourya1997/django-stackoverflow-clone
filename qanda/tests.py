from unittest.mock import patch
from datetime import date

from django.test import TestCase, RequestFactory
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from elasticsearch import Elasticsearch

from qanda.models import Question
from qanda.factories import QuestionFactory
from qanda.views import DailyQuestionList
from user.factories import UserFactory

# Create your tests here.

class QuestionSaveTestCase(TestCase):
    """
    Tests Question.save()
    """
    @patch('qanda.service.esearch.Elasticsearch')
    def test_elasticsearch_upsert_on_save(self, ElasticsearchMock):
        user = get_user_model().objects.create_user(
            username='unittest',
            password='unittest',
        )
        question_title = 'Unit Test'
        question_body  = 'some long text'
        q = Question(title=question_title,
                    question=question_body,
                    user=user,)
        q.save()

        self.assertIsNotNone(q.id)
        self.assertTrue(ElasticsearchMock.called)
        mock_client = ElasticsearchMock.return_value
        mock_client.update.assert_called_once_with(
            settings.ES_INDEX,
            'doc',
            id = q.id,
            body={
                'doc':{
                    'text':f'{question_title}\n{question_body}',
                    'question_body': question_body,
                    'title': question_title,
                    'id':q.id,
                    'created':q.created,
                    },
                'doc_as_upsert':True,
                }                
            )

class DailyQuestionListTestCase(TestCase):
    """
    Tests the DailyQuestionList view
    """

    QUESTION_LIST_NEEDLE_TEMPLATE = '''
        <a href="/q/{id}" >
        {title}
        </a>
    '''
    # print(QUESTION_LIST_NEEDLE_TEMPLATE)
    REQUEST = RequestFactory().get(path='/q/2030-12-31')
    TODAY = date.today()

    def test_GET_on_day_with_many_questions(self):
        today_questions = [QuestionFactory() for _ in range(10)]

        response = DailyQuestionList.as_view()(
                                                self.REQUEST,
                                                year=self.TODAY.year,
                                                month=self.TODAY.month,
                                                day=self.TODAY.day
                                                )

        self.assertEqual(200, response.status_code)
        self.assertEqual(10, response.context_data['object_list'].count())
        rendered_content = response.rendered_content
        for question in today_questions:
            needle = self.QUESTION_LIST_NEEDLE_TEMPLATE.format(
                # votes=question.votes,
                id=question.id,
                title=question.title,
                username=question.user.username,
            )
            self.assertInHTML(needle, rendered_content)

class QuestionDetailViewTestCase(TestCase):
    QUESTION_DISPLAY_SNIPPET = '''
    <div class="body col-sm-12 >
        <p>{body}</p>
    </div>    
    '''
    LOGIN_TO_POST_ANSWERS = '''<div> Login to post answers. </div>'''

    def test_logged_in_user_can_post_answer(self):
        question = QuestionFactory()
        self.assertTrue(self.client.login(
            username=question.user.username,
            password=UserFactory.password
        ))
        response = self.client.get('/q/{}'.format(question.id))
        rendered_content = response.rendered_content

        self.assertEqual(200, response.status_code)
        # self.assertInHTML(self.LOGIN_TO_POST_ANSWERS, rendered_content)

        template_names = [t.name for t in response.templates]

        self.assertIn('qanda/common/post_answer.html', template_names)

        question_needle = self.QUESTION_DISPLAY_SNIPPET.format(
            body=QuestionFactory.question,
        )
    
        # self.assertInHTML(question_needle, rendered_content)
