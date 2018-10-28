# Project 2 - Web Programming with Python and JavaScript "Flack" by LOBSTERICK
## What's inside?
Inside this repo, you can find main application `flack.py` and two folders: `static` (with static files, like images and JS files) and `templates` (with templates of html views). After starting application, there will be created folder `flask_session` with session files of all user connected to server.
## What is Flack?
Flack is an online application, similar to [Slack](http://www.slack.com), providing possibility of contact between connected users in real-time. Concept of this app is based on three concepts:

* **nickname** - the name chosen by user to communicate with rest of the application users. One person can generate unlimited amount of nicknames and using them without any authorisation (*no password*). One nickname can be used by many people, but only one person can use specific nickname at the time. Nickname are available again, when user logged out.

* **room** - space of communication, storing messages. Nicknames can access all rooms, create new rooms (if specific room don't exist) and change room at any time. Every room store last 100 messages. Every message contain nickname of author, date of creation and text body of message. Nickname can also *"flush"* all activity; delete all messages that is connected with specific nickname.

* **sessions** - when user choose nickname, all data is stored in `session` belonging to to specific user. Thanks to localStorage, once nickname is reserved - can be used until user log out, even after closing browser.

<u>All communication in Flack is **real-time** - new messages and rooms appear immediately after receiving them by server, without manually reloading page.</u>

## How to start?
Just start Flask app and go to localhost address (f.e. `127.0.0.1:3000`). Everything should setup itself :) 
## How to use?
Type chosen nickname in form and click `Reserve nickname` button. After this, You will be redirect to `General` room. Now, You can send messages by typing them in form at the bottom of the page (*send by click enter*) or create new room using form located in right section of navbar. Changing room is possible in two ways - choosing room name in droplist in left section of navbar or using right-section form (if You type existing room name, it will redirect You to it).
## Used technologies

### Python
Primary language for all backend logic for this project, with use of **Flask** - framework for creating server and managing endpoints (8 routes; 2 dynamically generated, 1 API endpoint), along with: 
* **Flask session** - to store session-depended information, like nicknames or actual room in server side,
* **socketIO** - for emitting events like creating new room or message,
* **Flask render_template** - for rendering views depended on actual status of user's action,

### HTML
Primary language for all frontend logic for this project. All views are created by Flask's ***render_template*** with use of **Jinja2** providing possibilities like inserting variables in HTML code or view's dependency. All templates inherit from `layout.html`, adding specific elements for main page (`index.html`) and room page (`room.html`). Navigation bar provide different possibilities, depended on login status (logic implemented in Jinja2). Styling of HTML content is made using **CSS** (`main.css`). Most of elements are based on **Bootstrap 4**.

### Javascript
Language responsible for responsiveness of generated pages (`layout.js` and `room.js`). Using Javascript allow to using real-time events like:
* exchange messages and presenting it on page
* automatically updating room's list,
* sending messages with Enter key,
* preventing page reload on common events (like receiving and sending messages),
* sanitizing room names (for backend purposes),
* [<u>with</u> <u>*XMLHttpRequest*</u>] preloading posts on room change, using own API, checking login status
* access localStorage (remember nickname, even after closing window)

#### Security concern about `localStorage`
After adding localStorage logic in client-side, it is now possible to log in as user already logged in, due to nature of "log in check" in Javascript. In this app we trust that user provide us real information about his actions. It can lead to undefined behaviour if user manipulate his localStorage - from normal usage of one nick simultaneously by many people to server crash when trying preform actions after one of them logged out. Solution for this might require add password option, but - since the task was operating only on nicknames and reloading nickname even after closing browser - logic of the app was implemented in this way.

## Screenshots
### Index page
<p align="center">
  <img src=Screenshots\WelcomePage.JPG>
</p>

### First view after nick reservation
<p align="center">
  <img src=Screenshots\AfterLog.JPG>
</p>

### View of "General" room with new message
<p align="center">
  <img src=Screenshots\AfterLog.JPG>
</p>

### View of "General" from other user perspective
<p align="center">
  <img src=Screenshots\AfterLog2.JPG>
</p>

### View of created "Github" room
<p align="center">
  <img src=Screenshots\NewRoom.JPG>
</p>

### Small-screen view of site
<p align="center">
  <img src=Screenshots\ResponsiveView.JPG>
</p>