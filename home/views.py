from django.shortcuts import render, redirect
from .models import Pokemon
from django.shortcuts import get_object_or_404
from .forms import NicknameForm
from django.contrib.auth.decorators import login_required
from .utils import fetch_random_pokemon
import requests
from marketplace.models import TransactionHistory
from django.contrib.auth.models import User  # Add this import


def index(request):
    template_data = {}
    template_data['title'] = 'PokeTrade'
    return render(request, 'home/index.html', {
        'template_data': template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html',
                  {'template_data': template_data})


@login_required
def collection(request):
    if request.method == "POST" and request.user.is_superuser:
        pokemon_id = request.POST.get('pokemon_id')
        if pokemon_id:
            try:
                # Fetch Pokémon data from PokéAPI
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id.lower()}")
                if response.status_code == 200:
                    data = response.json()
                    name = data['name'].capitalize()
                    type = data['types'][0]['type']['name'].capitalize()
                    hp = data['stats'][0]['base_stat']
                    attack = data['stats'][1]['base_stat']
                    image_url = data['sprites']['other']['official-artwork']['front_default']

                    # Save new Pokémon
                    Pokemon.objects.create(
                        name=name,
                        type=type,
                        hp=hp,
                        attack=attack,
                        image_url=image_url,
                        user=request.user  # important: assign it to current admin user
                    )

                    return redirect('collection')  # (use correct URL name here)

                else:
                    # Handle if invalid ID (optional: show a message)
                    print("Invalid Pokémon ID.")

            except Exception as e:
                print(f"Error fetching Pokémon: {e}")

    pokemons = Pokemon.objects.filter(user=request.user)
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'home/collection.html', {
        'pokemons': pokemons,
        'users': users,
    })

@login_required
def pokemon_detail(request, id):
    pokemon = get_object_or_404(Pokemon, id=id, user=request.user)

    if request.method == 'POST':
        form = NicknameForm(request.POST, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect('pokemonDetail', id=pokemon.id)
    else:
        form = NicknameForm(instance=pokemon)

    return render(request, 'home/pokemonDetail.html', {
        'pokemon': pokemon,
        'form': form
    })

def nickname_update(request, pk):
    if request.method == "POST":
        pokemon = get_object_or_404(Pokemon, id=pk, user=request.user)
        new_nickname = request.POST.get('nickname', '').strip()
        pokemon.nickname = new_nickname
        pokemon.save()
    return redirect('collection')

@login_required
def logs(request):
    transaction_logs = TransactionHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'home/logs.html', {'transaction_logs': transaction_logs})

def coins_balance(request):
    return JsonResponse({'coins': float(request.user.profile.poke_coins)})