from django.shortcuts import render, redirect, get_object_or_404
from .models import MarketplaceListing, TransactionHistory
from home.models import Pokemon
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required
def marketplace_home(request):
    listings = MarketplaceListing.objects.filter(is_active=True).exclude(seller=request.user)
    return render(request, 'marketplace/marketplace_home.html', {'listings': listings})


@login_required
def marketplace_listing_detail(request, listing_id):
    listing = get_object_or_404(MarketplaceListing, id=listing_id, is_active=True)
    return render(request, 'marketplace/listing_detail.html', {'listing': listing})


@login_required
def buy_pokemon(request, listing_id):
    listing = get_object_or_404(MarketplaceListing, id=listing_id, is_active=True)

    if request.method == 'POST':
        # Transfer ownership
        pokemon = listing.pokemon
        pokemon.user = request.user
        pokemon.save()
        messages.success(request, f"Congratulations! You successfully bought {pokemon.name}!")

        # Mark the listing as inactive
        listing.is_active = False
        listing.save()

        # Create a TransactionHistory object if you are tracking purchases
        TransactionHistory.objects.create(
            user=request.user,
            pokemon=pokemon,
            price=listing.price,
            transaction_type="buy"
        )

        return redirect('marketplace_home')

    return redirect('marketplace_home')

@login_required
def create_listing(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id, user=request.user)

    if request.method == 'POST':
        price = request.POST.get('price')
        if price:
            MarketplaceListing.objects.create(
                seller=request.user,
                pokemon=pokemon,
                price=price,
                is_active=True,
            )
            return redirect('marketplace_home')

    return render(request, 'marketplace/create_listing.html', {'pokemon': pokemon})