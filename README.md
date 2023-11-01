# Hyrule Compendium
#### Video Demo:  https://youtu.be/5QqQxyYnbEs
#### Description:

For my final proect for CS50w I've used Django and JavaScript to build "The Hyrule Compendium". This app will allow users to look up items and monsters in The Legend of Zelda: Breath of the Wild, a video game on Nintendo Switch. A portion of the game involves the tracking and collecting photographs of the creatures, monsters, weapons and materials in the land of Hyrule. The website is designed to assist users in looking up the in-game locations that they can track down these items as well as tracking their progress and managing a separate TODO list. Additionally, if feeling indecisive, a "Random Entry" feature can be used to give the user an item or creature to complete, collect or photograph.

This wouldn't have been possible without the Hyrule Compendium API (https://gadhagod.github.io/Hyrule-Compendium-API/#/) by Aarav Borthakur and I have already been in touch with the author to see if I can assist with anything on the new version.

I made the choice to allow some of the functionality of the app to be used by users that have not signed up or logged in (Browse, Search, Random Entry) while, by necessity, other features are behind a log in (Item tracking and TODO lists).

While logged in, the view of a specific entry will also include buttons to "compelete" or "uncomplete" an item as well as to add or remove it to/from their TODO list.

### Features

#### Browse

The Browse feature is available to all users regardless of whether they are logged in. First they are presented the main five categories of items, Creatures, Materials, Equipment, Monsters, Treasure. Each of these links triggers an API call to return all entries under the clicked category and populate them as an unordered list, each of which is a hyperlink to the full entry for that specific item.

#### Search

On the search page, users are able to carry out a case-insensitive search by sub-string for any items in the game. For example, a search of "Shield" will return a list of the 30 items containing the substring "shield" in the game, again as an unordered list of hyperlinks to the entry for each item. The search is handled with an API call to the end point for "All" items and filters the results based on the substring.

#### Random Entry

The Random Entry page will return a random entry from the entire compendium. Although this works with the same API as the Browse & Search features, the API call for the Random Entry feature is handled in python as part of the `random_entry()` view in `views.py`. I found that allowing python to deal with generation of a random number on which to base the choice was cleaner than doing the same through JavaScript.

If the user viewing an entry is logged in, buttons will also be rendered allowing the item to be marker as "compelte" or added to the todo list. These buttons do not render if the user is not logged in through the use of a jinja "if" block checking if there is an authenticated user. These buttons render to either add or remove items depending on whether they are or aren't already on the list in question and are updated with a JavaScript PUT request to an API view so that the browser does not need to be refreshed in order for the user to "complete" an item or add one to their To-Do list.

#### MyTracker - BrowseMyTracker

If logged in, a user is able to access the BrowseMyTracker feature. This works functionally the same as the main browse feature but excludes all items that the user has marked as complete. Completions are a django model consisting of an itemid and a User (another Django model).

#### MyTracker - To-Do list

The To-Do list feature allows logged in users to manage their own To-Do list. Items can be added through a button on the item's entry page so the user can prioritise them and equivalently removed once they have been completed.

### Distinctiveness and Complexity

I believe this project satisfies the Distinctiveness and Complexity requirements due to the number of features implemented in the project, the different methods used to implement the features and the app being completely distinct from any projects carried out during CS50. A high level view of some of the added complexity includes:

- API calls being carried out through both GET and PUT
- API calls being carried out both with JavaScript and Python
- Features being differentiated between general use and specifically for logged-in users
- Styling allowing for use of the app in a mobile browser
- The building and use of a custom jinja template tag when none of the existing tag rendered text in the "correct" way.


### Key files

#### views.py

`views.py` contains all the functions that allow the app to render each view (listed in `urls.py`) as it is requsted by the user.

- `index()` is the default view accessed through the "" route. It renders `browse.html` which allows all users to browse items by category (via js API call) regardless of whether they are logged in or not.

- `search()` renders `search.html`, the template which allows users (logged in or not) to search case-insensitively for any items containing the searched substring.

