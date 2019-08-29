## About
Python lambda function that uses the Twitter Search API to get the 500 most recent tweets for a given query, and returns a list of tokens---after removing punctuation, stopwords and the query itself.

## Local development
1. Create virtual environment with virtualenvwrapper (I use it's postactivate script to create env vars so don't know how to do it with another venv manager like pipenv)
2. Install requirements  with `pip install -r requirements.txt`
3. edit the postactivate script, to add the 4 secret keys you got from the [twitter developer site](https://developer.twitter.com/en/apps) for your app. Mine is in `~/.Envs/pylambda/bin/postactivate` (I named my venv `pylambda` and configured virtualenvwrapper to dump environments in `~/.Envs`) and looks something like this:

```bash
#!/bin/bash
# This hook is sourced after this virtualenv is activated.
export CONSUMER_KEY=REPLACE-ME
export CONSUMER_SECRET=REPLACE-ME
export ACCESS_TOKEN=REPLACE-ME
export ACCESS_TOKEN_SECRET=REPLACE-ME
```
4. Run `lambda invoke -v` to run in the local environment (using the `events.json` file) and `lambda deploy` to deploy to AWS
