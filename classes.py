import random as rand

rand.seed(2)


class Card:
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank
        self.points = points[rank]


class Deck:
    def __init__(self):
        self.cards = []
        self.shuffled = False

    def fill(self):
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        rand.shuffle(self.cards)
        self.shuffled = True

    def print_cards(self, debug=False):
        if debug:
            for card in self.cards:
                print(f"{card.rank},{card.suit}")
        else:
            for card in self.cards:
                print(f"{card.rank} of {card.suit}")


class Stack(Deck):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.num_decks = 0
        self.shuffled = False

    def add_decks(self, num_decks: int):
        for i in range(num_decks):
            self.fill()


class Hand(Deck):
    def __init__(self):
        super().__init__()
        self.points = 0


class Player(Hand):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class Dealer(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.stack = Stack()

    def deal(self, players):
        for i in range(2):
            for player in players:
                player.cards.append(self.stack.cards.pop(0))

    def start_game(self, num_decks: int, players):
        self.stack.add_decks(num_decks=num_decks)
        self.stack.shuffle()
        self.deal(players=players)


suits = ['hearts', 'spades', 'diamonds', 'clubs']
ranks = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']

points = {'ace': 11,
          'two': 2,
          'three': 3,
          'four': 4,
          'five': 5,
          'six': 6,
          'seven': 7,
          'eight': 8,
          'nine': 9,
          'ten': 10,
          'jack': 10,
          'queen': 10,
          'king': 10}
