from django.shortcuts import render, redirect
from .models import Pokemon
from django.shortcuts import get_object_or_404
from .forms import NicknameForm
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

def collection(request):
    pokemons = Pokemon.objects.all()
    return render(request, 'home/collection.html', {
        'pokemons': pokemons,
        'title': 'Collection'})

def pokemon_detail(request, id):
    pokemon = get_object_or_404(Pokemon, id=id)

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