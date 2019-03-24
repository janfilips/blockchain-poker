#!/usr/bin/env python3
import collections
import itertools
import random

SUIT_LIST = ("H", "S", "D", "C")
NUMERAL_LIST = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")

class card:

    def __init__(self, numeral, suit):
        self.numeral = numeral
        self.suit = suit
        self.card = self.numeral, self.suit

    def __repr__(self):
        return self.numeral + self.suit

class deck(set):

    def __init__(self):
        for numeral, suit in itertools.product(NUMERAL_LIST, SUIT_LIST):
            self.add(card(numeral, suit))

    def get_card(self):

        a_card = random.sample(self, 1)[0]
        self.remove(a_card)
        return a_card

    def evaluate_hand(self, cards_list):

        short_desc = "Nothing."
        numeral_dict = collections.defaultdict(int)
        suit_dict = collections.defaultdict(int)

        for my_card in cards_list:
            numeral_dict[my_card.numeral] += 1
            suit_dict[my_card.suit] += 1

        # Pair
        if len(numeral_dict) == 4:
            short_desc = "One-pair."
            if(numeral_dict['J']==2 or numeral_dict['Q']==2 or numeral_dict['K']==2 or numeral_dict['A']==2):
                short_desc = "Jacks-or-better."

        # Two pair or 3-of-a-kind
        elif len(numeral_dict) == 3:
            if 3 in numeral_dict.values():
                short_desc ="Three-of-a-kind."
            else:
                short_desc ="Two-pair."

        # Full house or 4-of-a-kind
        elif len(numeral_dict) == 2:
            if 2 in numeral_dict.values():
                short_desc ="Full-house."
            else:
                short_desc ="Four-of-a-kind."
        else:

            # Flushes and straights
            straight, flush = False, False
            if len(suit_dict) == 1:
                flush = True
            min_numeral = min([NUMERAL_LIST.index(x) for x in numeral_dict.keys()])
            max_numeral = max([NUMERAL_LIST.index(x) for x in numeral_dict.keys()])
            if int(max_numeral) - int(min_numeral) == 4:
                straight = True

            # Ace can be low
            low_straight = set(("A", "2", "3", "4", "5"))
            if not set(numeral_dict.keys()).difference(low_straight):
                straight = True
            if straight and not flush:
                short_desc = "Straight."
            elif flush and not straight:
                short_desc = "Flush."
            elif flush and straight:
                short_desc = "Straight-flush."
                if('A' in numeral_dict.keys() and 'K' in numeral_dict.keys()):
                    short_desc = "Royal-flush."

        return short_desc, numeral_dict, suit_dict

    def suggest_hand(self, player, hand, evaluated_hand, numeral_dict, suit_dict):

        sugested_hand = []

        if(evaluated_hand == "Full-house."):
            sugested_hand = hand
        if(evaluated_hand == "Straight."):
            sugested_hand = hand
        if(evaluated_hand == "Flush."):
            sugested_hand = hand
        if(evaluated_hand == "Straight-flush."):
            sugested_hand = hand
        if(evaluated_hand == "Royal-flush."):
            sugested_hand = hand

        if(evaluated_hand == "Three-of-a-kind."):
            for i in numeral_dict:
                if(numeral_dict[i] == 3):
                    for card in hand:
                        if(i in str(card)):
                            sugested_hand.append(card)

        if(evaluated_hand == "Four-of-a-kind."):
            for i in numeral_dict:
                if(numeral_dict[i] == 4):
                    for card in hand:
                        if(i in str(card)):
                            sugested_hand.append(card)

        # XXX TODO check if there is a chance for straight

        if not sugested_hand:
            for i in suit_dict:
                if(suit_dict[i]==4):
                    for card in hand:
                        if(i in str(card)):
                            sugested_hand.append(card)

        if not sugested_hand:
            if(evaluated_hand == "One-pair." or evaluated_hand == "Jacks-or-better." or evaluated_hand == "Two-pair."):
                for i in numeral_dict:
                    if(numeral_dict[i] == 2):
                        for card in hand:
                            if(i in str(card)):
                                sugested_hand.append(card)

        if not sugested_hand:
            for card in hand:
                if('J' in str(card)): sugested_hand.append(card)
                if('Q' in str(card)): sugested_hand.append(card)
                if('K' in str(card)): sugested_hand.append(card)
                if('A' in str(card)): sugested_hand.append(card)


        # player mini-bonus

        if(evaluated_hand == "Royal-flush."):
            mini_bonus = round(random.uniform(1.2,1.55),2)
            player.mini_bonus += mini_bonus
            print('mini-bonus royal-flush', mini_bonus)

        if(evaluated_hand == "Straight-flush."):
            mini_bonus = round(random.uniform(1.02,1.11),2)
            player.mini_bonus += mini_bonus
            print('mini-bonus straight-flush', mini_bonus)

        if(evaluated_hand == "Four-of-a-kind."):
            mini_bonus = round(random.uniform(0.62,0.69),2)
            player.mini_bonus += mini_bonus
            print('mini-bonus four-of-a-kind', mini_bonus)

        if(evaluated_hand == "Full-house."):
            mini_bonus = round(random.uniform(0.36,0.39),2)
            player.mini_bonus += mini_bonus
            print('mini-bonus fullhouse', mini_bonus)

        if(evaluated_hand == "Flush."):
            mini_bonus = round(random.uniform(0.29,0.33),2)
            player.mini_bonus += mini_bonus
            print('mini-bonus straight', mini_bonus)

        if(evaluated_hand == "Straight."):
            mini_bonus = round(random.uniform(0.20,0.25),2)
            player.mini_bonus += mini_bonus
            print('mini-bonus straight', mini_bonus)

        if(evaluated_hand == "Three-of-a-kind."):
            mini_bonus = round(random.uniform(0.11,0.14),2)
            player.mini_bonus += mini_bonus
            print('mini-bonus three-of-a-kind', mini_bonus)

        if(evaluated_hand == "Two-pair."):
            mini_bonus = round(random.uniform(0.07,0.09),2)
            player.mini_bonus += mini_bonus
            print('mini-bonus two-pair', mini_bonus)

        if(evaluated_hand == "Jacks-or-better."):
            mini_bonus = round(random.uniform(0.02,0.05),2)
            player.mini_bonus += mini_bonus
            print('mini-bonus jacks-or-better', mini_bonus)

        if(evaluated_hand == "One-pair."):
            mini_bonus = round(random.uniform(0.01,0.03),2)
            player.mini_bonus += mini_bonus
            print('mini-bonus one-pair', mini_bonus)

        if(evaluated_hand == "Nothing."):
            if(len(sugested_hand)==3):
                mini_bonus = 0.02
                player.mini_bonus += mini_bonus
                print('mini-bonus nothing 3 cards', mini_bonus)

        player.save()

        return sugested_hand



    def get_hand(self, number_of_cards=5):

        number_of_cards = 5
        cards_list = [self.get_card() for x in range(number_of_cards)]
        return cards_list

if __name__ == '__main__':
    for i in range(10000000):
        hand = deck().get_hand()
        evaluated_hand = deck().evaluate_hand(hand)
        print(hand, evaluated_hand)
