#Reddit Data Acquisition
#Author: Jaycee Cleveland

import praw, urllib, os, string, time
from PIL import Image


def main():
	#**10/12/2017** implement read in subreddit list (done)
	##25-30 subreddits

	#Keeps track of program runtime
	START_TIME = time.time()	

	#Reads in a list of subreddits to process
	subs = []
	with open("subreddits.txt") as subreddits:
		for subreddit in subreddits:
			subs.append(subreddit.rstrip())
	#Post limit
	post_limit = 10000
	totalPosts = 0

	for sub in subs:

		sub_path = "/home/kaislyn/RedditData/subreddits/%s/" % sub	
		if not os.path.exists(sub_path):

			#Create paths if they don't exist
			raw_text_path = "/home/kaislyn/RedditData/subreddits/%s/raw_text/" % sub 	#Change directory in this line
			image_path = "/home/kaislyn/RedditData/subreddits/%s/images/" % sub		#Change directory in this line

			if not os.path.exists(raw_text_path):
				os.makedirs(raw_text_path)
				
			if not os.path.exists(image_path):
				os.makedirs(image_path)

			#Create reddit instance
			reddit = praw.Reddit(user_agent="Comment Extraction (by /u/kaislyn89)", 
					client_id='gRwn8nhDjwyriA', client_secret='GCsKnHzzNFEpF5DZ1cBnnBzA8EI')

			#Lists
			posts = []
			txtfiles = []

			#Gets list of post ids from subreddit
			subreddit = reddit.subreddit(sub)
			for submission in subreddit.top(limit=post_limit):
				posts.append(submission.id)

						
			for post in posts:
				#Creates the submission object using the post id		
				submission = reddit.submission(id=post)
				
				#Only works on posts that have an image url associated with them
				if (".jpg" in submission.url) or (".png" in submission.url) or (".bmp" in submission.url):
					
					try:
						#Create text filepath
						text_filepath = os.path.join(raw_text_path, (post + '.txt'))
						
						#Create comment queue
						submission.comments.replace_more(limit=10000)
						comment_queue = submission.comments[:]
						
						
						if (len(comment_queue) >= 5):
							print("Aquiring post id %s from %s." % (post, sub))	
						
							#Grabs image from post
							
							#**10/17/17** Fixed bug for downloading corrupt images
							image_filename = os.path.join(image_path, (post + ".jpg"))
							image_url = submission.url
							urllib.urlretrieve(image_url, image_filename)
						
							try:

								#Testing image for corruption
								##This is not fully reliable yet, still getting some corrupt images
								im = Image.open(image_filename)
								
								#If this throws an error then a text file will not be created and
								##The image will be removed
								im.verify()							 
								
								#Creates a list of valid text filenames
								txtfiles.append(post + '.txt')
						
								#Create textfile to write comments to
								nfile = open(text_filepath, "w+")
								
								#**10/17/17** Check comment_queue size to avoid empty txt file bug
								while comment_queue:
									comment = comment_queue.pop(0)
									nfile.write(comment.body.encode('utf-8'))
									comment_queue.extend(comment.replies)
								nfile.close()
								print("Success!")
							except:
								#Displays corrupt image error and deletes corresponding image
								print("Image %s.jpg corrupt. Removing..." % post)
								os.remove(image_filename)
					except:
						#Throws an error if any issues arise from retrieving submission
						print("Unable to collect post... continuing")

			#Creates a list of txtfiles for each sub
			txtfiles_filename = "%s_textfiles.txt" % sub
			txtfiles_filepath = os.path.join(raw_text_path, txtfiles_filename)			
			textfiles = open(txtfiles_filepath, "w+")
			for txt in txtfiles:
				textfiles.write(txt + "\n")
			textfiles.close()

		
			#End of program info
			totalPosts += len(txtfiles)


	print("Collected data from a total of %s posts." % totalPosts)
	
	#Outside of sub loop, keeps track of runtime
	ELAPSED_TIME = time.time() - START_TIME
	m, s = divmod(ELAPSED_TIME, 60)
	h, m = divmod(m, 60)
	print("%dh:%02dm:%02ds" % (h, m, s))

			
main()			
