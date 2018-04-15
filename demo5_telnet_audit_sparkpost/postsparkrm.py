import requests


def post_message(token, message, room_id):

    url = "https://api.ciscospark.com/v1/messages"

    payload = {'roomId': room_id,
               'text': message
              }

    headers = {
        'authorization': "Bearer " + token,
        'content-type': "application/json"
         }

    requests.request("POST", url, json=payload, headers=headers)
