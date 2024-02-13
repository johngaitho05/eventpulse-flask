# EventPulse - Backend
### An event management system API built with Flask and SQLAlchemy

The API provides data for the following records

- Users
- Events
- Venues

For endpoints and supported methods, check out the documentation: [https://events.johngaitho.info/apidocs/](https://events.johngaitho.info/apidocs/)

![Photo](static/eventpulse.png)

## Installation

### Prerequisites
- MySQL version 5.7.*
- A [cloudinary](https://cloudinary.com/) account


**Note**: The following environment variables must be set for the API to work properly

#### Cloudinary Credentials
- CLOUDINARY_NAME - the name of your cloudinary application
- CLOUDINARY_KEY - the application key
- CLOUDINARY_SECRET - the application secret key

#### Database Environment
- EVENTPULSE_USER - eventpulse_dev
- EVENTPULSE_PWD - eventpulse_dev_pwd
- EVENTPULSE_HOST - localhost or the ip of your database server

### Setting up the database
```shell
cat setup_mysql_dev.sql | -uroot -p
```

### Setting up the project
#### Clone the repository
```shell
git clone git@github.com:johngaitho05/eventpulse-flask.git
cd eventpulse-flask
```

#### Install dependencies
```shell
pip install -r requirements.txt
```

#### Launch the application
```shell
python -m api.v1.app
```