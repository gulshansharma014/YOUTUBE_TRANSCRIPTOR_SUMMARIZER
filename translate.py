from googletrans import Translator

def g_translate(text, lang):

    translator = Translator()

    translated_text = translator.translate(text, src='en', dest=lang)
    translated_text = translated_text.text
    return translated_text