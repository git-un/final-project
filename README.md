# 507 Fall 2017 - Project 6.5

## Part 1 (200 points)

Add a route `/word/<new_word>`

Using the Datamuse API: https://www.datamuse.com/api/

* Whatever `new_word` is in the URL, this route should simply show a plain old string that is a word that rhymes with whatever the value of new_word is. So, for example, if you went to the URL `http://localhost:5000/word/cat` a possibility is that you’d see on your screen
 **`bat`**


## Part 2 (200 points)

There exists a route already `/flickrphotos/<tag>/<num>`

There is already code in it to make a request to flickr for info about photos tagged with the tag in the url, but only the number that is in the url.

* To get it to work (even though it won’t quite do what you eventually want yet), all you have to do is fill in a valid Flickr API key
(URL to get one if you don’t already have one: https://www.flickr.com/services/api/misc.api_keys.html — You’ll need a Yahoo or Hotmail account, but it doesn’t have to be one you really use.)

* Your goal is to edit the route code a little bit so that the template provided, `photo_info.html` shows data when you go to e.g. `http://locahost:5000/mountains/2` or `http://localhost:5000/sunset/1`, or whatever.


    * At the top, the number of photos that were retrieved (1 photo was retrieved or # photos were retrieved, with the # replaced by whatever number it was)

    * And then, a bulletpoint “unordered list” (`<ul>`) of each of those photos’ titles.

    * [Like this](https://www.dropbox.com/s/uxdhm699lejjmsu/Screenshot%202017-11-28%2022.08.07.png?dl=0)

You’ll need to add a small amount of code at the end of the view function, and you’ll need to edit the invocation of `render_template` to send the right data to the view.

So, you’ll need to check out `photo_info.html` to figure out what the Jinja templating code in that file is expecting, and send the right values, with the right names, to it!



## To submit

* Fork and clone this repository we’ve provided
* Make changes to complete parts 1 and 2, and add and commit them all
* (Check if it works)
* Push them to your fork of the repository
* Submit a link to your fork at the Project 6.5 assignment on Canvas
