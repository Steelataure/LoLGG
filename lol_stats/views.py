import requests
from django.shortcuts import render
from .forms import SummonerForm
import urllib.parse

def summoner_view(request):
    data = None
    if request.method == 'POST':
        form = SummonerForm(request.POST)
        if form.is_valid():
            summoner_name = form.cleaned_data['summoner_name']
            tagline = 'euw'  # Correct tagline code
            api_key = 'RGAPI-6838818e-b2e3-45be-bfc3-5b58bc083b14'  # Your API key

            # URL encode the summoner name
            encoded_summoner_name = urllib.parse.quote(summoner_name)

            # Fetch summoner data from the League of Legends API
            url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encoded_summoner_name}/{tagline}?api_key={api_key}"
            headers = {
                'X-Riot-Token': api_key,
            }
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an HTTPError for bad responses
            except requests.exceptions.RequestException as e:
                if response.status_code == 401:
                    data = {'error': 'API key is unauthorized. Please check your API key and ensure it has the necessary permissions.'}
                elif response.status_code == 403:
                    data = {'error': 'API key is invalid or lacks necessary permissions. Please check your API key and permissions.'}
                elif response.status_code == 400:
                    data = {'error': 'Bad request. Please ensure the summoner name is correct.'}
                else:
                    data = {'error': f"Network error occurred: {e}"}
            else:
                if response.status_code == 200:
                    summoner_data = response.json()
                    data = {
                        'summoner': summoner_data,
                    }
                else:
                    data = {'error': f"Summoner not found. Status code: {response.status_code}"}
    else:
        form = SummonerForm()

    return render(request, 'lol_stats/summoner.html', {'form': form, 'data': data})
