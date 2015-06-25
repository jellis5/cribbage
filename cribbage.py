#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit
from random import shuffle, randint
from time import sleep
from itertools import combinations
			
from Classes import CARD_MAP, RUNS_MAP, Card, Deck, Hand, Player, Computer, GoError


def first_crib_draw():
	deck = Deck()
	shuffle(deck.cards)
	input("Press enter to randomly select a card.")
	player_card = deck.draw_cards(1)
	print("You selected a {}".format(player_card[0]))
	print("Computer selects a...")
	comp_card = deck.draw_cards(1)
	sleep(1)
	print("{}!".format(comp_card[0]))
	player_card = Card.ranks.index(player_card[0].rank)
	comp_card = Card.ranks.index(comp_card[0].rank)
	if player_card > comp_card:
		print("Computer gets the first crib.")
		return False
	elif player_card < comp_card:
		print("You get the first crib.")
		return True
	else:
		print("Tie!")
		first_crib_draw()

def form_crib(whose_crib):
	crib.cards = []
	crib.cards.extend(comp.crib_cards())
	card_nums = player.hand.get_card_nums()
	player.hand.print_card_nums()
	print()
	print("{} crib.".format("Your" if whose_crib else "Computer's"))
	while True:
		try:
			crib_card1 = input("Select the first card to go into the crib: ")
			crib_card1 = int(crib_card1)
			crib.cards.append(card_nums[crib_card1])
			player.hand.remove(card_nums[crib_card1])
			break
		except (ValueError, KeyError):
			continue
	card_nums = player.hand.get_card_nums()
	player.hand.print_card_nums()
	print()
	while True:
		try:
			crib_card2 = int(input("Select the second card to go into the crib: "))
			crib.cards.append(card_nums[crib_card2])
			player.hand.remove(card_nums[crib_card2])
			break
		except (ValueError, KeyError):
			continue
	
def print_flip_card(card):
	print("*********************".rjust(80))
	print("*     FLIP CARD     *".rjust(80))
	print("*********************".rjust(80))
	print("* {:17s} *".format(card).rjust(80))
	print("*********************".rjust(80))

def flip_card(whose_crib):
	if whose_crib:
		print('\nYou ask for a cut. Opponent obliges.')
		input("\nPress enter to flip the card.")
	else:
		print("\nYou oblige a cut.\nOpponent flips the card.")
		input("Press enter to continue.")
	flip = deck.draw_cards(1)[0]
	print_flip_card(flip)
	if flip.rank == 'Jack':
		if whose_crib:
			print("You got nibs!\n")
			player.score += 2
		else:
			print("Computer got nibs!\n")
			comp.score += 2
		check_for_winner()
			
	return flip

#
# FIRST ROUND FUNCTIONS
#

def is_consec(cards):
	for i in range(len(cards) - 1):
		if cards[i] != cards[i+1] - 1:
			return False
			
	return True

def fr_pair_scorer(cards_played, cp_length):
	if cards_played[-1].rank == cards_played[-2].rank:
		if cp_length >= 3 and cards_played[-1].rank == cards_played[-3].rank:
			if cp_length >= 4 and cards_played[-1].rank == cards_played[-4].rank:
				return (12, "four-of-a-kind for 12")
			return (6, "three-of-a-kind for 6")
		return (2, "pair for 2")
	
def fr_run_scorer(cards_played, cp_length):
	if cp_length < 2:
		return
	run = None
	#for 3-card possible runs to cp_length-card possible runs...
	for runLength in range(3, cp_length + 1):
		#see if runLength-card run by checking if last runLength nums are consecutive
		print([RUNS_MAP[card.rank] for card in cards_played[-1:(runLength*-1)-1:-1]])
		if is_consec(sorted([RUNS_MAP[card.rank] for card in cards_played[-1:(runLength*-1)-1:-1]])):
			run = runLength
		else:
			break
	if run:
		return (run, "run for {}".format(run))
	
def first_round_scorer(cards_played, cp_length, count):
	if cp_length == 1:
		return
	text_and_score = []
	if count == 15:
		text_and_score.append((2, "15 for 2"))
	pairs = fr_pair_scorer(cards_played, cp_length)
	if pairs:
		text_and_score.append(pairs)
	#if card paired, a run in the same play is impossible
	else:
		runs = fr_run_scorer(cards_played, cp_length)
		if runs:
			text_and_score.append(runs)
	
	return text_and_score

