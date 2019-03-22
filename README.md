SI 507 Project 3 by Amanda Jung

In this project, the goal was to write a small Flask application that includes a database to hold data about movies from the files SI507_project3 and requirements.txt.

The file SI507_project3.py encompasses the code for the different parts of our Flask application. For example, it includes code for application configurations, class models (i.e. Movie, Director, & Genre), helper functions for database additions, and different Flask routes with specific set of inputs based on the url.

For the Flask routes, the first (home) route indicates how many movies have been saved to the database. The second route takes in input for a movie (i.e. title, director, and genre) and stores it in the database. The third route lists all the movies that are saved in the database. Last but not least, the fourth route takes the input for a movie genre and produces output of all movies in the database that are of the indicated genre.

The file requirements.txt contains the packages (e.g. Flask) that are necessary to run the files of code listed above.
