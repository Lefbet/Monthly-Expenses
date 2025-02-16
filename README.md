# Monthly Expenses
#### Video Demo:  <https://www.youtube.com/watch?v=mBOVD7gingI>
#### Description:
This project is a web-based application using JavaScript, Python, and SQL that records a user's daily expenses and classifies them by the category they belong to. It is intended to be used as a way to keep track of one's spending over a monthly period, so as to get a better understanding of the places they spend the most money at and adjust their budget accordingly.
The web page requires the user to log in before they can use the application. If the user is not logged in, the only pages they have access to are `/login.html`, where they are always redirected to if they try to access another page and `/register.html`, where they are prompted to create a new account. After the user successfully logs in with their credentials, they get full access to every aspect of the web app. They can then:
* Add a new expense, where they are required to provide the category in which the expense belongs to (i.e. rent, food, health etc), the amount of money they spent, an optional description for future reference and the date it took place. If a date is not selected, it is considered to be the current date of the recording.
* Add a new category of their choosing if they are not satisfied with the predetermined ones.
* View a history of their past expenses in the form of a table ordered by date recorded. The option to remove any transaction is also availiable at this page.
* Get an overview of all the expenses that occurred on a monthly basis, grouped by category. The sum of all expenses in that specific category is displayed, so that the user can clearly inspect the total amount of money they spent in each one. The grand total is also displayed at the end of the page, which is the sum of all the money spent during that month. The default month that is displayed when accessing this page is the current one, but the user can also select to display any year and month combination of their choosing through the select form. Only the years that have actual entries are selectable here. The option to display the expenses of a whole year is available as well.
* Perform actions regarding their account, like changing their password or logging out. If the user does not log out, their session is maintained in that platform and the next time they try to access the application, they will not be required to input their credentials again.
For all the above actions, there are checks taking place whenever user input is expected. If it is possible, the checks are being done client side using javascript, more specifically the functions that are defined in the file `validation.js`. Such examples are checking if important fields are left blank or if the user password has less than four characters. If it is not possible, like when the database must first be accessed in order to validate an input (the user's password for example), then an error message is delivered from the server in the form of a picture with `apology.html`.

In order to store each user's credentials and their respective expenses, a `sqlite3` database is used which is named `budget.db`. It contains three tables:
* The table `users` stores:
  - each user's unique `id`,
  - their `username`, which must also be unique and
  - a `hash` code of their password, so that even if somebody has access to the database itself, they won't be able to extract the original password of each user.
* The table `categories` stores:
  - the unique `id` of the category/user combination,
  - the `user_id` of the user who created the category, which references the `id` of the previous table `users` and
  - the name of the `category`.
* The table `expenses` stores:
  - the unique `id` of the expense,
  - the `user_id` of the user who made the expense, which references the `id` of the previous table `users`,
  - the `category` in which the expense is classified by the user,
  - the `amount` of money they spent for this expense,
  - an optional `description`, where the user can add more information about the transaction for personal reference and
  - a `timestamp`, the date in which the transaction took place.

For the development of this project, the `flask` framework was used. Let's take a closer look at each file:
* In the `static` directory, there are two files:
  - `styles.css`, the css file that is used to adjust the appearance of the web pages and
  - `validation.js` where the functions that validate the user input are defined as mentioned above.
* In the `templates` directory, there are nine html files that define the content and structure of each web page:
  - `layout.html` is the general layout of all the pages which is used to avoid repeating lines of code,
  - `login.html`, `register.html` and `change_password.html` offer forms where the user inputs are received,
  - `add.html` (add expense) and `categories.html` (add category) also expect user inputs in order to add new entries to the corresponding table of the database,
  - `apology.html` displays a picture with an error message when something goes wrong,
  - `index.html` presents an overview of all the expenses that occurred over a monthly period, grouped by category and
  - `history.html` shows a history of all past expenses of the current user.
    * The last two html files also offer forms for the user to alter what is presented according to their needs.
    * It is also worth mentioning that the bootstrap library is used to make this web app look better on every device.
* Lastly, there are two more python files that contain all the code which is executed by this application:
  - `app.py` is the backbone of this application, a python code that indicates what is shown when a web page is requested while handling all the appropriate database queries and
  - `helpers.py` contains three helper functions which are used throughout `app.py`.
    * Both these python files are filled with comments that explain what each block of code does.
