from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TradeListing, ListingOffer
from home.models import Pokemon
from django.contrib.auth.models import User
from marketplace.models import TransactionHistory


@login_required
def trade_center_home(request):
    trade_listings = TradeListing.objects.all()
    return render(request, 'trades/trade_center_home.html', {'trade_listings': trade_listings})

@login_required
def list_pokemon_for_trade(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id, user=request.user)

    # Check if already listed
    if TradeListing.objects.filter(pokemon=pokemon).exists():
        messages.error(request, "This Pokémon is already listed for trade.")
        return redirect('collection')

    TradeListing.objects.create(user=request.user, pokemon=pokemon)
    messages.success(request, f"{pokemon.name} has been listed for trade!")
    return redirect('trade_center_home')

@login_required
def make_trade_offer(request, listing_id):
    listing = get_object_or_404(TradeListing, id=listing_id)

    if listing.user == request.user:
        messages.error(request, "You cannot offer on your own listing.")
        return redirect('trade_center_home')

    if request.method == 'POST':
        offered_pokemon_id = request.POST.get('offered_pokemon')
        if not offered_pokemon_id:
            messages.error(request, 'Please select one of your Pokémon to offer.')
            return redirect('make_trade_offer', listing_id=listing.id)

        offered_pokemon = get_object_or_404(Pokemon, id=offered_pokemon_id, user=request.user)

        ListingOffer.objects.create(
            listing=listing,
            sender=request.user,
            offered_pokemon=offered_pokemon
        )
        messages.success(request, "Offer submitted successfully!")
        return redirect('trade_center_home')

    user_pokemon = Pokemon.objects.filter(user=request.user)
    return render(request, 'trades/make_trade_offer.html', {
        'listing': listing,
        'user_pokemon': user_pokemon
    })

@login_required
def my_listings_offers(request):
    listings = TradeListing.objects.filter(user=request.user)
    return render(request, 'trades/my_listings_offers.html', {'listings': listings})

@login_required
def respond_to_listing_offer(request, offer_id):
    offer = get_object_or_404(ListingOffer, id=offer_id)

    if offer.listing.user != request.user:
        messages.error(request, "You can only respond to offers on your own listings.")
        return redirect('my_listings_offers')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            offer.status = 'ACCEPTED'
            offer.save()

            # Swap ownership
            offered_pokemon = offer.offered_pokemon
            target_pokemon = offer.listing.pokemon

            original_owner = target_pokemon.user
            offer_sender = offered_pokemon.user

            # Swap the owners
            offered_pokemon.user, target_pokemon.user = target_pokemon.user, offered_pokemon.user
            offered_pokemon.save()
            target_pokemon.save()

            # Create TransactionHistory logs
            TransactionHistory.objects.create(
                user=offer_sender,
                pokemon=target_pokemon,
                price=0,
                transaction_type='trade',
                other_party=original_owner
            )

            TransactionHistory.objects.create(
                user=original_owner,
                pokemon=offered_pokemon,
                price=0,
                transaction_type='trade',
                other_party=offer_sender
            )

            # ❗ First decline other offers BEFORE deleting listing
            ListingOffer.objects.filter(listing=offer.listing).exclude(id=offer.id).update(status='DECLINED')

            # Now delete the listing
            offer.listing.delete()

            messages.success(request, "Offer accepted! Pokémon have been swapped and logged.")
            return redirect('my_listings_offers')

        elif action == 'decline':
            offer.status = 'DECLINED'
            offer.save()
            messages.success(request, "Offer declined.")
            return redirect('my_listings_offers')

    return render(request, 'trades/respond_offer.html', {'offer': offer})