- `compendium_login()` is the view accessed either through the log in button in the nav bar or through the submit button on the log in screen. The navbar submits a GET request which renders `login.html` wheras the submit button submits a POST request which attempts to authenticate and log the user in. This view caused some trouble as I initially called it `login()` and didn't realise it was clashing with the django.contrib.auth function of the same name.

- `compendium_logout()` is a view accessed from a navbar link that is only visible to logged in users and uses the `logout()` function to log the current user out and then redirect to the `index()` view which renders browse.html

- `register()`, as with `compendium_login()` reacts differently to GET and POST requests. A GET request, accessed from the navbar link, will render `register.html`. A POST request, accessed from the submit button on `register.html` will attempt to register a new user for the app. The registration process carries out checks that the password and password confirmation match, that the password is at least 8 characters in length and then uses a `try/catch` block to handle cases where the user already exists. There were problems here as, at first, I failed to use the `create_user()` function of Django Models and instead just used the syntax to manually create a new object. This had the problem of failing to hash passwords meaning that, not only was there a security flaw in that passwords were being stored in plaintext but, additionally, users could not signed in as the `login()` function hashes the password entered by the user but then compared it to the plaintext password held in the database.

- `mytracker()` is the a view only accessible to logged in users via a navbar link that does not render if no user is logged in. It presents a page where the user can then access (via JavaScript only) either the BrowseMyTracker feature or their todo list.

- `entry()` is the view that will render the details for one specific entry from the compendium. The view takes in the item id as an argument and makes an API call in python before providing the details of the entry as context to `entry.html`. Part of the reason that this was done in Python is that I found it simpler to query my Django models here when there is a signed in user to check whether the entry in question is on/off a user's completed list and on/off a user's todo list in order to correctly render the buttons. Another option would have been to set up an API view to get those details via JavaScript but I felt that refreshing the browser when navigating to a new entry felt like an appropriate way to set up this feature rather than trying to set up a "one page app".

- `random_entry()` is accessed via a navbar link and generates a random number from 1 up to the length of the response from the Compendium API. This random number is then fed into the `entry()` view above. I recognise that calling the entire API in order to generate a random number may be excessive and in some circumstances inappropriate but I wanted to avoid hardcoding the maximum item id so that the views will remain robust if the API author were to add new items to their API.

- `toggle_collection()` is a view only accessed via an API call (of type PUT) that allows the user to toggle whether they have completed/collected an item or not. A `try/except` block in the view is used to "complete" the item if a model does not exist but if one already exists and an `IntegrityError` access the "except" block then the existing "Completion" is deleted, effectively toggling the item to incomplete.

- `toggle_todo()` works in exactly the same way as `toggle_completion()` except it refers to the Todo model instead of the Completion model. See below for more details on models.py

- `todo()` todo is an API view accessed through JavaScript. Once a user is logged in and has browed to the MyTracker page, a ToDo List link accesses this view via  which gathers a list of the item ids on the users ToDo list and uses them to make an API call for each from the Hyrule Compendium API in order to render a list of hyperlinks that the user has marked as their todo list.

- `completed()` is a similar view to `todo()` but that returns a list of the completed items by a user in order that JavaScript can construct a browsable list of all items that have not been completed by the user.

#### models.py

The app contains three models.

- `User`, inherits from `AbstractUser` and includes fields for username and email
- `Completion`, includes fields for itemid and compendium_user (a foreign key). The itemid is a simple integer field so that they can be fetched without needing to make an API call to the Hyrule Compendium API. The `Completion` model also contains a `__str__` function that returns an appropriate string representation of the model ('User' completed 'itemid') and a meta class that forces uniqueness across combinations of User and itemid
- `Todo`, includes fields for itemid and list_writer but other than that is functionally identical to Completion. The `__str__` function renders the model as "'User' prioritises 'itemid'"

#### custom_tags.py

