Sharing/Social
==============

- (1) Follow lists
	- (1.1) DB improvement to have the list of users and list of who follows who
	- (1.2) UI improvement to add a "follow" button on a user/list page
- (2) Ability to add (like) a present from a list to put it in our list
	- (2.1) Just duplicate entry in DB
- (3) Simple sharing on twitter/facebook/google+ of list or present
- (4) Followed lists show up on signed-in home page of user, mixed in with my presents, ordered by date added
	- Depends on (1)
- (5) Import list from Amazon wish list and others
- (6) Ability to fill in date of birth, and use this to remind followers of our birthday (and before xmas) by email or internal notification that you should check the list of the person
	- (6.1) Profile edit page
	- (6.2) IM system
	- (6.3) Cron jobs to check once per day the birthday and xmas to send IMs
- (32) Gravatar
	- (32.1) *DONE* Create gravatar URL and display image
	- (32.2) Fallback to default noImage URL if not gravatar is available

Design
======

- (7) *DONE* Simple, small logo
- (8) White theme, lot's of space to breathe
- (9) Block image-based layout with lot's of images for lists, with different image sizes
- (10) When clicking on an item, show detailed view (present preview mode). When logged in, this is where the delete button will be
- (31) Redesign add present page. See (19) to (25)
- (33) Redo the whole navigation.

Explore
=======

- (11) In present preview mode, show related presents (Amazon API or local DB matching thanks to tags?)
	- (11.1) For local matching, need tags for each present

List
====

- (12) Possibility to sort list by preference
	- (12.1) Save ordering in DB = need list entity per user in DB, or extra column
- (13) Infinite list with "load more …" or infinite scrolling
- (14) Show beneath present the like/add/preview buttons + number of times this was added to other lists
	- Depends on (2), but adds the need for saving this info into the DB

Access
======

- (15) Friendly URLs for lists and single presents
- (16) Mobile website

Profile
=======

- (17) Use username rather than email address for identifying list
	- (17.1) Move to appengine federated login
- (18) Use oauth or similar to login

Add present
===========

- (19) Redo present add page to show better the possible images and prices and descriptions, and let the user choose one, and then revert (unlike today)
- (20) Allow user to give URL for image too
- (21) Picture parsing not perfect still. Try here: http://www.ukcampsite.co.uk/tents/p/Vango-Spirit-200+/873
- (22) Improve bookmarklet as this will be the main way to get presents into the list: when used, redirect to the site, with pre filled add present page
- (23) When photo chosen, ask user to type a list of words to describe what is in the picture = tags. Also used internally to propose similar presents, and create some kind of image recognition system.
- (24) If there is no image chosen, or the present is simply added without site, do a request to http://images.google.com/images?q=... to get something
	- (24.1) Access to google image search jsonp API
- (25) Redo design with one textbox only (like buzz) which will detect whether it's a URL or not
	- *DONE* (25.1) Need smart input detector to get URL and description from the field
	- (25.2) Plug detector to the current search form and merge both simple and url search forms into one
		- *DONE* (25.2.1) Start to plug it in and simplify the code
		- (25.2.2) Finalize design as per drawing (should look like normal present with mouse-over edit-in-place stuff)
		- (25.2.3) Signify that images/title/price are being retrieved with loading indicator

Technical improvements
======================

- (26) Save images into the DB, with blobs, and resize them once and for all, to improve perfs and avoid 404
- (27) Continue to implement site-related parsers to provide better targeted content
- (28) Multiple currency support
- (29) SEO: meta, robots.txt, ...
- (30) Merge JS/CSS and minify
- (34) Move code to Github