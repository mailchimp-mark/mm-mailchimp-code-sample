# Mark's Mailchimp Code Sample

This is based off a project I did for another company I applied for. I adjusted it a bit to make it
my own and decided to re-use it as my code sample submission for MailChimp. It was fun and it's
recent work, so it felt like a good candidate for a code sample. Initially, I was going to snag some recent work from my current position, but felt uncomfortable about it and decided against it. Hopefully this is okay. If this doesn't feel appropriate, feel free to reach out and I'll see if I can write something new.

**Note**: It's very possible that submitting this full app is overkill. If this is more than what's needed, I have extracted the important parts and placed them in this [gist](https://gist.github.com/mailchimp-mark/045a77e00c6e00b26bc28fe5f15985b4).


### Requirements
The aim for this project was to create a list view for items. The items in this updated verison are Pokemon.

There were a few requirements:

- Pokemon must be fetched from an external api that adds new pokemon entries on a daily basis. The db
for the app must always be insync with the external api. One thing to note is there is no external api for this new version, so running this locally will not make scheduled calls to the external api. Instead I have created a fixture that'll get you setup with initial data. My tests mock the call, so they are the living proof that the functionality works in the presence of the correct external api.

- When visiting the page you should be able to "like" a Pokemon and the action should be remembered when you
visit the page again

- When visiting the page you should be able to see the aggregated "like" counts for each pokemon

![Alt text](pokemon_app/static/images/preview.png?raw=true "Title")


### Installing and Getting Started

In order to get this app running locally you will need to create a `virtualenv`, install dependencies, and run DB migrations, but before that you'll need to make sure you have `pip` and `virtualenv` installed.

You can install them with the following

```
sudo easy_install pip
sudo easy_install virtualenv # "pip install virtualenv" should work also
```

Once you have that worked out you can proceed with creating your `virtualenv`, installing dependencies, and running migrations

```
cd mm-mailchimp-code-sample/
virtualenv ve
. ve/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata pokemon.json #load initial data
```

After successfully running the previous commands, you will be able to kick start the app with

```
python manage.py runserver ## good starting point is http://127.0.0.1:8000/pokemon
```


### Testing

To run tests you run

```
python manage.py test pokemon_app/tests
```


Please feel free to reach out if you have any issues.


## Warning: the next parts are not relevant if you are running a local instance of this app. I'm leaving them here incase you are curious about the steps to sync the db with the external api

### Syncing DB with API
One important thing to note is that Pokemon objects, are created via a cron job
that makes calls to coolpokemon.com/pokemon/all and populates the
DB based on the items in the response, which means the page will be empty
until you start the cron job. You can kick off this process with the following command (make sure your dev server is up)

```
python manage.py crontab add # when you open a new terminal to run this make sure to execute ". ve/bin/activate" first
```

If you like would to see the active job you can run

```
python manage.py crontab show
```

If you would like to remove the job you can run
```
python manage.py crontab remove
```

This job will run every every minute, but it can be tuned to run less often in pokemon_proj/settings.py (see `CRONJOBS` setting).

### Troubleshooting

If for some reason django-crontab is giving you trouble, you can just invoke the call on your own by doing

```
python manage.py shell
```

Then in the Python intepreter you can run

```
from pokemon_app.cron import fetch_Pokemon_data
fetch_pokemon_data()
```
