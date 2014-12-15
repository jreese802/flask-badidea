# My Flasky Midterm

## Why I did what I did.

I really wanted to learn about Bootstrap and SQLAlchemy. Those were two technologies, frontend and backend, that seemed to streamline some of the most tedious parts of building a website. Bootstrap promised to streamline the CSS process and allow for websites that look good and function well on any platform.

I started with a basic idea: I was going to create a website that would allow anyone to upload pictures and comment on them. My goal for Flask was to figure out how to pass data back and forth from the server via GET and POST, and how to set up a (fairly basic) database with some foriegn keys.

## What sources I used.

Luckily there are a lot of tutorials out on the internet about how to set up Flask with WTForms (a helpful form creator/processor) and SQLAlchemy. By far the most helpful resources was *Flask Web Development* written by Miguel Grinberg and published by O'Reilly Media. The book went over many use cases for Flask and gave very detailed instructions on how to integrate Flask with other technologies (e.g. Bootstrap and SQLAlchemy).

I also utilized the ["Flask Mega Tutorial"](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by Miguel Grinburg for some clarification about SQLAlchemy. Google and Stack Exchange were indispensibletools as well. I would not have been able to solve all of my little problems if other people didn't make the same mistakes.


## So what did I do?

I started out by planning the website. I wanted to have a home page, an upload page, a page to browse the uploaded images, and each image should have its own page with comments.

The home page was easy enough to create. It was just a completely static page from a simple template. I used bootstrap to create a navbar and a footer, as well as to line up the elements on the page. The navbar, "jumbotron", and descriptions of the upload and browse page all changed shape and size as the screen size increased and decreased.

The "upload" page isn't very pretty, but it does allow people to upload pictures as .jpeg/.jpg, .bmp, and .png. The page uses POST to get the image from the WTForm where it turns the filename into something harmless and adds it to the database, along with a datetime. It is also responsive, but there's not much to move around as the screen gets smaller.

The "browse" page makes a query request to the database to find the photos and sorts them by the date they were uploaded. The template for the page loops through the results of the query, turns each one into a thumbnail box, and displays a grid of the results that reacts to screen size. The grid layout is a little broken right now because it doesn't know how to reconcile images that are weird sizes. I was hoping that it would automatically reflow correctly but it doesn't.

Each picture can be clicked on and a page is generated showing the picture, the comments on the picture, and a box to enter new comments. The comments are sent via POST and when the server receives the request it adds an entry to the database with the sterilized text of the comment, a timestamp, and a reference to the image. Everything is working just fine for now but I didn't do much with the CSS so everything looks kinda crappy. 

## That's fine. Now what?

Well, if I worked more on this website I would add an optional account system so that people could sign up and have their comments and uploaded images attributed to them. To make it work I would create an extra table for Users. That table would have columns for usernames and hashed passwords. Comments and images would have extra foreign key fields for the user who uploaded them.

The way the site handles thumbnails right now is a problem because it just loads the full resolution image and resizes it with css. If I worked on it more I would add a function to automatically generate thumbnail-sized images when an image is uploaded. 

I would also do a lot more to the css. Right now the website is really ugly.

## What did I learn?

I learned a **ton** about Flask. I didn't realize how little I understood what was going on under the hood until I had to debug a lot of my code. Once data started getting passed back and forth I had to actually think about Flask's different contexts. I also discovered the power of the Flask debugger. Being able to drop into a terminal to help figure out SQLAlchemy was great. I would have been lost for a long time and I wouldn't have gained as much knowlege of the structure of SQLAlchemy. 

SQLAlchemy caused a lot of headaches during the setup process, but it made life a lot easier once I got it working. I'm still not totally happy with the schema it generates, though. If I worked on it more I would spend time tweaking the database creation code. 

Not a lot of Bootstrap made it into my website. I learned a lot about it during my research for this project but there weren't many places on my website to apply it. I'm still not sold on Bootstrap as a framework. I found it restrictive, even just for my final project. It's really easy to make something that looks decent and generic, but it can be pretty tough to make something that looks good and unique. 

If I redid the front-end I would probably use Foundation. It is similarly *Mobile First* but it doesn't seem as limiting. 

## So, you wanna see it?

Well, here are some pictures:

