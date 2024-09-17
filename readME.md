pip install -r requirements.txt

create a .env file in the root folder

store the TWITTER_KEY and TWITTER_SECRET in the .env file
set the FLASK_APP = webapp.py

set SECRET_KEY. FACEBOOK_APP_ID and FACEBOOK_APP_SECRET

Kindly, visit the website https://unbiasedanalytics.herokuapp.com/ 

Create an account and test the following API endpoints

https://unbiasedanalytics.herokuapp.com/api/v1/amazon/Roku-Streaming-Device-Vision-Controls/B09BKCDXZC

https://unbiasedanalytics.herokuapp.com/api/v1/konga/samsung-galaxy-a03-core-6-5-32gb-rom-2gb-ram-dual-sim-4g-lte-5000mah-black-5577143

https://unbiasedanalytics.herokuapp.com/api/v1/jumia/UM742MP0DHARQNAFAMZ

INFO: The links below can only work if the user's instagram account is a business account
and is linked with the facebook page

Hence, to be able to test these links kindly follow appropraite tutorials on how to create an instagram business account and link it
to your facebook page

https://unbiasedanalytics.herokuapp.com/api/v1/instagram/comments

https://unbiasedanalytics.herokuapp.com/api/v1/facebook/page-post-comments

https://unbiasedanalytics.herokuapp.com/api/v1/instagram/hashtag-search/peterobi

NOTE: For users with multiple facebook pages, only the most recent page will be interacted with.
	current API version does not provide options for multi-page/ multi-post interaction

COMMON ERRORS: SessionNotCreatedException
                from selenium.common.exceptions import SessionNotCreatedException

                with the msg "SessionNotCreatedException.msg"

                If you come across this kindly reload the page.

NETFLIX
YOUTUBE
IMBD
PLAYSTORE
NEWS MEDIA ***