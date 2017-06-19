# Udacity Full-Stack Nanodegree

## Project 3 : Item Catalog

### by Yash Sharan

## Overview

Project 3 implements a web application that provides a list of items within a variety of categories and integrates third-party user registration and authentication.

## How to Run

Please ensure you have Python, Vagrant and VirtualBox installed. This project uses a pre-congfigured Vagrant virtual machine which has the [Flask](http://flask.pocoo.org/) server installed.

## Run the virtual machine!

Using the terminal, change directory to oauth (**cd oauth**), then type **vagrant up** to launch your virtual machine

after that **vagrant ssh**

Within the virtual machine change in to the shared directory by running

```bash
$ cd /vagrant/
$ python database_setup.py      //to initialize the database.
$ python lotsofmenus.py         //to populate the database with companies and cars. (Optional)
$ python project.py             //to run the Flask web server. In your browser visit **http://localhost:5000** to view the car detail app.
```

Then navigate to localhost:5000 on your favorite browser.
