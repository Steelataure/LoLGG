from django.shortcuts import render, redirect
from .forms import SummonerForm
import requests
import urllib.parse

def summoner_view(request):
    if request.method == 'POST':
        form = SummonerForm(request.POST)
        if form.is_valid():
            summoner_name = form.cleaned_data['summoner_name']
            
            # Check if summoner_name contains a '#'
            if '#' in summoner_name:
                summoner_name, tagline = summoner_name.split('#', 1)
                tagline = tagline.strip().lower()  # Ensure tagline is lowercase and trimmed
            else:
                tagline = 'euw'  # Default tagline
            
            api_key = 'RGAPI-4188386b-e8f0-41ba-b5fb-07c8aeb0aa7b'  # Your API key

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
                # Handle API errors
                # Redirect to home with error message
                return redirect('home')
            else:
                if response.status_code == 200:
                    summoner_data = response.json()
                    # Pass summoner_data via URL parameters to profile_view
                    return redirect('profile', summoner_puuid=summoner_data['puuid'], summoner_gameName=summoner_data['gameName'], summoner_tagLine=summoner_data['tagLine'])
                else:
                    # Handle summoner not found
                    # Redirect to home with error message
                    return redirect('home')
    else:
        form = SummonerForm()

    return render(request, 'lol_stats/summoner.html', {'form': form})

def profile_view(request, summoner_puuid, summoner_gameName, summoner_tagLine):
    summoner_data = {
        'puuid': summoner_puuid,
        'gameName': summoner_gameName,
        'tagLine': summoner_tagLine,
    }
    # Render profile.html with summoner_data
    return render(request, 'lol_stats/profile.html', {'summoner': summoner_data})
