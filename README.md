# Project 1

Web Programming with Python and JavaScript

Created a library app that allows users to register, sign in, search for books, see the book's information, and write reviews.
Also created an API that accepted GET requests using a book's ISBN number and return a JSON of that book's information.

import.py will import 5000 books into the SQL database.

books.csv contains 5000 books and their title, author, and publication year.

application.py is the backend server handling the routes and database calls.

templates folder contains all of the views and html files.

static folder contains the JavaScript file that dynamically creates the login and sign up forms.

<code class="highlighter-rouge">pip3 install -r requirements.txt</code>

<strong>This is all pre-loaded into the app using python-dotenv and the .flaskenv file.</strong>

Set the environment variable <code class="highlighter-rouge">FLASK_APP</code> to be <code class="highlighter-rouge">application.py</code>. On a Mac or on Linux, the command to do this is <code class="highlighter-rouge">export FLASK_APP=application.py</code>. On
Windows, the command is instead <code class="highlighter-rouge">set FLASK_APP=application.py</code>. You may
optionally want to set the environment variable <code class="highlighter-rouge">FLASK_DEBUG</code> to <code class="highlighter-rouge">1</code>, which will activate Flask’s debugger and will automatically reload your web
application whenever you save a change to a file.

Make sure that you’ve set your <code class="highlighter-rouge">DATABASE_URL</code> environment variable before running
<code class="highlighter-rouge">flask run</code>!
