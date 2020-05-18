#!/usr/bin/env python3
"""
import random

__author__ = "shawnxhong"

class Deck(object):
    """
    A collection of ordered cards.
    """
    def __init__(self, starting_cards=None):
        """
        Construct a deck. The default starting cards is empty. When provided with starting cards, it is constructed with
        a list of the starting cards.
        Parameters:
            starting_cards (List<Card>): The list of starting cards.
        """
        if starting_cards is None:
            self._deck = []
        else:
            self._deck = starting_cards

    def get_cards(self):
        """
        Returns a list of cards in the deck
        """
        return self._deck

    def get_card(self, slot):
        """
        Return the card at the specified slot in a deck.
        Parameter:
            slot (int): The specified slot in a deck.
        """
        return self._deck[slot]

    def top(self):
        """
        Returns the card on the top of the deck, i.e. the last added.
        """
        return self._deck[-1]

    def remove_card(self, slot):
        """
        Removes a card at the given slot in a deck.
        Parameter:
            slot (int): The specified slot in a deck.
        """
        self._deck.pop(slot)

    def get_amount(self) -> int:
        """
        Returns the amount of cards in a deck.
        """
        return len(self.get_cards())

    def shuffle(self):
        """
        Shuffles the order of the cards in the deck.
        """
        random.shuffle(self._deck)

    def pick(self, amount: int = 1):
        """
        Takes the first 'amount' of cards off the deck and returns them.
        Parameter:
            amount (int): The amount of cards to be taken off.
        """
        picked_cards = []
        while amount > 0:
            picked_cards.append(self._deck[-1])
            self._deck.pop()
            amount -= 1
        return picked_cards

    def add_card(self, card):
        """
        Places a card on top of the deck.
        Parameter:
            card (Card): the card to be placed on top of the deck
        """
        self._deck.append(card)

    def add_cards(self, cards):
        """
        Places a list of cards on top of the deck.
        Parameter:
            cards (List[Card]): a list of cards.
        """
        self._deck.extend(cards)

    def copy(self, other_deck):
        """Copies all of the cards from the other_deck into the current deck
        extending the list of cards of the current deck.
        Parameter:
            other_deck (Deck): an other deck to be copied from.
        """
        self.add_cards(other_deck.get_cards())

    def __str__(self) -> str:
        """
        Returns the string representation of the deck
        """
        return "Deck({0})".format(', '.join(str(card) for card in self.get_cards()))

    def __repr__(self):
        """
        Returns the string representation of the deck
        """
        return "Deck({0})".format(', '.join(str(card) for card in self.get_cards()))


class Player(object):
    """
    A player represents one of the players in the game
    """

    def __init__(self, name: str):
        """
        Construct the player's name,an empty deck of cards on the hands and an empty deck of collected coder cards.
        Parameter:
            name (str): the player's name.
        """
        self._name = name
        self.hand = Deck()
        self.coders = Deck()

    def get_name(self) -> str:
        """
        Returns the name of the player.
        """
        return self._name

    def get_hand(self) -> Deck:
        """
        Returns the player's deck of cards
        """
        return self.hand

    def get_coders(self) -> Deck:
        """
        Returns the player's deck of collected coder cards.
        """
        return self.coders

    def has_won(self) -> bool:
        """
        Returns True iff the player has 4 or more coders.
        """
        if self.get_coders().get_amount() >= 4:
            return True
        else:
            return False

    def __str__(self):
        """
        Returns the string representation of the player, the cards in hands and coder cards in hands.
        """
        return "Player({0}, {1}, {2})".format(self.get_name(), self.get_hand(), self.get_coders())

    def __repr__(self):
        """
        Returns the string representation of the player, the cards in hands and coder cards in hands.
        """
        return "Player({0}, {1}, {2})".format(self.get_name(), self.get_hand(), self.get_coders())


class Card(object):
    """
    A card represents a card in the game.
    """

    def play(self, player, game):
        """
        Called when a player plays a card.
        Parameters:
            player (Player): the current player
            game (a2_support.CodersGame): the game of sleeping coders.
        """
        player.get_hand().get_cards().remove(self)  # remove the card from the player's hand
        player.get_hand().get_cards().extend(game.pick_card())  # pickup a new card from the pickup pile in the game
        game.set_action("NO_ACTION")  # set the action that needs to be performed, generally "NO ACTION"

    def action(self, player: Player, game, slot: int):
        """
        Called when an action of a special card is performed
        Parameter:
            player (Player): the current player
            game (a2_support.CodersGame): the game of sleeping coders.
            slot (int): the of this card
        """
        pass  # it should be overridden by the children subclasses.

    def __str__(self) -> str:
        """
        Returns the string representation of the card
        """
        return "Card()"

    def __repr__(self):
        """
        Returns the string representation of the card
        """
        return "Card()"


class NumberCard(Card):
    """
    A card whose aim is to be disposed of by the player.
    """
    def __init__(self, number: int):
        """
        Construct the number value of the number card。
        """
        self._number = number

    def get_number(self):
        """
        Return the number value of the number card.
        """
        return self._number

    def play(self, player, game):
        """
        The game move on to the next player's turn when a number card is played
        Parameter:
            player (Player): the current player
            game (a2_support.CodersGame): the game of sleeping coders.
        """
        super().play(player, game)
        game.next_player()

    def action(self, player: Player, game, slot):
        """
        No special action required for number cards.
        Parameter:
            player (Player): the current player
            game (a2_support.CodersGame): the game of sleeping coders.
            slot (int): the slot of this card in the deck
        """
        pass

    def __str__(self):
        """
        Returns the string representation of the number card with the number value
        """
        return "NumberCard({0})".format(self._number)

    def __repr__(self):
        """
        Returns the string representation of the number card with the number value
        """
        return "NumberCard({0})".format(self._number)


class TutorCard(Card):
    """
    A tutor card can be played by a player to pickup a coder card.
    """
    def __init__(self, name):
        """
        Construct the name of the tutor card.
        """
        self._name = name

    def get_name(self):
        """
        Return the name of the tutor card.
        """
        return self._name

    def play(self, player, game):
        """
        Set the game's action as 'PICKUP_CODER'.
        Parameter:
            player (Player): the current player
            game (a2_support.CodersGame): the game of sleeping coders.
        """
        super().play(player, game)
        game.set_action("PICKUP_CODER")

    def action(self, player, game, slot):
        """
        Take the coder card from the slot to the player's deck. Set the action to "NO_ACTION" and move on.
        Parameter:
            player (Player): the current player
            game (a2_support.CodersGame): the game of sleeping coders.
            slot (int): the slot of coder card
        """
        coder_card = game.get_sleeping_coder(slot)  # select the coder card
        player.get_coders().add_card(coder_card)  # added to the player's deck
        game.set_sleeping_coder(slot, None)  # empty the slot
        game.set_action("NO_ACTION")
        game.next_player()

    def __repr__(self):
        """
        Returns the string representation of the tutor card with the name
        """
        return "TutorCard({0})".format(self._name)

    def __str__(self):
        """
        Returns the string representation of the tutor card with the name
        """
        return "TutorCard({0})".format(self._name)


class AllNighterCard(Card):
    """
    A card which, when played, allows the player to put a coder card from another player back to sleep.        
    """
    def play(self, player, game):
        """
        Set the action to be 'SLEEP_CODER'.
        Parameter:
            player (Player): the coder card belongs to
            game (a2_support.CodersGame): the game of sleeping coders.
        """
        super().play(player, game)
        game.set_action("SLEEP_CODER")

    def action(self, player: Player, game, slot):
        """
        the selected card should be added to the first empty slot in the coders' pile
        and removed from its origin deck,
        Parameter:
            player: the coder card belongs to.
            game (a2_support.CodersGame): the game of sleeping coders.
            slot (int): the slot of the coder card to be put into sleep
        """
        card_back = player.get_coders().get_card(slot)  # pick the card
        empty_slot = game.get_sleeping_coders().index(None)
        game.get_sleeping_coders()[empty_slot] = card_back  # put the coder back to sleep
        player.get_coders().remove_card(slot)  # remove from the origin deck
        game.set_action("NO_ACTION")
        game.next_player()

    def __repr__(self):
        """
        Returns the string representation of the AllNighter Card
        """
        return "AllNighterCard()".format()

    def __str__(self):
        """
        Returns the string representation of the AllNighter Card
        """
        return "AllNighterCard()".format()


class KeyboardKidnapperCard(Card):
    """
    A card which, when played allows the player to steal a coder card from another player.
    """
    def play(self, player, game):
        """
        Set the games action to'STEAL_CODER'.
        """
        super().play(player, game)
        game.set_action("STEAL_CODER")

    def action(self, player, game, slot):
        """
        the selected card should be added to the current player's deck and removed from its origin deck
        the action should be set back to'NO_ACTION'
        the game should move on to the next player.
        Parameter:
            player (Player): the player refers to the player to which the coder belongs to.
            game (a2_support.CodersGame): the game of sleeping coders.
            slot (int): the slot of stolen coder card
        """
        card_stolen = player.get_coders().get_card(slot)  # pick the card
        game.current_player().get_coders().add_card(card_stolen)  # put into the deck of current player
        player.get_coders().remove_card(slot)  # remove the coder card
        game.set_action("NO_ACTION")
        game.next_player()

    def __repr__(self):
        """
        Returns the string representation of the KeyboardKidnapper Card
        """
        return "KeyboardKidnapperCard()".format()

    def __str__(self):
        """
        Returns the string representation of the KeyboardKidnapper Card
        """
        return "KeyboardKidnapperCard()".format()


class CoderCard(Card):
    """
    A card which stores the name of a coder card.
    """
    def __init__(self, name):
        """
        Stores the name of a coder card
        """
        self._name = name

    def get_name(self):
        """
        Return coder's name.
        """
        return self._name

    def play(self, player, game):
        """
        The coder card cannot be played, hence the action shall be "NO_ACTION"
        Parameter:
            player (Player): the current player
            game (a2_support.CodersGame): the game of sleeping coders.
        """
        game.set_action("NO_ACTION")

    def action(self, player: Player, game, slot):
        """
        No action for coder card.
        Parameter:
            player (Player): the current player
            game (a2_support.CodersGame): the game of sleeping coders.
            slot (int): the slot of the coder card
        """
        pass

    def __repr__(self):
        """
        Returns the string representation of the coder card with the name
        """
        return "CoderCard({0})".format(self._name)

    def __str__(self):
        """
        Returns the string representation of the coder card with the name
        """
        return "CoderCard({0})".format(self._name)


def main():
    print("Please run gui.py instead")


if __name__ == "__main__":
    main()
