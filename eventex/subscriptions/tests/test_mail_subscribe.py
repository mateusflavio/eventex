from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):

    def setUp(self):
        data = dict(name='Mateus Flavio', cpf='32783355892', email='mateusflavio@gmail.com', phone='(16) 992636600')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscrible_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscrible_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscrible_email_to(self):
        expect = ['contato@eventex.com.br','mateusflavio@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscrible_email_body(self):
        contents = [
            'Mateus Flavio',
            '32783355892',
            'mateusflavio@gmail.com',
            '(16) 992636600'
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
