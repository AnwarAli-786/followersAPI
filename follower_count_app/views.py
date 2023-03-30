# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class FollowerCountView(APIView):
    def get(self, request):
        instagram_username = request.query_params.get('insta')
        twitch_username = request.query_params.get('twitch')
        twitter_username = request.query_params.get('twitter')
        youtube_channel = request.query_params.get('youtube')
        
        results = {}
        
        if instagram_username:
            instagram_response = requests.get(f"https://www.instagram.com/{instagram_username}/?__a=1")
            if instagram_response.status_code == 200:
                instagram_data = instagram_response.json()['graphql']['user']
                results['instagram'] = instagram_data['edge_followed_by']['count']
                
        if twitch_username:
            twitch_response = requests.get(f"https://api.twitch.tv/helix/users?login={twitch_username}", headers={"Client-ID": "<your-twitch-client-id>"})
            if twitch_response.status_code == 200:
                twitch_data = twitch_response.json()['data']
                if len(twitch_data) > 0:
                    results['twitch'] = twitch_data[0]['follower_count']
                
        if twitter_username:
            twitter_response = requests.get(f"https://api.twitter.com/2/users/by/username/{twitter_username}", headers={"Authorization": "Bearer <your-twitter-bearer-token>"})
            if twitter_response.status_code == 200:
                twitter_data = twitter_response.json()['data']
                results['twitter'] = twitter_data['public_metrics']['followers_count']
                
        if youtube_channel:
            youtube_response = requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername={youtube_channel}&key=<your-youtube-api-key>")
            if youtube_response.status_code == 200:
                youtube_data = youtube_response.json()['items'][0]['statistics']
                results['youtube'] = youtube_data['subscriberCount']
                
        return Response(results)
