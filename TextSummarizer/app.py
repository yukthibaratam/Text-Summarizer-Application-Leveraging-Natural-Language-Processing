from flask import Flask, url_for, render_template, request
from spacy_summarization import text_summarizer
from nltk_summarization import nltk_summarizer
import spacy 
#from gensim.summarization import summarize
import nltk
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
nltk.download('stopwords')
nltk.download('punkt')

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
#Home[2]
#Compare[2]
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def sumy_summary(docx):
	parser = PlaintextParser.from_string(docx, Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document, 3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result


def readingTime(mytext):
	total_words = len([token.text for token in nlp(mytext)])
	extimated_time = total_words/200.0
	return extimated_time


def get_text(url):
	 page= urlopen(url)
	 soup = BeautifulSoup(page,"lxml")
	 fetched_text = ' '.join(map(lambda p:p.text.soup.find_all('p')))
	 return fetched_text


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/analyze', methods=['GET','POST'])
def analyze():
	start = time.time()
	if request.method =='POST':
		rawtext = request.form['rawtext']
		final_reading_time= readingTime(rawtext)
		#Summarizaton
		final_summary= text_summarizer(rawtext)
		#ReadingTime
		final_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html', final_summary= final_summary, final_time=final_time, final_reading_time=final_reading_time)

@app.route('/analyze_url', methods=['GET','POST'])
def analyze_url():
	start = time.time()
	if request.method =='POST':
		raw_url= request.form['raw_url']
		raw_text = get_text(raw_url)
		final_reading_time= readingTime(raw_text)
		#Summarizaton
		final_summary= text_summarizer(raw_text)
		#ReadingTime
		final_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html', final_summary= final_summary, final_time=final_time, final_reading_time=final_reading_time)

@app.route('/compare_summary')
def compare_summary():
	return render_template('compare_summary.html')

@app.route('/comparer', methods=['GET','POST'])
def comparer():
	rawtext = final_summary_spacy = final_summary_nltk = ""
	final_time = final_reading_time = summary_reading_time = 0
	final_summary_sumy = summary_reading_time_sumy = summary_reading_time_nltk = 0
	start = time.time()
	if request.method =='POST':
		rawtext = request.form['rawtext']
		final_reading_time= readingTime(rawtext)
		#Summarizaton
		final_summary_spacy= text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary_spacy)
		# Summary for gensim
		#final_summary_gensim = summarize(rawtext)
		#summary_reading_time_gensim = readingTime(final_summary_gensim)

		# Summary for nltk
		final_summary_nltk = nltk_summarizer(rawtext)
		summary_reading_time_nltk = readingTime(final_summary_nltk)

		# Summary for sumy
		final_summary_sumy = sumy_summary(rawtext)
		summary_reading_time_sumy = readingTime(final_summary_sumy)

		end = time.time()
		final_time = end-start

	# Reading
	return render_template('compare_summary.html', ctext=rawtext, final_summary_spacy=final_summary_spacy,final_summary_nltk=final_summary_nltk,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,final_summary_sumy=final_summary_sumy,summary_reading_time_sumy=summary_reading_time_sumy,summary_reading_time_nltk=summary_reading_time_nltk)

@app.route('/about')
def about():
	return render_template('index.html')



if __name__ == '__main__':
	app.run(debug= True)
