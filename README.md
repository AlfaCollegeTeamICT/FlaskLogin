# Basic FLASK application for authentication demonstrations
> Hoite Prins - Alfa-college Boumaboulevard

Authentication with a database using LoginManager() in Flask.

**Functionality**
- Register
- Log in
- Log out
- Protected pages

# Installation
To install the application, use the following commands:

1. Clone repo && change folder
```shell
git clone https://github.com/AlfaCollegeTeamICT/FlaskLogin
cd FlaskLogin
```

2. Create virtual env && install dependencies
```shell
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

3. Create DB
```shell
touch database.db
python3

# In python shell:
>>> from app import db
>>> db.create_all()
```

4. Start application
```shell
python3 app.py
```

The application should now run on http://127.0.0.1:5000