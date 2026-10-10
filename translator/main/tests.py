from unittest.mock import patch

from django.test import TestCase


class HomeViewTests(TestCase):
	@patch("main.views.Translator")
	def test_post_displays_translation_using_language_code(self, translator_class):
		translator_class.return_value.translate.return_value = "नमस्ते"

		response = self.client.post("/", {"translate": "Hello", "language": "hi"})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "नमस्ते")
		translator_class.assert_called_once_with(to_lang="hi")

	@patch("main.views.Translator")
	def test_translation_failure_displays_message(self, translator_class):
		translator_class.return_value.translate.side_effect = RuntimeError

		response = self.client.post("/", {"translate": "Hello", "language": "hi"})

		self.assertContains(response, "The translation service could not return a result.")
		translator_class.return_value.translate.assert_called_once_with("Hello")
