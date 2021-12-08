import os
from requests_oauthlib.oauth1_session import OAuth1Session

def fetchKeys():
  
  consumer_key = os.environ.get("CONSUMER_KEY")
  consumer_secret = os.environ.get("CONSUMER_SECRET")

  # You can adjust ids to include a single Tweets
  # Or you can add to up to 100 comma-separated IDs
  # Tweet fields are adjustable.
  # Options include:
  # attachments, author_id, context_annotations,
  # conversation_id, created_at, entities, geo, id,
  # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
  # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
  # source, text, and withheld

  request_token_url = "https://api.twitter.com/oauth/request_token"
  oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

  try:
      fetch_response = oauth.fetch_request_token(request_token_url)
  except ValueError:
      print(
          "There may have been an issue with the consumer_key or consumer_secret you entered."
      )

  resource_owner_key = fetch_response.get("oauth_token")
  resource_owner_secret = fetch_response.get("oauth_token_secret")
  print("Got OAuth token: %s" % resource_owner_key)

  # Get authorization
  base_authorization_url = "https://api.twitter.com/oauth2/token"
  authorization_url = oauth.authorization_url(base_authorization_url)

  base_authorization_url = "https://api.twitter.com/oauth/authorize"
  authorization_url = oauth.authorization_url(base_authorization_url)
  print("Please go here and authorize: %s" % authorization_url)
  verifier = input("Paste the PIN here: ")

  # Get the access token
  access_token_url = "https://api.twitter.com/oauth/access_token"
  oauth = OAuth1Session(
      consumer_key,
      client_secret=consumer_secret,
      resource_owner_key=resource_owner_key,
      resource_owner_secret=resource_owner_secret,
      verifier=verifier,
  )
  oauth_tokens = oauth.fetch_access_token(access_token_url)
  print(oauth_tokens)


  access_token = oauth_tokens["oauth_token"]
  access_token_secret = oauth_tokens["oauth_token_secret"]
  
  return oauth_tokens