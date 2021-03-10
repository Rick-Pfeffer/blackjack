import random as rand
import csv

rand.seed(1235)


class Card:
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank
        self.points = points[rank]


class Deck:
    def __init__(self):
        self.cards = []

    def fill(self):
        # create one full deck
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        rand.shuffle(self.cards)

    def print_cards(self):
        # function to print cards, debugging only
        for card in self.cards:
            print(f"{card.rank} of {card.suit}")


class Shoe(Deck):
    # class to create "shoes" or stacks of decks.
    # Blackjack is typically played with more than one deck and up to eight
    def __init__(self):
        super().__init__()
        self.num_decks = 0
        self.discard_pile = []

    def add_decks(self, num_decks: int):
        for i in range(num_decks):
            self.fill()

    def shuffle_discard(self):
        self.cards = self.discard_pile
        self.shuffle()
        self.discard_pile = []


class Hand:
    def __init__(self):
        self.cards = []
        self.points = 0

    # helper function for debugging. Will print players cards
    def print_cards(self, debug=False):
        for card in self.cards:
            print(f"{card.rank} of {card.suit}")


class Player(Hand):
    # Player is initialized with target points. These target points default to 17 (dealer's target) but will be
    # inputted as a random variable for simulation
    def __init__(self, name: str, target_points=17):
        super().__init__()
        self.name = name
        self.busted = False
        self.stand = False
        self.winner = False
        self.tied = False
        self.target_points = target_points
        self.aces = []
        self.points_before = 0

    # Initial function to get the players points
    def get_points(self):
        # get points before the last hit (important for output analysis)
        self.points_before = self.points
        # get points assuming all aces are equal to 11
        self.base_points()
        if self.points > 21:
            # if the player has more than 21 points, we need to check for aces to see if we can adjust their score
            self.check_points()
        elif self.points >= self.target_points:
            # stand if the player hits their target points
            self.stand = True

    def check_points(self):
        # this function is called if a player has over 21 points
        # first find any aces in the player's hand
        self.aces = [c for c, card in enumerate(self.cards) if card.rank == 'ace']
        if not self.aces:
            # if the player has no aces, their points will stay above 21, so they bust
            self.busted = True
        else:
            for ace in self.aces:
                # for each ace, we need to check the modified score.
                # first set the ace to one point
                self.cards[ace].points = 1
                # then get their points after adjustment
                self.base_points()
                if self.points <= 21:
                    return
        # if the above if statement never returns, the player has busted
        self.busted = True

    def base_points(self):
        # this function is required so we don't get a recursive call in get_points
        # get_points calls this function after adjusting aces, if required
        self.points = 0
        for card in self.cards:
            self.points += card.points


class Dealer(Player, Shoe):
    def __init__(self, name: str):
        super().__init__(name)
        self.shoe = Shoe()

    def deal(self, players):
        for i in range(2):
            for player in players + [dealer]:
                try:
                    player.cards.append(self.shoe.cards.pop(0))
                except IndexError:
                    self.shoe.shuffle_discard()
                    player.cards.append(self.shoe.cards.pop(0))
        for player in players + [dealer]:
            player.get_points()

    def start_game(self, num_decks: int, players):
        self.shoe.add_decks(num_decks=num_decks)
        self.shoe.shuffle()
        self.deal(players=players)

    def hit(self, player):
        try:
            player.cards.append(self.shoe.cards.pop(0))
        except IndexError:
            self.shoe.shuffle_discard()
            player.cards.append(self.shoe.cards.pop(0))
        player.get_points()


