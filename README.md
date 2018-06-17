# twitch-vod-to-m3u8
Extract m3u8 playlist from Twitch VoD

## API Calls

**Retrieve an access token for a specific HLS VOD**  
[https://api.twitch.tv/api/vods/{vod_id}/access_token?client_id={client_id}](https://api.twitch.tv/api/vods/{vod_id}/access_token?client_id={client_id})

The {vodId} should be the ID without the prefix letter, so 'v1234567' becomes '1234567'

Result
```
{
"token": "{\"user_id\":xxxxxxxx,\"vod_id\":xxxxxxx,\"expires\":xxxxxxxxxx,\"chansub\":{\"restricted_bitrates\":[]},\"privi leged\":false}",
"sig":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```
The `token` and `sig` values can be put straight into the next API call.

**Retrieve M3U8 file containing the qualities and respective links**  
[https://usher.twitch.tv/vod/{vodid}?player=twitchweb&nauth={token}&nauthsig={sig}&$allow_audio_only=true&allow_source=true&type=any&p={random}](https://usher.twitch.tv/vod/{vodid}?player=twitchweb&nauth={token}&nauthsig={sig}&$allow_audio_only=true&allow_source=true&type=any&p={random})

Where the `{vodId}`, `{sig}` and `{token}` are the vod id and the exact values you obtained from the previous API call.

Result
A file looking something like
```
#EXTM3U
#EXT-X-TWITCH-INFO:ORIGIN="s3",REGION="EU",USER-IP="94.103.236.38",SERVING-ID="f6f8cef976cb48bfac86fcf4153c63cf",CLUSTER="akamai_vod",MANIFEST-CLUSTER="akamai_vod"
#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="chunked",NAME="1080p60",AUTOSELECT=YES,DEFAULT=YES
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3769268,CODECS="avc1.64002A,mp4a.40.2",RESOLUTION="1920x1080",VIDEO="chunked"
https://vod020-ttvnw.akamaized.net/554dbf248c4e864da1fd_olyashaa_29063373520_885131008/chunked/index-muted-F7HL7XENLI.m3u8
#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="720p60",NAME="720p60",AUTOSELECT=YES,DEFAULT=YES
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3186613,CODECS="avc1.4D401F,mp4a.40.2",RESOLUTION="1280x720",VIDEO="720p60"
https://vod020-ttvnw.akamaized.net/554dbf248c4e864da1fd_olyashaa_29063373520_885131008/720p60/index-muted-F7HL7XENLI.m3u8
#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="720p30",NAME="720p",AUTOSELECT=YES,DEFAULT=YES
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2317851,CODECS="avc1.4D401F,mp4a.40.2",RESOLUTION="1280x720",VIDEO="720p30"
https://vod020-ttvnw.akamaized.net/554dbf248c4e864da1fd_olyashaa_29063373520_885131008/720p30/index-muted-F7HL7XENLI.m3u8
#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="480p30",NAME="480p30",AUTOSELECT=YES,DEFAULT=YES
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1411525,CODECS="avc1.4D401E,mp4a.40.2",RESOLUTION="852x480",VIDEO="480p30"
https://vod020-ttvnw.akamaized.net/554dbf248c4e864da1fd_olyashaa_29063373520_885131008/480p30/index-muted-F7HL7XENLI.m3u8
#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="360p30",NAME="360p",AUTOSELECT=YES,DEFAULT=YES
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=666597,CODECS="avc1.4D401E,mp4a.40.2",RESOLUTION="640x360",VIDEO="360p30"
https://vod020-ttvnw.akamaized.net/554dbf248c4e864da1fd_olyashaa_29063373520_885131008/360p30/index-muted-F7HL7XENLI.m3u8
#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="160p30",NAME="160p",AUTOSELECT=YES,DEFAULT=YES
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=258444,CODECS="avc1.4D400C,mp4a.40.2",RESOLUTION="284x160",VIDEO="160p30"
https://vod020-ttvnw.akamaized.net/554dbf248c4e864da1fd_olyashaa_29063373520_885131008/160p30/index-muted-F7HL7XENLI.m3u8
```

## FFMPEG
It's worth noting that the FFMPEG command line program is able to take a M3U8 file as a value for its input (-i) parameter, which will automatically download and concatenate the pieces together if, for example, run like this

`ffmpeg -i "https://vod020-ttvnw.akamaized.net/554dbf248c4e864da1fd_olyashaa_29063373520_885131008/chunked/index-muted-F7HL7XENLI.m3u8" -bsf:a aac_adtstoasc -c copy output.mp4`