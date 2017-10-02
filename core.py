import time
import threading
import random

EASY = 1
MEDIUM = 2
HARD = 4
TURN_TIME = 5

class Settings:
    def __init__(self, players, is_pair, amount, difficulties):
        self.players = players
        self.is_pair = is_pair
        self.difficulties = difficulties
        self.amount = amount

def generateWords(amount, difficulties):
    word_lists = []
    if EASY & difficulties:
        word_lists.append(open("easy.txt").read().split())
    if MEDIUM & difficulties:
        word_lists.append(open("medium.txt").read().split())
    if HARD & difficulties:
        word_lists.append(open("hard.txt").read().split())

    n = amount // len(word_lists)
    generated = []
    for i in range(len(word_lists) - 1):
        generated.extend(random.sample(word_lists[i], n))
    generated.extend(random.sample(word_lists[-1], amount - len(generated)))
    generated = set(generated)
    while (len(generated) < amount):
        if (len(word_lists[-1]) == 0):
            word_lists.pop()
        generated.add(word_lists[-1].pop())
    generated = list(generated)
    return generated


class Game:
    def __init__(self, settings):
        self.word_list = generateWords(settings.amount, settings.difficulties)
        self.player_names = settings.players
        self.players_amount = len(settings.players)
        self.player_results_guessed = [0] * len(settings.players)
        self.player_results_explained = [0] * len(settings.players)
        self.is_pair = settings.is_pair
        if (self.is_pair):
            self.current_pair = [0, self.players_amount // 2]
        else:
            self.current_pair = [0, 1]
        self.turn_number = 0
        self.current_word = ''
        self.turn_result = 0
        self.is_active_turn = 0

    def turn(self):
        if (self.current_pair[0] == 0):
            self.turn_number += 1
        self.start_time = time.time()
        self.new_word()
        end_timer = threading.Timer(TURN_TIME, self.turn_end)
        end_timer.start()
        self.is_active_turn = True

    def success_word(self):
        self.turn_result += 1
        self.word_list.remove(self.current_word)
        self.new_word()

    def inc_person(self, i):
        self.current_pair[i] += 1
        self.current_pair[i] %= self.players_amount

    def next_pair(self):
        self.inc_person(0)
        self.inc_person(1)
        if not self.is_pair and self.current_pair[0] == 0:
            self.inc_person(1)
            if (self.current_pair[0] == self.current_pair[1]):
                self.inc_person(1)

    def turn_end(self):
        self.player_results_explained[self.current_pair[0]] += self.turn_result
        self.player_results_guessed[self.current_pair[1]] += self.turn_result
        self.next_pair()
        self.turn_result = 0
        self.is_active_turn = False

    def new_word(self):

        if (len(self.word_list) == 0):
            self.turn_end()
        else:
            self.current_word = random.choice(self.word_list)

    def get_pair_names(self):
        return self.player_names[self.current_pair[0]], self.player_names[self.current_pair[1]]

    def get_current_word(self):
        if not self.is_active_turn:
            return "here should be a word"
        return self.current_word

    def get_time_remaining(self):
        return TURN_TIME - int(time.time() - self.start_time)

    def get_current_words_amount(self):
        return len(self.word_list)

    def get_results(self):
        raw = [(self.player_names[i], self.player_results_explained[i],
                self.player_results_guessed[i]) for i in range(self.players_amount)]
        raw.sort(key=lambda x : x[1] + x[2])
        formatted = ["%s: \t ❗%d \t 💡 %d " % raw[i] for i in range(len(raw))]
        return formatted

def requestSettings():
    print("Please, tell me amount of players")
    players_amount = int(input())
    print("and now, do you want to play by pairs?[01]")
    is_pair = int(input())
    players = []
    if (not is_pair):
        print("Then, tell me your names")
        players = [input() for i in range(players_amount)]
    else:
        print("Type pairs in format:\n first player : second player\n ...")
        first_players, second_players = [], []
        for i in range(players_amount // 2):
            pair = input().split(" : ")
            first_players.append(pair[0])
            second_players.append(pair[1])
        players = first_players + second_players
    print("We almost have done it! Now tell me amount of words")
    words_amount = int(input())
    print("Good! Now wait a sec")
    return Settings(players, is_pair, words_amount, MEDIUM ^ HARD)