class Game:
    def __init__(self, dealer, players, num_decks, target_points):
        self.players = players
        self.dealer = dealer
        self.target_points = target_points
        self.is_over = False
        self.dealer.start_game(players=players, num_decks=num_decks)
        dealer.showing_info = ' of '.join([dealer.cards[1].rank, dealer.cards[1].suit])
        dealer.showing_points = dealer.cards[1].points

    def play(self):
        # if the dealer has blackjack, score the game immediately
        if self.dealer.points == 21:
            self.score_game()
            return
        # each player takes their turn
        for player in players:
            # print(f"{player.name} starting")
            # player.print_cards()
            # if player has 21 on the deal, its a blackjack
            if player.points == 21:
                # print("Blackjack!")
                player.stand = True
            elif player.points >= self.target_points:
                player.stand = True
            else:
                # player continues to hit until they reach their target score or bust
                while not player.busted and not player.stand:
                    self.dealer.hit(player)
                    # print(f"{player.name} hits.")
                    # player.print_cards()
                    if not player.busted and player.points >= self.target_points:
                        player.stand = True
        # dealer plays
        # ASSUMPTIONS:
        # Dealer MUST HIT if they have 16 or less.
        # Dealer MUST STAND if they have 17 or more.
        # print(f"Dealer has {dealer.points} points")
        while dealer.points < 17:
            dealer.hit(dealer)
            # print(dealer.points)
        if dealer.busted:
            pass
        else:
            dealer.stand = True
        self.score_game()

    def score_game(self):
        for player in self.players:
            # print(f"{player.name} has {player.points} points.")
            # print(f"Dealer has {dealer.points} points")
            if player.busted:
                # print(f"{player.name} busted and lost.")
                continue
            elif self.dealer.busted:
                # print(f"The dealer busted and {player.name} did not. {player.name} wins!")
                player.winner = True
                continue
            elif self.dealer.points > player.points:
                # print(f"{player.name} had less points and lost.")
                continue
            elif self.dealer.points == player.points:
                # print(f"Dealer and {player.name} drew.")
                player.tied = True
                continue
            else:
                # print(f"{player.name} had more points and beat the dealer!")
                player.winner = True

    def reset_hands(self):
        for player in self.players + [dealer]:
            player.busted = False
            player.stand = False
            player.winner = False
            player.tied = False
            player.aces = []
            player.points_before = 0
            player.points = 0
            for card in player.cards:
                self.dealer.shoe.discard_pile.append(card)
            player.cards = []


suits = ['hearts', 'spades', 'diamonds', 'clubs']
ranks = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
points = {'ace': 11, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
          'jack': 10, 'queen': 10, 'king': 10}


def card_info(player):
    for card in player.cards:
        print(f"rank: {card.rank}, suit: {card.suit}, points: {card.points}")


columns = ['Target Points', 'Player Won?', 'Player Tied?', 'Player Busted?',
           'Player Points', 'Dealer Points', 'Dealer Showing', 'Player Points on Last Hit',
           'Decks', 'discard number', 'shoe number', 'equals 1']

with open('test.csv', 'w', newline='') as output:
    w = csv.DictWriter(output, fieldnames=columns)
    w.writeheader()

for target in range(12, 22, 1):
    for i in range(100000):
        dealer = Dealer("Joe the Dealer")
        player_1 = Player("Player 1", target_points=target)
        players = [player_1]

        decks = rand.randint(1, 8)

        game = Game(num_decks=decks, players=players, dealer=dealer, target_points=target)
        game.play()

        with open('test.csv', 'a', newline='') as output:
            w = csv.DictWriter(output, fieldnames=columns)
            w.writerow({'Target Points': player_1.target_points,
                        'Player Won?': player_1.winner,
                        'Player Tied?': player_1.tied,
                        'Player Busted?': player_1.busted,
                        'Player Points': player_1.points,
                        'Dealer Points': dealer.points,
                        'Dealer Showing': dealer.showing_points,
                        'Player Points on Last Hit': player_1.points_before,
                        'Decks': game.dealer.shoe.num_decks,
                        'discard number': len(game.dealer.shoe.discard_pile),
                        'shoe number': len(game.dealer.shoe.cards),
                        'equals 1': (len(game.dealer.shoe.discard_pile) + len(game.dealer.shoe.cards)) / 52 / (
                            decks)})

        game.reset_hands()
