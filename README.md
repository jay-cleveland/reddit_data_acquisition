THE PURPOSE OF THIS READ ME FILE IS TO INSTRUCT ON HOW TO USE THE INCLUDED SCRIPTS IN THIS DIRECTORY:

NOTE: These scripts have been written with the intent of running on a Linux system, they are not compatible with Windows. Additionally, please ensure that the proper amount of storage is available for any data downloaded by the scripts.

###INSTALLATION OF DEPENDENCIES###
1. Run the installation.sh from the /RedditData directory in sudo mode. 
2. Ensure that all of the dependencies install correctly before proceeding.

###SCRIPT MODIFICATION FOR RUNNING###
1. Open the reddit_data.py file and change the path in lines 24 and 25 to the correct path. The /subreddits directory and the following directory tree levels are created and traversed by the scripts, so it is essential that the paths are correct.
2. Modify the paths in line 31, 34, and 35 in the format_data.py file and ensure that the correct path is entered. 
3. Make sure that the subreddits.txt file has the desired subreddits listed. Note: Only the subreddit name in lower case is required. 

