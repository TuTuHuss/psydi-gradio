import googletrans
translator = googletrans.Translator()

question = 'i dont know'
question_shown = translator.translate(question, src='en', dest='zh-tw').text + '\n'
print(question_shown)