from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):

    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        response = self.client.get('/inscricao/')
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_fomr.html"""
        response = self.client.get('/inscricao/')
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Must contain input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp,'<input', 6)
        self.assertContains(self.resp, 'type="text"',3)
        self.assertContains(self.resp, 'type="email"',1)
        self.assertContains(self.resp, 'type="submit"',1)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Contex must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Mateus Flavio', cpf='32783355892', email='mateusflavio@gmail.com', phone='(16) 992636600')
        self.resp = self.client.post('/inscricao/', data)


    def test_ppost(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscrible_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, email.subject)

    def test_subscrible_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, email.from_email)

    def test_subscrible_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br','mateusflavio@gmail.com']

        self.assertEqual(expect, email.to)

    def test_subscrible_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Mateus Flavio', email.body)
        self.assertIn('32783355892', email.body)
        self.assertIn('mateusflavio@gmail.com', email.body)
        self.assertIn('(16) 992636600', email.body)



class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_has_form_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class SubscribeSuccessMessage(TestCase):

    def test_message(self):
        data = dict(name='Mateus Flavio', cpf='32783355892', email='mateusflavio@gmail.com', phone='(16) 992636600')
        response = self.client.post('/inscricao/', data, follow=True)

        self.assertContains(response, 'Inscrição realizada com sucesso!')
