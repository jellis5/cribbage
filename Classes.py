from random import randint

CARD_MAP = {'Ace': 1, \
			'2': 2, \
			'3': 3, \
			'4': 4, \
			'5': 5, \
			'6': 6, \
			'7': 7, \
			'8': 8, \
			'9': 9, \
			'10': 10, \
			'Jack': 10, \
			'Queen': 10, \
			'King': 10}

RUNS_MAP = {'Ace': 1, \
			'2': 2, \
			'3': 3, \
			'4': 4, \
			'5': 5, \
			'6': 6, \
			'7': 7, \
			'8': 8, \
			'9': 9, \
			'10': 10, \
			'Jack': 11, \
			'Queen': 12, \
			'King': 13}

class Card:
	"""Class for a card.
	
	Args:
		suit: index number of suit in Card.suits
		rank: index number of rank in Card.ranks
	Return:
		Card object
	"""

	suits = ('clubs', 'diamonds', 'hearts', 'spades')
	ranks = (None, 'Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')
	def __init__(self, suit=0, rank=1):
		self.suit = Card.suits[suit]
		self.rank = Card.ranks[rank]
	
	def __str__(self):
		return "{} of {}".format(self.rank, self.suit)
		
class Deck:
	"""Class for a deck of cards.
	
	Args:
		None
	Return:
		Deck object with 52 cards in self.cards
	"""

	def __init__(self):
		self.cards = [Card(suit, rank) for rank in range(1,14) for suit in range(4)]
		
	def __str__(self):
		for each in self.cards:
			print(each)
		return ""
	
	def draw_cards(self, num):
		return [self.cards.pop() for card in range(num)]
		
	def draw_card_objects(self, *cards):
		return [self.cards.pop(n) for card in cards for n,each_card in enumerate(self.cards) \
		if each_card.rank == card.rank and each_card.suit == card.suit]

class Hand(Deck):
	"""Class for a hand of cards.
	
	Args:
		None
	Return:
		Empty hand object; use add_cards(num_cards) method to add to hand
	"""

	def __init__(self):
		self.cards = []
		
	def __str__(self):
		return '\n'.join([str(card) for card in self.cards])
		
	def __iter__(self):
		self.index = 0
		return self
		
	def __next__(self):
		try:
			card = self.cards[self.index]
		except IndexError:
			raise StopIteration
		self.index += 1
		return card

	def add_cards(self, cards):
		self.cards.extend(cards)
		
	def get_card_nums(self):
		return {index+1:card for index,card in enumerate(self.cards)}
		
	def print_card_nums(self):
		print()
		for num,card in self.get_card_nums().items():
			print("{}: {}".format(num, str(card)))
		
	def remove(self, card_obj):
		for n,card in enumerate(self):
			if card.rank == card_obj.rank and card.suit == card_obj.suit:
				del self.cards[n]
				break
		else:
			print("Card not in hand.")
				
class Player:
	def __init__(self):
		self.hand = Hand()
		self.score = 0

class Computer(Player):
	def crib_cards(self):
		first = self.hand.cards[randint(0,5)]
		self.hand.remove(first)
		second = self.hand.cards[randint(0,4)]
		self.hand.remove(second)
		return (first, second)
	#add count and list of cards played as parameters later
	def first_round_play(self, count):
		for card in self.hand.cards:
			if CARD_MAP[card.rank] + count <= 31:
				self.hand.remove(card)
				return card
		else:
			return "go"
		
class GoError(Exception):
	"""Class for catching player trying to go over 31.
	
	All handling should be done in context and outside of this class, hence pass. :)"""
	pass
