import requests, json, random, m3u8

def get_token_and_signature(channel):
	url = TOKEN_API.format(channel=channel)
	r = requests.get(url)
	data = json.loads(r.text)
	sig = data['sig']
	token = data['token']
	return token, sig

vod = '272439809' # VoD ID
channel = 'olyashaa' # twitch.tv/olyashaa
ran = random.randint(0,1E7) # random number 1-99999
client_id = '4zswqk0crwt2wy4b76aaltk2z02m67' # your client-id

TOKEN_API = 'https://api.twitch.tv/api/vods/'+vod+'/access_token?client_id=' + client_id # Here we get "token" and "sig" keys for next API call
token, sig = get_token_and_signature(TOKEN_API)
USHER_API = 'https://usher.twitch.tv/vod/{vodid}?player=twitchweb' +\
    '&nauth={token}&nauthsig={sig}&$allow_audio_only=true&allow_source=true' + \
    '&type=any&p={random}' # VoD ID, token and sig we got before and random number from 1 to 99999

r = requests.get(USHER_API.format(vodid=vod, token=token, sig=sig, random=ran), verify=False) # Do not verify SSL certificate, looks like it has been expired
print(r.text)