**Metaprogramming**

About the project:

---

## Requirements
- Add virtual environment to be able to run app and run tests

---

## How to create virtual environment
- Check if you have pip installed, by running `which pip3`. If you get an error "pip command not found", use the following command to install pip:
`sudo easy_install pip`

- Check if you have virtualenv installed , by running `which virtualenv`. If you get an error "virtualenv command not found", enter this command into terminal:
`sudo pip3 install virtualenv`

## Start virtualenv
- To create a new virtualenv, enter command:
`virtualenv env`

- To activate virtualenv, enter command:
`source env/bin/activate`

- To deactivate virtualenv, enter command:
`deactivate`

## Run tests
- Activate virtualenv
- Go into `metaprogramming` folder
- Run `python3 app/tests.py` 
