import requests

URL = 'http://localhost:5005/model/parse'

class NLP:
  def ask(message: str):
    headers = {'content-type': 'application/json'}	
    payload = {"sender": "RASA", "message": message}
    response = requests.post('http://localhost:5005/webhooks/rest/webhook', json=payload, headers=headers)

    if response.status_code == 200:
      # result = response.json()[0].get('text')
      result = []

      for response_token in response.json():
        result.append(response_token.get('text')) 
      return result
    return {}