def first_round(whose_crib, flip_card):
	if whose_crib:
		turn_alt = 3
	else:
		turn_alt = 2
	
	comp_played_cards = []
	player_played_cards = []
	while True:
		count = 0
		comp_go_flag = False
		player_go_flag = False
		comp_empty_hand = False
		player_empty_hand = False
		cards_played = []
		while len(player.hand.cards) != 0 or len(comp.hand.cards) != 0:
			if count == 31:
				break
			if len(player.hand.cards) == 0:
				player_empty_hand = True
			else:
				for card in player.hand:
					if CARD_MAP[card.rank] + count <= 31:
						break
				else:
					player_go_flag = True
			if len(comp.hand.cards) == 0:
				comp_empty_hand = True
			else:
				for card in comp.hand:
					if CARD_MAP[card.rank] + count <= 31:
						break
				else:
					comp_go_flag = True
			
			if turn_alt % 2 == 0:
				if player_empty_hand:
					turn_alt += 1
					continue
				print("Your turn.")
				print("Opponent's cards left: {}".format(len(comp.hand.cards)))
				card_nums = player.hand.get_card_nums()
				player.hand.print_card_nums()
				if player_go_flag:
					input("You can't go. Press enter to continue.")
					if comp_go_flag or comp_empty_hand:
						input("Computer can't go either. Press enter to continue.")
						break
					turn_alt += 1
					continue
				while True:
					try:
						card = input("Select card to play ('s' for scores): ")
						if card == 's':
							show_scores()
							continue
						card = int(card)
						if CARD_MAP[card_nums[card].rank] + count > 31:
							raise GoError
						count += CARD_MAP[card_nums[card].rank]
						player_played_cards.append(card_nums[card])
						cards_played.append(card_nums[card])
						player.hand.remove(card_nums[card])
						if len(player.hand.cards) == 0:
							player_empty_hand = True
						turn_alt += 1
						break
					except (ValueError, KeyError):
						continue
					except GoError:
						print("You can't play a card that exceeds 31.")
						continue
			else:
				if comp_empty_hand:
					turn_alt += 1
					continue
				if comp_go_flag:
					input("Computer can't go. Press enter to continue.")
					if player_go_flag or player_empty_hand:
						input("You can't go either. Press enter to continue.")
						break
					turn_alt += 1
					continue
				print("Computer's turn. He's thinking...\n")
				sleep(1)
				comp_card = comp.first_round_play(count)
				count += CARD_MAP[comp_card.rank]
				comp_played_cards.append(comp_card)
				cards_played.append(comp_card)
				if len(comp.hand.cards) == 0:
					comp_empty_hand = True
				turn_alt += 1
			print("***************")
			print("\nCount: {}\n".format(count))
			for card in cards_played:
				print(card)
			print("***************")
			print()
			print_flip_card(flip_card)
			score_text = first_round_scorer(cards_played, len(cards_played), count)
			if score_text:
				for score,text in score_text:
					input("{} {}. Press enter to continue.".format("You say" if cards_played[-1] is player_played_cards[-1] else "Computer says", text))
					if cards_played[-1] is player_played_cards[-1]:
						player.score += score
					else:
						comp.score += score
					check_for_winner()
				show_scores()
		if count == 31:
			if comp_empty_hand and player_empty_hand:
				if cards_played[-1] is player_played_cards[-1]:
					input("You say 31 for 2. Press enter to continue.")
					player.score += 2
				else:
					input("Computer says 31 for 2. Press enter to continue.")
					comp.score += 2
				check_for_winner()
				break
			else:
				if cards_played[-1] is player_played_cards[-1]:
					input("You say 31 for 2. Press enter to continue.")
					player.score += 2
				else:
					input("Computer says 31 for 2. Press enter to continue.")
					comp.score += 2
				check_for_winner()
		else:
			if comp_empty_hand and player_empty_hand:
				if cards_played[-1] is player_played_cards[-1]:
					input("You got one for last. Press enter to continue.")
					player.score += 1
				else:
					input("Computer got one for last. Press enter to continue.")
					comp.score += 1
				check_for_winner()
				break
			else:
				if cards_played[-1] is player_played_cards[-1]:
					input("You got one for last. Press enter to continue.")
					player.score += 1
				else:
					input("Computer got one for last. Press enter to continue.")
					comp.score += 1
				check_for_winner()
		show_scores()
	player.hand.cards.extend(player_played_cards)
	comp.hand.cards.extend(comp_played_cards)
	
#
# SECOND ROUND FUNCTIONS
#
	
def count_flush(suits, crib=False):
	if suits[0] == suits[1] == suits[2] == suits[3]:
		if suits[3] == suits[4]:
			return 5
		return 0 if crib else 4
	return 0

def count_nobs(cards, flip_card):
	for card in cards:
		if card.rank == 'Jack' and card.suit == flip_card.suit:
			return 1
	return 0

def count_pairs(cards):
	points = 0
	for combo in combinations(cards, 2):
		if combo[0] == combo[1]:
			points += 2
	
	return points

def count_runs(cards):
	points = 0
	# we only need to test for 3-card runs if no 4-card runs exist
	run4flag = False
	# check for 5-card run first
	for combo5 in combinations(cards, 5):
		if is_consec(sorted(combo5)):
			points += 5
			break
	else:
		for combo4 in combinations(cards, 4):
			if is_consec(sorted(combo4)):
				run4flag = True
				points += 4
		if not run4flag:
			for combo3 in combinations(cards, 3):
				if is_consec(sorted(combo3)):
					points += 3
	
	return points

