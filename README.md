# TIZWA_Website

## Environment settings

### Virtual Environment

We use Python virtual environment.

First, **install** virtual environment using

```shell
sudo apt install python3-venv
```

In order to **create** a virtual environment, run

```shell
python3 -m venv .env 
```

this will create a virtual environment, called **.env**, that you can activate using

```shell
source .env/bin/activate
```

### install dependencies

you should install the requirements file, using

```shell
pip3 install -r requirements.txt
```

### adding new dependencies

whenever you add a new third party library to our project, you need freeze the environment and update the requirements file. This can be done using the following command:

```shell
pip3 freeze > requirements.txt
```

it will generate a requirements file from freezed environment


## Start from scratch

the script **src/start_from_scratch.sh** has been created to allow you having an empty project, by cleaning all the migrations files, database, etc then populating the db from the **data** directory, which turns out to be very usefull whenever you want to clean the database and testing your code.

You can make it executable, using chmod 

```shell
chmod +rx src/start_from_scratch.sh
```

now you can execute it from the home directory using

```shell
src/start_from_scratch.sh
```

or from the **src** directory using

```shell
./start_from_scratch.sh
```

## Running the project

As usual with Django projects, just run the following command from the **src** directory

```shell
python3 manage.py runserver
```

The migrations are done by the **start_from_scratch** script. However, if you are modifying models, you may need to run the usual commands **makemigrations**, **migrate** and **collectstatic**. 

## Good practices

TODO

