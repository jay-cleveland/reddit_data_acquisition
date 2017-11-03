###THE PURPOSE OF THIS READ ME FILE IS TO INSTRUCT ON HOW TO USE THE INCLUDED SCRIPTS IN THIS DIRECTORY:

NOTE: These scripts have been written with the intent of running on a Linux system, they are not compatible with Windows. Additionally, please ensure that the proper amount of storage is available for any data downloaded by the scripts.

###INSTALLATION OF DEPENDENCIES

1. Run the installation.sh from the /RedditData directory in sudo mode. 
2. Ensure that all of the dependencies install correctly before proceeding.

###SCRIPT MODIFICATION FOR RUNNING

1. Open the reddit_data.py file and change the path in lines 24 and 25 to the correct path. The /subreddits directory and the following directory tree levels are created and traversed by the scripts, so it is essential that the paths are correct.
2. Modify the paths in line 31, 34, and 35 in the format_data.py file and ensure that the correct path is entered. 
3. Make sure that the subreddits.txt file has the desired subreddits listed. Note: Only the subreddit name in lower case is required. 

*BEFORE RUNNING*
1. Check your /subreddits directory, if you have a directory for a subreddit you have not fully harvested yet, remove the subreddit directory. If the program finds an existing directory for a subreddit in the list, it will skip that subreddit and go to the next one. So if your program is interrupted in the middle of harvesting from a subreddit, make sure you delete the corresponding directory before running the program again. This enables users to simple add additional subreddits to subreddits.txt without them being harvested every run. 
