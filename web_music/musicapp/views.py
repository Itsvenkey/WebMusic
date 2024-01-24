# views.py

from django.shortcuts import render
import requests
from urllib.parse import parse_qs, unquote
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



def index(request):
    video_info = []

    if request.method == "POST":
        query = request.POST.get("query", "")

        if query:
            api_key = "AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30"
            client_name = "WEB_REMIX"
            client_version = "1.20220918"

            url = "https://music.youtube.com/youtubei/v1/search"

            headers = {
                "Content-Type": "application/json",
            }

            # JSON data to be included in the request body
            json_data = {
                "context": {
                    "client": {
                        "clientName": "WEB_REMIX",
                        "clientVersion": "1.20220918",
                    },
                    "request": {"useSsl": True},
                },
                 "query": query,
  "params": "EgWKAQIIAWoKEAkQBRAKEAMQBA%3D%3D",
  "searchEndpoint": {
    "query": query,
    "params": "EgWKAQIIAWoKEAkQBRAKEAMQBA%3D%3D",
    "musicSearchEndpoint": {
      "selectedTab": "SONGS",
      "params": "EgWKAQIIAWoKEAkQBRAKEAMQBA%3D%3D"
    }
  }
            }

            try:
                response = requests.post(
                    url, json=json_data, headers=headers, params={"key": api_key}
                )
                response.raise_for_status()

                data = response.json()
                if "contents" in data and "tabbedSearchResultsRenderer" in data["contents"]:
                    tabs = data["contents"]["tabbedSearchResultsRenderer"]["tabs"]

                    for tab in tabs:
                        if "musicShelfRenderer" in tab["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]:
                            music_shelf = tab["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["musicShelfRenderer"]

                            for item in music_shelf["contents"]:
                                if "musicResponsiveListItemRenderer" in item:
                                    music_item = item["musicResponsiveListItemRenderer"]
                                    title = music_item["flexColumns"][0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                                    video_id = music_item["flexColumns"][0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["navigationEndpoint"]["watchEndpoint"]["videoId"]
                                    music_type = music_item["flexColumns"][0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["navigationEndpoint"]["watchEndpoint"]["watchEndpointMusicSupportedConfigs"]["watchEndpointMusicConfig"]["musicVideoType"]
                                    if music_type == "MUSIC_VIDEO_TYPE_ATV":
                                        video_info.append({"title": title,"video_id":video_id})
                                                        
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data: {e}")

    return render(request, "musicapp/base.html", context={"video_info": video_info})



def play_song(request, video_id):
    format_data = []

    if video_id:
        api_key = "AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30"
        url = "https://music.youtube.com/youtubei/v1/player"

        headers = {
            "Content-Type": "application/json",
        }

        json_data = {
    "videoId": video_id,
    "context": {
        "client": {
            "clientName": "ANDROID_MUSIC",
            "clientVersion": "5.26.1",
            "platform": "DESKTOP",
            "playerType": "UNIPLAYER"
        }
    },
    "playbackContext": {
        "contentPlaybackContext": {
            "html5Preference": "HTML5_PREF_WANTS",
            "referer": "https://music.youtube.com/watch?v=ZIjVF7eNwm0"
        }
    },
    "parts": "player_response",
    "player_response": {
        "playbackContext": {
            "contentPlaybackContext": {
                "html5Preference": "HTML5_PREF_WANTS",
                "referer": "https://music.youtube.com/watch?v=ZIjVF7eNwm0"
            }
        }
    }
}


        try:
            response = requests.post(
                url, json=json_data, headers=headers, params={"key": api_key}
            )
            response.raise_for_status()

            data = response.json()
            print("Complete JSON response:")

            if "streamingData" in data:
                formats = data["streamingData"].get("adaptiveFormats", [])

                for format in formats:
                    itag = format.get("itag", None)
                    if itag is not None and itag == 251:
                        name = format.get("itag", "")
                        audio_url = format.get("url",'')
                        quality = format.get("quality", "")
                        format_data.append({"name": name, "url": audio_url, "quality": quality})

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
    return JsonResponse({"format_data": format_data})