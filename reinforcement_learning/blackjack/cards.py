#!/usr/bin/env python

import numpy as np
import random


def get_color_from_suits(suit):

    if suit in ["C", "S"]:
        return "black"
    elif suit in ["D", "H"]:
        return "red"
    else:
        raise Exception("Unknown suit.")




class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.color = get_color_from_suits(suit)
        self.repr = self.suit+self.rank

    def __repr__(self):
        return self.repr

    def __str__(self):
        return self.repr
        

class Deck:
    
    def __init__(self):
        self.cards = []
        
    def draw_random_card(self):
        drawn_card = np.random.choice(self.cards)
        self.cards.remove(drawn_card)
        return drawn_card
        
    def draw_top_card(self):
        top_card = self.cards.pop(len(self.cards)-1)
        return top_card

    def append_card(self, card):
        self.cards.append(card)

    def add_cards(self, cards_to_be_added):
        self.cards = self.cards + cards_to_be_added

    def insert_card_randomly(self, card):
        random_index = random.randint(0, len(cards)-1)
        self.cards.insert(random_index, card)

    def shuffle(self):
        random.shuffle(self.cards)

    def __repr__(self):
        return str(self.cards)

    def __str__(self):
        return self.cards

    def __add__(self, deck_to_be_added):
        return self.cards + deck_to_be_added.cards


class FrenchDeck(Deck):

    def __init__(self):
        super().__init__()

        suits = ["C", "S", "D", "H"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        for suit in suits:
            for rank in ranks:
                c = Card(suit, rank)
                self.append_card(c)
        

class Hand(Deck):

    def __init__(self):
        super().__init__()


def rank_counts(hand):

    rank_count = {}

    for card in hand.cards:
        if card.rank in rank_count:
            rank_count[card.rank] += 1
        else:
            rank_count[card.rank] = 1

    return rank_count


#def check_for_row(hand):
#     
