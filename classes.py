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


class Shoe(Deck):
    def __init__(self):
        super().__init__()
        self.num_decks = 0
        self.shuffled = False

    def add_decks(self, num_decks: int):
        for i in range(num_decks):
            self.fill()


class Hand:
    def __init__(self):
        self.cards = []
        self.points = 0

    def print_cards(self, debug=False):
        if debug:
            for card in self.cards:
                print(f"{card.rank},{card.suit}")
        else:
            for card in self.cards:
                print(f"{card.rank} of {card.suit}")


class Player(Hand):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.busted = False
        self.stand = False

    def get_points(self):
        self.base_points()
        if self.points == 21:
            self.stand = True
            return "21"
        elif self.points > 21:
            self.check_points()
        if self.busted:
            return "busted"

    def base_points(self):
        # if self.busted:
        #     return
        self.points = 0
        for card in self.cards:
            self.points += card.points
        if self.points == 21:
            self.stand = True

    def check_points(self):
        self.aces = [c for c, card in enumerate(self.cards) if card.rank == 'ace']
        while not self.busted and self.points > 21:
            self.change_aces()

    def change_aces(self):
        if not self.aces:
            return
            # self.busted = True
        for ace in self.aces:
            self.cards[ace].points = 1
            self.base_points()
            if self.points <= 21:
                return
        self.busted = True


class Dealer(Player, Shoe):
    def __init__(self, name: str):
        super().__init__(name)
        self.shoe = Shoe()

    def deal(self, players):
        for i in range(2):
            for j in range(len(players)):
                players[j].cards.append(self.shoe.cards.pop(0))
            self.cards.append(self.shoe.cards.pop(0))
        for player in players:
            player.get_points()
        self.get_points()

    def start_game(self, num_decks: int, players):
        self.shoe.add_decks(num_decks=num_decks)
        self.shoe.shuffle()
        self.deal(players=players)

    def hit(self, player):
        player.cards.append(self.shoe.cards.pop(0))
        player.get_points()
        player.check_points()


class Game:
    def __init__(self, dealer, players, num_decks):
        self.players = players
        self.dealer = dealer
        self.dealer.start_game(players=players, num_decks=num_decks)

    def play(self):
        for player in players:
            player.get


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

dealer = Dealer("Joe the Dealer")
player_1 = Player("Player 1")
player_2 = Player("Player 2")
players = [player_1, player_2]
game = Game(num_decks=1, players=players, dealer=dealer)


def card_info(player):
    for card in player.cards:
        print(f"rank: {card.rank}, suit: {card.suit}, points: {card.points}")


aces = [True if card.rank == 'ace' else False for card in dealer.shoe.cards]
player_3 = Player(name="Player 3")

for c, card in enumerate(aces):
    if card:
        player_3.cards.append(dealer.shoe.cards[c])

for i in range(2):
    dealer.hit(player_3)
    card_info(player_3)
