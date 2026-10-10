from django.shortcuts import render
from requests.exceptions import RequestException
from translate import Translator
from translate.exceptions import TranslationError

LANGUAGES = {"hi": "Hindi", "mr": "Marathi", "de": "German"}

def home(request):
    context = {"text": "", "language": "", "translation": "", "error": ""}

    if request.method == "POST":
        text = request.POST.get("translate", "").strip()
        language = request.POST.get("language", "")
        context.update({"text": text, "language": language})

        if not text:
            context["error"] = "Please enter text to translate."
        elif language not in LANGUAGES:
            context["error"] = "Please choose a supported language."
        else:
            try:
                context["translation"] = Translator(to_lang=language).translate(text)
            except (RequestException, TranslationError, RuntimeError):
                context["error"] = "The translation service could not return a result. Check your connection and try again."

    return render(request, "main/index.html", context)
