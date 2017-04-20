# Urban Forest Recommender
This project is a San Francisco tree recommendation website. Trees are recommended for any location in the city based on the health of the surrounding trees. Tree health data is from the 2016 census and can be found in `assets/data/trees.csv`. In addition to recommending based on tree health, we only recommend trees that the city allows to be planted.

The website can be found live at: https://sf-urban-forest-recommender.herokuapp.com/

What remains to be done:
- Make it look nicer
- Potentially integrate with the [Friends of the Urban Forest website](www.fuf.net/resources-reference/urban-tree-species-directory/)

# Install Locally

1. `virtaulenv venv`
1. `source venv/bin/activate`
1. `pip install -r requirements.txt`

# How to Run Locally

- Run `env FLASK_APP=app.py flask run`

# How to Deploy

- Hosted on Heroku
- Push to `deployment` branch to deploy:
  1. `git checkout deployment`
  1. `git rebase master`
  1. `git push`

