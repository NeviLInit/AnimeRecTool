import requests

BASE_URL = 'https://api.myanimelist.net/v2'
API_KEY = 'fe8074c87d075333b2d8f3d9a3d7d7c7'


def main():
    anime_name = input("Enter the name of the anime: ").strip().lower()
    anime_info_list = get_anime_info_by_name(anime_name)

    complete_genre_set = set()
    if anime_info_list:
        for anime_info in anime_info_list:
            anime_id = anime_info['node']['id']
            genres_list = get_anime_genres(anime_id)
            complete_genre_set.update(genres_list)
    else:
        print(f"Anime with name '{anime_name}' not found.")
        return

    complete_genre_list = [genre for genre in complete_genre_set]

    print(f"Genres of '{anime_name}':", complete_genre_list)

    # Find similar anime based on title
    similar_anime = find_similar_anime_by_title(anime_name)
    if similar_anime:
        print("Similar anime based on title:")
        for anime in similar_anime:
            print("-", anime)
    else:
        print("No similar anime found.")


def get_anime_info_by_name(anime_name):
    url = f'{BASE_URL}/anime'
    params = {
        'q': anime_name,
        'fields': 'node_id,title'
    }
    headers = {
        'X-MAL-CLIENT-ID': API_KEY
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        anime_data = response.json()['data']
        return anime_data
    else:
        return f'Error {response.status_code}: Unable to fetch anime data.'


def get_anime_genres(anime_id):
    url = f'{BASE_URL}/anime/{anime_id}'
    params = {
        'fields': 'genres'
    }
    headers = {
        'X-MAL-CLIENT-ID': API_KEY
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        anime_info = response.json()
        genres_data = anime_info.get('genres', [])
        genres_list = [genre['name'] for genre in genres_data]
        return genres_list
    else:
        return None


def find_similar_anime_by_title(anime_name):
    url = f'{BASE_URL}/anime'
    params = {
        'q': anime_name,
        'fields': 'title',
        'limit': 5
    }
    headers = {
        'X-MAL-CLIENT-ID': API_KEY
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        anime_data = response.json()['data']
        similar_anime_titles = [anime['node']['title'] for anime in anime_data if anime['node']['title'] != anime_name]
        return similar_anime_titles
    else:
        return None


if __name__ == "__main__":
    main()
