# LatexToUnicode
The idea of this project is to have an app where you can type text with basic latex commands in it and encode it to unicode

# Requirements:
- I suggest you set up a python environment `python -m venv .venv` and activate it `source .venv/bin/activate` in Linux.
- Run `pip install -r requirements.txt`
- move to the project folder `cd latexToUnicode`
- Just in case make migrations. It shouldn't be an issue yet but anyways `python manage.py makemigrations` and then `python manage.py migrate`
- Start the server `python manage.py runserver`
- Now you should be able to see the basic app on `localhost:8000`

# Issues:
A lot. It's a work in progress, though the parser is able to manage nested parenthesis on substrings like 2^((3n-1)+(2n-4))+a_(2n-1)/a_(3(5n+1)) or such, it's still having issues with commands with nested operations. Also the greek alpha is just up to alpha, beta, gamma and delta in lowercase.

