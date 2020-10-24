# CS235Flix Web Application

## Description
A Web application that demonstrates use of Python's Flask framework. 
The application makes use of libraries such as the Jinja templating library and WTForms. 
Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. 
The application uses Flask Blueprints to maintain a separation of concerns between application functions. 
Testing includes unit and end-to-end testing using the pytest tool. 

## Installation

**Installation via requirements.txt**

From directory *CS235FlixSkeleton-Extensions*:

```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

**Setting DATA_PATH variable**

The Python script *CS235FlixSkeleton-Extensions/cs235flix/adapters/memory_repository.py* script defines a variable
named DATA_PATH. Before running the Web application or running tests, DATA_PATH must be set to the absolute path of
the *CS235FlixSkeleton-Extensions/data* directory.

E.g. 

`DATA_PATH = os.path.join('C:', os.sep, 'Users', 'Sanjeev Toora', 'Desktop', 'Srishti new',
                         'srishti-cs230', 'CS235FlixSkeleton-Extensions', 'data')`

assigns DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

`C:\Users\Sanjeev Toora\Desktop\Srishti new\srishti-cs230\CS235FlixSkeleton-Extensions\data`

## Running the Webapp

From directory *CS235FlixSkeleton-Extensions*:

```shell
$ set PYTHONPATH=C:\Users\Sanjeev Toora\Desktop\Srishti new\srishti-cs230\CS235FlixSkeleton-Extensions
$ flask run
````

The *PYTHONPATH* value above should be changed to the absolute path of the *CS235FlixSkeleton-Extensions* directory.