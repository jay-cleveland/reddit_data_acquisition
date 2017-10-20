#Script for formatting text
import os, sys, re, string, nltk, enchant
from nltk.corpus import stopwords


def main():

	sub_list = []
	with open("subreddits.txt") as subreddits:
		for subreddit in subreddits:
			sub_list.append(subreddit.rstrip())

	onlyAlphabet = re.compile(r'[^a-z\l+ \']')
	stop = set(stopwords.words('english'))
	d = enchant.Dict("en_US")
	foul_language = []

	with open("foul_language.txt") as words:
		for word in words:
			foul_language.append(word.rstrip())


	def cleanDoc(doc):
		stop_free = " ".join([i for i in doc.lower().split() if i not in stop and i not in foul_language and d.check(i)])
		punc_free = onlyAlphabet.sub('', stop_free)
		return punc_free


	for sub in sub_list:
		txtlist_filename = sub + "_textfiles.txt"
		txtlist_path = "/home/kaislyn/RedditData/subreddits/%s/raw_text/" % sub			#Change path in this line
		txtlist_filepath = os.path.join(txtlist_path, txtlist_filename)
		
		originTextPath = "/home/kaislyn/RedditData/subreddits/%s/raw_text/" % sub		#Change path in this line
		processedTextPath = "/home/kaislyn/RedditData/subreddits/%s/processed_text/" % sub	#Change path in this line


		if not os.path.exists(processedTextPath):
			os.makedirs(processedTextPath)
	
		with open(txtlist_filepath) as posts:
			for post in posts:
				docs = []

				postPath = os.path.join(originTextPath, post.rstrip())
				newPath = os.path.join(processedTextPath, post.rstrip())
				
				with open(postPath) as txtfile:
					for line in txtfile:
						docs.append(line.rstrip())

				nfile = open(newPath, "w+")
				for doc in docs:
					if len(cleanDoc(doc)) > 1:
						nfile.write(cleanDoc(doc) + "\n")
				nfile.close()
				
				
	



main()
