# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
busted = False
outcome = ""
score = 0
click = 0
ended = False


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, 
                          [pos[0] + CARD_CENTER[0], 
                           pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
    def draw_back(self, canvas, pos):
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_SIZE, 
                          [pos[0] + CARD_BACK_CENTER[0], 
                           pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.mano = []

    def __str__(self):
        salida ="hand contains "
        for i in range(len(self.mano)):
            salida += str(self.mano[i])
            salida += " "
        return salida

    def add_card(self, card):
        self.mano.append(card)

    def get_value(self):
        global value,count
        value = 0
        aces = False
        for i in range(len(self.mano)):
            value += int(VALUES[self.mano[i].get_rank()])
            if(self.mano[i].get_rank() == 'A'):
                aces = True
        if(aces and value + 10 <= 21):
            value += 10
        return value
   
    def draw(self, canvas, pos):
        global inc, card1
        card1 = Card('S','A')
        for i in range(len(self.mano)):
            card1 = self.mano[i]
            card1.draw(canvas,[pos[0] + i*100,pos[1]])
        if(in_play):
            card1.draw_back(canvas,[100,200])
        
# define deck class 
class Deck:
    def __init__(self):
        self.mazo = []
        
        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                c = Card(SUITS[i],RANKS[j])
                self.mazo.append(c)

    def shuffle(self):
        random.shuffle(self.mazo)

    def deal_card(self):
        if(len(self.mazo)):
            deal = self.mazo[-1]
            self.mazo.pop()
            return deal
        else:
            print "Deck is empty"
    
    def __str__(self):
        salida ="Deck contains "
        for i in range(len(self.mazo)):
            salida += str(self.mazo[i])
            salida += " "
        return salida

#define event handlers for buttons
def deal():
    global message, outcome, in_play, deck1, busted, score, ended, click
    
    if(not ended and click > 0):
        score -= 1
    click += 1    
    message = "Hit or stand?"
    outcome = ""
    busted = False
    ended = False
    
    deck1 = Deck()
    deck1.shuffle()

    
    global dealer, player
    dealer = Hand()
    player = Hand()

    dealer.add_card(deck1.deal_card())
    player.add_card(deck1.deal_card())
    dealer.add_card(deck1.deal_card())
    player.add_card(deck1.deal_card())

    in_play = True

def hit():
    global in_play, message, outcome, score, busted, ended, click
    click += 1
    if(in_play):
        if(player.get_value() <= 21):
            player.add_card(deck1.deal_card())
        if(player.get_value() > 21):
            outcome = "You have busted!"
            message = "New game?"
            score -= 1
            busted = True
            ended = True
            in_play = False
       
def stand():
    global in_play, message, outcome, score, ended
    
    message = "New game?"
    
    while(in_play):
        dealer.add_card(deck1.deal_card())
        if(dealer.get_value() >= 17):
            in_play = False
    if(not busted and not ended):
        ended = True
        if(dealer.get_value() > 21):
            outcome = "The dealer busted and you win!"
            score += 1
        elif(dealer.get_value() >= player.get_value()):
            outcome = "You lose!"
            score -= 1
        else:
            outcome = "You win!"
            score += 1
        print outcome

# draw handler    
def draw(canvas):
    global score,outcome,message
    
    dealer.draw(canvas, [100,200])
    player.draw(canvas, [100,400])
    
    canvas.draw_text("Blackjack", [60,80], 50, 'Cyan')
    canvas.draw_text("Score: " + str(score), [450,80], 30, 'White')
    canvas.draw_text("Dealer's hand", [60,180], 25, 'White')
    canvas.draw_text(outcome, [270,180], 25, 'Orange')
    canvas.draw_text("Player's hand", [60,380], 25, 'White')
    canvas.draw_text(message, [270,380], 30, 'Orange')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric