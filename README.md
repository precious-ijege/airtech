# airtech
[![Build Status](https://travis-ci.org/precious-ijege/airtech.svg?branch=develop)](https://travis-ci.org/precious-ijege/airtech)
[![Coverage Status](https://coveralls.io/repos/github/precious-ijege/airtech/badge.svg?branch=develop)](https://coveralls.io/github/precious-ijege/airtech?branch=develop)
## Description
This repository contains the API enpoints for a Flight management system. The system enables authenticated and authorized users book flight tickets, purchase flight tickets and also make flight resevations. The system is built using the Django rest framework.

## Feaatures
A User can:
- Register
- Log in
- Upload passport photographs
- Book tickets
- Receive tickets as an email
- Check the status of their flight
- Make flight reservations
- Purchase tickets

An Admin user can:
- Create flight

The system supports:
- encrypting password
- handling multiple requests
- User authentication

### API Documentation
Follow this [link](http://) to view the full api documentation.

## Technologies
**airtech** makes use of a host of modern technologies. The core ones are:
- Python 3
- Postgresql
- Django Rest Framework (API development)

## Getting Started
These instructions will get you a clone of the project up and running on your local machine for development and testing purposes.

- Clone the repository:
```
$ git clone https://github.com/precious-ijege/airtech.git
```

- Open the project directory:
```
$ cd airtech/flight_backend
```
### Create a virtual environment
For this project, I will be using `pipenv` to manage my working environment as well as package installation.
To install `pipenv` run this command:
```
pip install pipenv
```
To install all packages from the `pipfile`, run this command:
```
pipenv install
```
Activate the virtual environment by running this command:
```
pipenv shell
```

### Set up environment variables
Create a `.env` file to add the necessary environment variabbles.

- check `.env.sample` file for list of variables to set.

### Set up Database
- Create a database:
```
$ createdb db_name
```

- Run migrations
```
$ python manage.py migrate
```
### Running the app
- To run tests:
```
$ python manage.py test
```

- Run the app:
```
$ python manage.py runserver
```

### Create a Superuser account
- To create a super user account for accessing the admin dashboard, run the following command:
```
python manage.py createsuperuser
```

- Enter your email and password
You can log into the admin dashboard using those credentials on `http://127.0.0.1:8000/admin/`

### How To Contribute
Contributing to this project would always be a welcoming idea. If you feel you have an addition to make this project better, follow the steps bellow:
- **Fork** the repository.
- Create as many **branch** as you like depending on how many features you would love to add. One feature per branch.
- Make neccessary changes and **commit**.
- Finally, submit a **pull request**.

### License

This project is authored by **Ijege Precious** (precious.ijege@andela.com) and is licensed for your use, modification and distribution under the **MIT** license. 

[MIT][license] © [andela-pijege][author]

<!-- Definitions -->

[license]: LICENSE

[author]: andela-pijege