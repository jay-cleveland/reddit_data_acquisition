#Reddit Data Acquisition
#Author: Jaycee Cleveland

#V2 Changes: Implemented code to retrieve list of all post IDs from pushshift API


from __future__ import division
import praw, urllib, os, string, time, requests
from PIL import Image

def main():
	#**10/12/2017** implement read in subreddit list (done)
	##25-30 subreddits

	#Keeps track of program runtime
	PROGRAM_START_TIME = time.time()	

	#Reads in a list of subreddits to process
	subs = []
	with open("subreddits.txt") as subreddits:
		for subreddit in subreddits:
			subs.append(subreddit.rstrip())

	#Create an instance of the PRAW Reddit object
	reddit = praw.Reddit(user_agent="Data Acquisition (by /u/kaislyn89)",
			client_id="1ZJR-h5YqFJg-Q", client_secret="JjoK7f5_JF5th7c1BvpVa3DCFk0")

	
	#Goes through each subreddit in the subreddit.txt list
	for sub in subs:		

		#Lists to store ids and txtfile names
		posts = []
		txtfiles = []

		#Gets list of post ids from subreddit using Pushshift API credit to /u/Stuck_in_the_Matrix
		posts_URL = "https://api.pushshift.io/reddit/search/submission/?size=500&subreddit=%s&num_comments=>100" % sub
		postsAPI_Data = requests.get(posts_URL)
		postsJSON = postsAPI_Data.json()
		posts_Obj_List = postsJSON['data']
			
		#Creates a list containing all post IDs in the subreddit
		##Iterates through first 500 objects returned from API call
		for post in posts_Obj_List:
			posts.append(post['id'])

		#Sets the API call to pick up at the post made prior to the created_utc of the last post from previous call
		##iterates to end of subreddit, filters by total number of comments >= 100
		if len(posts) == 500:
			while(True):
				date_created = posts_Obj_List[-1]['created_utc']
				posts_URL = "https://api.pushshift.io/reddit/search/submission/?size=500&subreddit=%s&num_comments=>100&before=%s" % (sub, date_created)
				postsAPI_Data = requests.get(posts_URL)
				try:
					postsJSON = postsAPI_Data.json()
				except:
					break
				posts_Obj_List = postsJSON['data']
				if len(posts_Obj_List) == 500:
					for post in posts_Obj_List:
						posts.append(post['id'])
				else:
					for post in posts_Obj_List:
						posts.append(post['id'])
					break
							
		print(len(posts))
		
		#Prevents div/0 error when there are no viable posts to harvest from the sub, also skips sub if 0 viable posts
		if len(posts) != 0:
			sub_path = "/home/kaislyn/RedditData/subreddits/%s/" % sub			#Change directory in this line
			raw_text_path = "/home/kaislyn/RedditData/subreddits/%s/raw_text/" % sub 	#Change directory in this line
			image_path = "/home/kaislyn/RedditData/subreddits/%s/images/" % sub		#Change directory in this line

			#Checks to see if subreddit path already exists, if it does, subreddit is skipped
			if not os.path.exists(sub_path):
			
				#Create paths if they don't exist
				os.makedirs(raw_text_path)
				os.makedirs(image_path)

				#Subreddit Data Information
				totalCommentsInSubreddit = 0
				avgCommentsPerPost = 0
				sub_Data_File = open((sub_path + ("%s_data.txt" % sub)), "w+")
				SUB_START_TIME = time.time()

				for post in posts:

					try:
						#Creates the submission object using the post id		
						submission = reddit.submission(id=post)			

						#Only works on posts that have an image url associated with them
						if (".jpg" in submission.url) or (".png" in submission.url) or (".bmp" in submission.url):
						
							#Create text filepath
							text_filepath = os.path.join(raw_text_path, (post + '.txt'))
						
							print("Aquiring post id %s from %s." % (post, sub))	
						
							#Grabs image from post
							
							#**10/17/17** Fixed bug for downloading corrupt images
							
							if (".jpg" in submission.url):
								image_filename = os.path.join(image_path, (post + ".jpg"))
							if (".png" in submission.url):
								image_filename = os.path.join(image_path, (post + ".png"))
							if (".bmp" in submission.url):
								image_filename = os.path.join(image_path, (post + ".bmp"))
							
							urllib.urlretrieve(submission.url, image_filename)
						
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
								comments_File = open(text_filepath, "w+")
								
								#Reverted back to using Reddit API for comment calls
								submission.comments.replace_more(limit=0)
								for comment in submission.comments.list():
									comments_File.write(comment.body.encode('utf-8'))
									totalCommentsInSubreddit += 1

								comments_File.close()	
								
								print("Success!")
							except:
								#Displays corrupt image error and deletes corresponding image
								print("Image %s corrupt. Removing..." % image_filename)
								os.remove(image_filename)
					except:
						#Throws an error if any issues arise from retrieving submission
						print("Unable to collect post... continuing")

				
				#Creates a list of txtfiles for each sub
				txtfiles_filename = "%s_textfiles.txt" % sub
				txtfiles_filepath = os.path.join(raw_text_path, txtfiles_filename)			
				textfile_List_File = open(txtfiles_filepath, "w+")
				for txt in txtfiles:
					textfile_List_File.write(txt + "\n")
				textfile_List_File.close()

				#Creates a file containing subreddit data sub_Data_File
				totalPosts = len(posts)
				totalHarvested = len(txtfiles)
				percentYielded = (totalHarvested/totalPosts)*100

				if len(txtfiles) > 0:
					avgCommentsPerPost = totalCommentsInSubreddit/len(txtfiles)
				else:
					avgCommentsPerPost = 0

				SUB_ELAPSED_TIME = time.time() - SUB_START_TIME
				m, s = divmod(SUB_ELAPSED_TIME, 60)
				h, m = divmod(m, 60)		
		
				sub_Data_File.write("Sub Runtime: %dh:%02dm:%02ds\n" % (h, m, s))
				sub_Data_File.write("Total Comments Collected: %s\n" % totalCommentsInSubreddit)
				sub_Data_File.write("Average Comments Per Post: %.2f\n" % avgCommentsPerPost)
				sub_Data_File.write("Total Number of Posts Harvested: %s\n" % len(txtfiles))
				sub_Data_File.write("Percent of Viable Posts: %.2f%%" % percentYielded)
				sub_Data_File.close()
				

		else:
			print("%s contained no viable posts, probably too few comments." % sub)
		#End subreddit block


	#Outside of sub loop, keeps track of runtime
	h=m=s=0
	ELAPSED_TIME = time.time() - PROGRAM_START_TIME
	m, s = divmod(ELAPSED_TIME, 60)
	h, m = divmod(m, 60)
	print("Total Runtime: %dh:%02dm:%02ds" % (h, m, s))

			
main()