def count_fifteens(card_values):
	points = 0
	for card_combo in combinations(card_values, 2):
		if card_combo[0] + card_combo[1] == 15:
			points += 2
	for card_combo in combinations(card_values, 3):
		if card_combo[0] + card_combo[1] + card_combo[2] == 15:
			points += 2
	for card_combo in combinations(card_values, 4):
		if card_combo[0] + card_combo[1] + card_combo[2] + card_combo[3] == 15:
			points += 2
	for card_combo in combinations(card_values, 5):
		if card_combo[0] + card_combo[1] + card_combo[2] + card_combo[3] + card_combo[4] == 15:
			points += 2
			
	return points
	
def print_score(hand, flip_card):
	values = [CARD_MAP[card.rank] for card in hand.cards]
	values.append(CARD_MAP[flip_card.rank])
	rank_nums = [RUNS_MAP[card.rank] for card in hand.cards]
	rank_nums.append(RUNS_MAP[flip_card.rank])
	suits = [card.suit for card in hand.cards]
	suits.append(flip_card.suit)

	fifteens = count_fifteens(values)
	runs = count_runs(rank_nums)
	pairs = count_pairs(rank_nums)
	nobs = count_nobs(hand.cards, flip_card)
	flush = count_flush(suits)
	total = fifteens + runs + pairs + nobs + flush
	print("\nFifteens:", fifteens)
	print("Runs:", runs)
	print("Pairs:", pairs)
	print("Nobs:", nobs)
	print("Flush:", flush)
	print("\nTotal:", total)
	
	return total
	
def ask_player_points():
	while True:
		try:
			points = int(input("Enter how many points you have: "))
			if points < 0 or points > 29:
				raise KeyError
			break
		except ValueError:
			continue
		except KeyError:
			print("Hand must be between 0 and 29 points.")
			continue
	return points
	
def check_player_points(points, total):
	if total >= points:
		if points == total:
			print("Yeah, you got {} point(s).".format(points))
		else:
			print("You missed {} point(s).".format(total - points))
		return points
	else:
		print("No, you only got {} point(s). 2 point deduction from actual point amount.".format(total))
		return total - 2
	
def second_round(whose_crib, flip_card):
	if whose_crib:
		input("It's your crib. Computer scores first. Press enter to continue.")
		print()
		print_flip_card(flip_card)
		print(comp.hand)
		print("\nComputer has...")
		comp.score += print_score(comp.hand, flip_card)
		show_scores()
		check_for_winner()
		#your turn to score
		input("Your turn to score. Press enter to continue.")
		print()
		print_flip_card(flip_card)
		print(player.hand)
		points = ask_player_points()
		total = print_score(player.hand, flip_card)
		player.score += check_player_points(points, total)
		show_scores()
		check_for_winner()
		print("\nNow for the crib.\n")
		print_flip_card(flip_card)
		print(crib)
		points = ask_player_points()
		total = print_score(crib, flip_card)
		player.score += check_player_points(points, total)
		show_scores()
		check_for_winner()
	else:
		input("Computer's crib. You score first. Press enter to continue.")
		print()
		print_flip_card(flip_card)
		print(player.hand)
		points = ask_player_points()
		total = print_score(player.hand, flip_card)
		player.score += check_player_points(points, total)
		show_scores()
		check_for_winner()
		#computer's turn to score
		input("Computer's turn to score. Press enter to continue.")
		print()
		print_flip_card(flip_card)
		print(comp.hand)
		print("\nComputer has...")
		comp.score += print_score(comp.hand, flip_card)
		show_scores()
		check_for_winner()
		input("\nNow for the crib. Press enter to continue.")
		print()
		print_flip_card(flip_card)
		print(crib)
		print("\nComputer has...")
		comp.score += print_score(crib, flip_card)
		show_scores()
		check_for_winner()

def show_scores():
	print("************".rjust(80))
	print("** SCORES **".rjust(80))
	print("* YOU: {:3d} *".format(player.score).rjust(80))
	print("* OPP: {:3d} *".format(comp.score).rjust(80))
	print("************".rjust(80))

def check_for_winner():
	if player.score >= 121:
		if comp.score <= 90:
			print("**************************")
			print("YOU SKUNKED THE COMPUTER!")
			print("**************************")
			exit()
		print("********")
		print("YOU WIN!")
		print("********")
		exit()
	if comp.score >= 121:
		if player.score <= 90:
			print("*****************")
			print("YOU GOT SKUNKED!")
			print("*****************")
			exit()
		print("*********")
		print("OPP WINS!")
		print("*********")
		exit()
		
		
def main():
	print("Welcome to Cribbage!\n")
	#whose_crib returns True for player's crib, false for opponent's
	whose_crib = first_crib_draw()
	global player
	global comp
	global crib
	global deck
	player = Player()
	comp = Computer()
	crib = Hand()
	while True:
		deck = Deck()
		shuffle(deck.cards)
		player.hand.add_cards(deck.draw_cards(6))
		comp.hand.cards = []
		comp.hand.add_cards(deck.draw_cards(6))
		form_crib(whose_crib)
		flip = flip_card(whose_crib)
		first_round(whose_crib, flip)
		second_round(whose_crib, flip)
		print("\n*************")
		print("* NEXT HAND *")
		print("*************\n")
		player.hand.cards = []
		comp.hand.cards = []
		crib.cards = []
		whose_crib = False if whose_crib else True

	return 0

if __name__ == '__main__':
	main()
