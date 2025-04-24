from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TradeOffer
from home.models import Pokemon
from django.contrib.auth.models import User

@login_required
def create_trade(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        sender_pokemon_ids = request.POST.getlist('sender_pokemon')
        receiver_pokemon_ids = request.POST.getlist('receiver_pokemon')
        
        if not sender_pokemon_ids or not receiver_pokemon_ids:
            messages.error(request, 'Please select at least one Pokémon from each side.')
            return redirect('create_trade', user_id=user_id)

        trade = TradeOffer.objects.create(
            sender=request.user,
            receiver=receiver
        )
        trade.sender_pokemon.set(Pokemon.objects.filter(id__in=sender_pokemon_ids))
        trade.receiver_pokemon.set(Pokemon.objects.filter(id__in=receiver_pokemon_ids))
        messages.success(request, 'Trade offer sent successfully!')
        return redirect('trade_home')

    # Changed from 'owner' to 'user'
    sender_pokemon = Pokemon.objects.filter(user=request.user)
    receiver_pokemon = Pokemon.objects.filter(user=receiver)
    
    return render(request, 'trades/create_trade.html', {
        'receiver': receiver,
        'sender_pokemon': sender_pokemon,
        'receiver_pokemon': receiver_pokemon
    })


@login_required
def trade_home(request):
    # Get trades where the current user is the receiver
    received_trades = TradeOffer.objects.filter(receiver=request.user)

    # Get trades where the current user is the sender
    sent_trades = TradeOffer.objects.filter(sender=request.user)

    return render(request, 'trades/trade_home.html', {
        'received_trades': received_trades,
        'sent_trades': sent_trades
    })


@login_required
def respond_to_trade(request, trade_id):
    trade = get_object_or_404(TradeOffer, id=trade_id, receiver=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'accept':
            trade.status = 'ACCEPTED'
            # Handle the pokemon exchange
            for pokemon in trade.sender_pokemon.all():
                pokemon.user = trade.receiver
                pokemon.save()
            for pokemon in trade.receiver_pokemon.all():
                pokemon.user = trade.sender
                pokemon.save()
        elif action == 'decline':
            trade.status = 'DECLINED'

        trade.save()
        messages.success(request, f'Trade {trade.status.lower()}!')

    return redirect('trade_home')


@login_required
def cancel_trade(request, trade_id):
    trade = get_object_or_404(TradeOffer, id=trade_id, sender=request.user, status='PENDING')

    if request.method == 'POST':
        trade.status = 'CANCELLED'
        trade.save()
        messages.success(request, 'Trade cancelled successfully!')

    return redirect('trade_home')