`custom_tags.py` contains one function, `entry_title_filter(s)` which takes a string as an argument and returns it in a properly cased format. The reason for this was that I was initially using the `title` tag inside a jinja tag with the format `{{item|title}}` but a number of item names rendered awkwardly with this. One example is the "guardian scout iii". Item names are all ower case in the API response and most lend themselves to title casing. The above, however, renders as "Guardian Scout Iii" (along with its brothers "Guardian Scout Ii" and "Guardian Scout Iv"). For the sake of cleaner styling, the `entry_title_filter()` function checks if the item name is one of the above cornercases and, if so, splits the full name into a list of its component parts and applies title casing to all except the last part to which is applies upper casing. This is then used in `entry.html` with the line `{{data.name|entry_title}}`.

#### compendium.js

`compendium.js` starts with an `EventListener` that triggers on `'DOMContentLoaded'` which applies "onclick" listeners to a number of list items on the page. It additionally uses if statements to apply onclick listeners to some html tags that may or may not exist depending on which page the user has loaded. The use of if statements allows for the avoidance of errors.

Beyond this are a number of functions, each of which are listed here.

- `search()` is the function accessed through an "onclick" listener on the submit button on search.html. It triggers am API request to the Hyrule compendium then filters it to only include items where the name includes the search term. For each of the items that matches, an `<li>` tag is created that contains an `<a>` tag that links to the entry for that item. The construction of the `<li>` is handled through a custom function construct_li() detailed below. Equally, before populating the `<ul>` with any of these tags it runs the custom function `clear_children()` that removes the results of the previous search from the `<ul>` (details below)

- `object_by_category()` makes an API call by one of the five item categories and returns every item in that category. Calls to `clear_children()` removes the last browsed cateogry and a loop over each item in the response utilises `construct_li()` to create an `<li>` that can be inserted into the `<ul>`

- `my_objects_by_category()` works similarly to `objects_by_category()` but also makes a call to the `completed()` view to use a list of the user's completed items as a filter for their own personalised browsing list. This was built as an async function because it makes two calls separately, one of which is able to start before the other one finishes. The two results are then combined to produce the user's output.

- `clear_children()` is a custom function used to clear all child element from an unordered list. It takes a parent list as an argument then loops over every chilc element in the list removing them until there are none left. It has no return value.

- `construct_li()` is a custom function used to take in a response object from an API call (effectvely the details of one item). It then creates a new `<li>` and `<a>` tag. Applies a custom href and textContent to the `<a>` tag and embeds the `<a>` tag inside the `<li>` tag. The function then returns the `<li>` tag as an item that will be appended to a `<ul>`

- `to_title_case()` is a custom function that serves a similar purpose to `entry_title_filter()` in `custom_tags.py`. After building the custom tag I realised the same issue was happening in the lists that were being rendered on each page. This custom function fixes the casing for "guardian scout iii" from "Guardian Scout Iii" to "Guardian Scout III"

- `toggle_collect()` is a function accessed through the "Collect" button on an entry page that passes a PUT request to the `collect()` view in `views.py`. This is what allows a user to toggle whether they have collected an item or now.

- `toggle_todo()` is identical to `toggle_collect()` but allows a user to toggle the status of an item on the ToDo list.

- `display_todo()` is accessed through an "onlick" event on the ToDo list option in the MyTracker feature. It make individual calls to the 'todo' view to obtain a list of the items on a users todo list and then uses that as a filter to make individual API calls for each of those items so that they can be rendered as a list after passing each to `construct_li()`

- `display_my_browser()` is a function used to toggle the `style.display` property of the html tags in the MyTracker page between `block` and `none` so that all MyTracker functionality can be accessed through the same page.

### Any Other Business

I can't express how much I enjoyed building this. It's a lot of fun to build something that intersects with your other hobbies. I think the weaker part of this project is the page styling. Admitedly, front end design is not where my priorities lie and I am always more interested and spend more time on the back end programming of a project like this as opposed to the front end styling.

Astute fans of The Legend of Zelda will notice that this compendium relates to the prior game "Breath of the Wild" rather than the more recent release "Tears of the Kingdom". The API currently contains no images of ToTK items and I felt that would do a diservice to the final project so ended up focusing on the earlier title in the series. That said, I have since reached out to the API author and am looking for a way to help with completion of the assets for the newer game, giving me an exciting opportunity to collaberate through GitHub for the first time on a real world project.
