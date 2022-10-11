from googleapiclient.discovery import build
def youtube_video_data(keyword):
    api_key="AIzaSyCpMiMvEOY4BmW4pUQ6kfT1xqj3kNeN4QQ"

    youtube=build("youtube","v3",developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        order="date",
        q=keyword,
        type="video",
        maxResults=50
        )
    response = request.execute()
    videoId = []
    title = []
    date = []
    for i in range(50):
        videoId.append(response['items'][i]['id']['videoId'])
        title.append(response['items'][i]['snippet']['title'])
        date.append(response['items'][i]['snippet']['publishedAt'].replace("T"," ").replace("Z"," "))
    return [videoId, title, date]

# for i in range(100):
#     print(i+1)
#     print(youtube_video_data('news'))
# print(youtube_video_data('updates'))
