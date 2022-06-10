# City OS Video Storage App

- [Instructions](#instructions)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Docker Compose](#docker-compose)
- [Features](#features)
- [About the Developer](#about-the-developer)

## Instructions

This challenge is about creating a simple video storage server with REST APIs with the following CRUD capabilities:

- Upload videos
- View all videos
- Delete videos
- Download videos

**How to Run Tests:**

```
$ python3 test.py
```

## Tech Stack

- **Backend:** Python3, Flask, SQLAlchemy
- **Frontend:** HTML5, CSS3, Bootstrap
- **Database:** PostgreSQL

## Installation

### Requirements:

- [PostgreSQL](https://www.postgresql.org/)
- [Python 3.7+](https://www.python.org/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

To run City OS Video Storage App on your local machine, follow the instructions below:

Clone repository:

```
$ git clone https://github.com/lauren-moore/shopify-challenge.git
```

Create and activate a virtual environment inside your project directory:

```
$ pip3 install virtualenv
$ virtualenv env 
$ source env/bin/activate
```

Install the dependencies:

```
(env) pip3 install -r requirements.txt
```

Seed the database:

```
(env) python3 seed_database.py
```


Run the app:

```
(env) python3 server.py
```

You can now navigate to `localhost:5000/` to run the app.


## Docker Compose

```
docker compose up
```



## Features

- **Upload a video to add to database:**  methods=["POST"]

Users can upload a video to their database by providing the following information: fileid, name.


- **View all videos in database:**  methods=["GET"]

View all the videos currently in the database.


- **Download video to desktop:**  methods=["GETT"]
  
Users download any videos in their database to their desktop. The video file name is restored to the original fileid.


- **Delete video from database:**  methods=["DELETE"]
  
Users can delete exisitng videos from the database. 






## About the Developer

As a Hotel Administration graduate, Laurén's background is in all things hospitality. From being a floor manager and bartender at a fine-dining restaurant to being a flight attendant, she has a passion for making others smile. She also has experience as an E-Com Producer and Project Manager where she works on board and card games. This appreciation for games, puzzles, problem solving, and logic lead her to tech. After taking courses in Computer Science and Python, Laurén knew it was time to transition into a life of software engineering and joined Hackbright Academy. Since graduating in April, she has continued to expand her technical skills by building projects and learning new technologies. She aspires to continue making a positive impact for others using her background in hospitality, passion for problem solving, and knowledge in Software Engineering. 

Let's connect on [LinkedIn!](https://www.linkedin.com/in/laurencaroleen/)

![image](/static/img/Business_card.jpg)