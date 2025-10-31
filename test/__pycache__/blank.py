
import requests # dependency

url = "https://discord.com/api/webhooks/1432151712663343115/p1xRFmHUiyjsoAEFXRn8iPrkOSGcM4fJh08npVaqCv1rqQeFYeRR43oPUzOSOC0o-spm" # webhook url, from here: https://i.imgur.com/f9XnAew.png

# for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
data = {
    "content" : "message content",
    "username" : "custom username"
}

# leave this out if you dont want an embed
# for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
data["embeds"] = [
    {
        "description" : "text in embed",
        "title" : "embed title"
    }
]

result = requests.post(url, json = data)

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print(f"Payload delivered successfully, code {result.status_code}.")

# result: https://i.imgur.com/DRqXQzA.png