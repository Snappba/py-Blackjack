import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

#Card Class
class Card:
    def __init__ (self,suit, rank):
        self.suit = suit
        self.rank = rank
        self.image_path= f"card_images/{rank.lower()}_of_{suit.lower()}.png"

    def __str__ (self):
        return f"{self.rank} of {self.suit}"

#deck class 
class Deck:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 
              'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

    def __init__(self):
        self.deck = [Card(suit,rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()
    
#hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += Deck.values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -=10
            self.aces -= 1

    def __str__(self):
        hand_comp =''
        for card in self.cards:
            hand_comp +='\n' + card.__str__()
        return 'Hand Value: ' +str(self.value) + hand_comp
    
#game class
class Game:
    def __init__(self):
        #initalizes the game
        self.deck = Deck()
        self.player_hand = Hand()
        self.house_hand = Hand()
        self.window = tk.Tk()
        self.window.title("BlackJack")
        #self.window.iconbitmap (r'blackjack.ico')

        # Initialize stats variables
        self.player_round_wins = 0
        self.house_round_wins = 0
        self.player_round_busts = 0
        self.house_round_busts = 0

        # Stats Labels
        self.stats_frame = tk.Frame(self.window)
        self.stats_frame.pack(pady=10, fill=tk.X)
        
        self.house_wins_label = tk.Label(self.stats_frame, text="House Wins: 0")
        self.house_wins_label.pack(side=tk.LEFT, padx=10)

        self.house_busts_label = tk.Label(self.stats_frame, text="House Busts: 0")
        self.house_busts_label.pack(side=tk.LEFT, padx=10)

        self.player_wins_label = tk.Label(self.stats_frame, text="Player Wins: 0")
        self.player_wins_label.pack(side=tk.LEFT, padx=10)

        self.player_busts_label = tk.Label(self.stats_frame, text="Player Busts: 0")
        self.player_busts_label.pack(side=tk.LEFT, padx=10)

        
        #frames
        self.house_frame = tk.Frame(self.window)
        self.house_frame.pack(pady=20)
        self.player_frame = tk.Frame(self.window)
        self.player_frame.pack(pady= 20)
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady= 20)

        
        #labels for house and player hands
        self.house_label = tk.Label(self.house_frame, text = "House's Hand")
        self.house_label.pack()
        self.house_card_labels = []

        self.player_label = tk.Label (self.player_frame, text = "Player's Hand")
        self.player_label.pack()
        self.player_card_labels = []

        #labels for house and player scores
        self.house_score_label = tk.Label(self.house_frame, text = "House's Visible Score: 0")
        self.house_score_label.pack()
        self.player_score_label  = tk.Label(self.player_frame, text = "PLayer's Score: 0")
        self.player_score_label.pack()

        #buttons
        self.hit_button = tk.Button (self.button_frame, text = "Hit", command = self.hit)
        self.hit_button.pack(side= tk.LEFT, padx=10)
        self.stand_button = tk.Button (self.button_frame, text = "Stand", command = self.stand)
        self.stand_button.pack(side= tk.LEFT, padx=10)
        self.reset_button = tk.Button (self.button_frame, text = "Reset", command = self.reset)
        self.reset_button.pack(side= tk.LEFT, padx=10)

        self.reset()
        self.window.mainloop()

    def deal_initial(self):
        #deals 2 cards to the house and the player
        for _ in range(2):
            self.player_hand.add_card(self.deck.deal())
            self.house_hand.add_card(self.deck.deal())

    def show_some(self):
        #shows the players hand an 1/2 of the house's hand
        try:
            self.house_card_labels = [self.load_card_image ("card_images/back.jpg"), self.load_card_image(self.house_hand.cards[1].image_path)]
            self.player_card_labels = [self.load_card_image (card.image_path) for card in self.player_hand.cards]

            self.update_hand_display(self.house_frame, self.house_card_labels)
            self.update_hand_display(self.player_frame, self.player_card_labels)

            self.update_scores(show_house_full=False)
            
        except FileNotFoundError as e:
            messagebox.showerror("File Not Found", str(e))

    def show_all(self):
        #shows all cards in play
        try:
            self.house_card_labels = [self.load_card_image (card.image_path) for card in self.house_hand.cards]
            self.update_hand_display(self.house_frame, self.house_card_labels)

            self.update_scores(show_house_full=True)                                       

        except FileNotFoundError as e:
            messagebox.showerror("File Not Found", str(e))

    def hit(self):
        #the player is dealt 1 addtional card
        try:
            self.player_hand.add_card(self.deck.deal())
            self.player_card_labels = [self.load_card_image(card.image_path) for card in self.player_hand.cards]
            self.update_hand_display(self.player_frame, self.player_card_labels)
            self.update_scores(show_house_full=False)

            if self.player_hand.value >21:
                self.player_busts()

        except FileNotFoundError as e:
            messagebox.showerror("File Not Found", str(e))
        
    def player_busts(self):
        #players total exceeded 21, losing the game
        self.player_round_busts += 1
        messagebox.showinfo("Game Over", "Player busts! House wins.")
        self.hit_button.config(state = tk.DISABLED)
        self.stand_button.config(state =tk.DISABLED)
        self.update_stats()
        #Makes it show the houses full hand after the player busts
        self.show_all()

    def house_busts(self):
        #house's total exceeded 21, losing the game
        self.house_round_busts += 1
        messagebox.showinfo("Game Over", "House busts! Player wins.")
        self.hit_button.config(state = tk.DISABLED)
        self.stand_button.config(state =tk.DISABLED)
        self.update_stats()

    def player_wins(self):
        #player had a higher value than the house without busting, or the house bust
        self.player_round_wins += 1
        messagebox.showinfo("Game Over", "Player wins.")
        self.hit_button.config(state = tk.DISABLED)
        self.stand_button.config(state =tk.DISABLED)
        self.update_stats()

    def house_wins(self):
        #house had a higher value than the player without busting, or the player bust
        self.house_round_wins += 1
        messagebox.showinfo("Game Over", "House wins.")
        self.hit_button.config(state = tk.DISABLED)
        self.stand_button.config(state =tk.DISABLED)
        self.update_stats()

    def push(self):
        #house and player had same value
        messagebox.showinfo("Game Over", "It's a tie!")
        self.hit_button.config(state = tk.DISABLED)
        self.stand_button.config(state =tk.DISABLED)

    def update_stats(self):
        #updates the stats after each round
        self.player_wins_label.config(text=f"Player Wins: {self.player_round_wins}")
        self.house_wins_label.config(text=f"House Wins: {self.house_round_wins}")
        self.player_busts_label.config(text=f"Player Busts: {self.player_round_busts}")
        self.house_busts_label.config(text=f"House Busts: {self.house_round_busts}")

    def stand(self):
        #player chooses not to be dealt an additional card
        while self.house_hand.value < 17:
            self.house_hand.add_card(self.deck.deal())
        self.show_all()
        #win conditions
        if self.house_hand.value >21:
            self.house_busts()
        elif self.house_hand.value > self.player_hand.value:
            self.house_wins()
        elif self.house_hand.value < self.player_hand.value:
            self.player_wins()
        else:
            self.push()

    def reset(self):
        #resets, dealing 2 new cards to the house and the player
        self.deck = Deck()
        self.player_hand = Hand()
        self.house_hand = Hand()
        self.deal_initial()
        self.show_some()
        self.hit_button.config(state = tk.NORMAL)
        self.stand_button.config(state = tk.NORMAL)

    def load_card_image(self, image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((100,150)) # make the image fit within the gui, rather than true size
            return ImageTk.PhotoImage(image)
        except FileNotFoundError:
            raise FileNotFoundError(f"Image file not found: {image_path}")
    
    def update_hand_display(self, frame, card_images):
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label) and widget not in (self.house_label, self.player_label, self.house_score_label, self.player_score_label):
                widget.destroy()
        
        for image in card_images:
            label = tk.Label(frame, image=image)
            label.image = image
            label.pack(side = tk.LEFT, padx=5)

    def update_scores(self, show_house_full):
        if show_house_full:
            house_score = self.house_hand.value
        else:
            #calculate the house's visible score (exclude the hidden card)
            house_score = Deck.values[self.house_hand.cards[1].rank]
        
        self.house_score_label.config(text = f"House's Visible Score: {house_score}")
        self.player_score_label.config(text = f"Player's Score: {self.player_hand.value}")
#start the game
game = Game()