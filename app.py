
from flask import Flask,render_template,url_for,request
from langdetect import detect
import pandas as pd
import re
import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language
import en_core_web_sm
import es_core_news_md


app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@Language.factory("language_detector")
def get_lang_detector(nlp, name):
	return LanguageDetector()

@app.route('/process',methods=["POST"])
def process():
	if request.method == 'POST':
		choice = request.form['taskoption']
		rawtext = request.form['rawtext']

		if detect(rawtext) == 'en':
			nlp = spacy.load('en_core_web_sm')
		elif detect(rawtext) == 'es':
			nlp = spacy.load('es_core_news_md')
		else:
			return render_template("index.html",results=['No se ha introducido texto en el idioma correcto.'], num_of_results='0')

		doc = nlp(rawtext)
		d = []
		for ent in doc.ents:
			d.append((ent.label_, ent.text))
			df = pd.DataFrame(d, columns=('named entity', 'output'))
			ORG_named_entity = df.loc[df['named entity'] == 'ORG']['output']
			PERSON_named_entity = df.loc[df['named entity'] == 'PERSON']['output']
			MISC_named_entity = df.loc[df['named entity'] == 'MISC']['output']
			MONEY_named_entity = df.loc[df['named entity'] == 'MONEY']['output']
			LOC_named_entity = df.loc[df['named entity'] == 'LOC']['output']

		if choice == 'organization':
			results = ORG_named_entity
			num_of_results = len(results)
		elif choice == 'person':
			results = PERSON_named_entity
			num_of_results = len(results)
		elif choice == 'miscelanea':
			results = MISC_named_entity
			num_of_results = len(results)
		elif choice == 'money':
			results = MONEY_named_entity
			num_of_results = len(results)
		elif choice == 'location':
			results = LOC_named_entity
			num_of_results = len(results)
		
	return render_template("index.html",results=results, num_of_results=num_of_results)


if __name__ == '__main__':
	app.run(debug=True)