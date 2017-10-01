#Reddit Data Acquisition

import praw, urllib, os, string

def main():
	
	#Input subreddit from user
	sub = raw_input("Enter the subreddit you would like to search: ")
	post_limit = eval(raw_input("Enter the post limit you would like to load: "))

	#Paths
	raw_text_path = "/home/kaislyn/RedditData/subreddits/%s/raw_text/" % sub
	image_path = "/home/kaislyn/RedditData/subreddits/%s/images/" % sub

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
		if ".jpg" in submission.url:
			
			#Create text filepath
			text_filepath = os.path.join(raw_text_path, (post + '.txt'))

			#Grabs image from post
			image_filename = os.path.join(image_path, (post + ".jpg"))
			image_url = submission.url
			urllib.urlretrieve(image_url, image_filename)
		
			#Creates a list of valid text filenames
			txtfiles.append(post + '.txt')
		
			#Create textfile to write comments to
			nfile = open(text_filepath, "w+")
			
			#Queue created from comments in submission
			submission.comments.replace_more(limit=0)
			comment_queue = submission.comments[:]
			while comment_queue:
				comment = comment_queue.pop(0)
				nfile.write(comment.body.encode('utf-8'))
				comment_queue.extend(comment.replies)
			nfile.close()

	#Creates a list of txtfiles at program source			
	textfiles = open("reddit_txtfiles.txt", "w+")
	for txt in txtfiles:
		textfiles.write(txt + "\n")
	textfiles.close()
			
main()
		
			
