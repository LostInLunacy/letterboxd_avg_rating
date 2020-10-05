""" When executed, asks the user for a letterboxd username to get the average rating for. """

__version__ = '1.0.0'

# Imports
import requests
from bs4 import BeautifulSoup as bs
import re
from time import sleep

# Local Imports
from user_input import yn

class AvgRating():
    """ This class is the whole program. It's only got the one use, folks. """

    score_count_pattern = r"\d+"

    def __init__(self, username):
        self.username = username

    def __str__(self):
        """ Average Rating: 1.52/5  3.04/10 """    
        return f"Average Rating: {self.avg_rating}/5\t{self.avg_rating*2}/10"

    @property
    def rating(self):
        """ Scrapes the user's Letterboxd profile to get the 
        number of times they have rated a film each score between 0.5 and 5.0
        Returns a dict of each score and the corresponding the user has rated that score.
        r-type: dict. """

        request = requests.get(f'https://letterboxd.com/{self.username}/')
        soup = bs(request.text, 'lxml')
        ratings_section = soup.find('div', class_=['rating-histogram clear rating-histogram-exploded']).find('ul')

        """ There are 10 li tags, 1 for each score 0.5 -> 5
        Within these li tags, there is a link provided that the user has rated >1 film with that rating. """
        ratings_data = [i.find('a') for i in ratings_section.find_all('li', class_='rating-histogram-bar')]
        if len(ratings_data) != 10:
            raise ValueError("Number of possible rating scores should be 10, not", len(ratings_data))

        """ This link has an attribute 'title', at the start of which is the value for the number 
        of times the user has rated a movie that score. """
        get_quantity = lambda x: int(re.findall(self.score_count_pattern, x.get('title'))[0]) if x else 0
        score_quantities = [get_quantity(i) for i in ratings_data]

        # {0.5: 44, 1.0: 108... 5.0: 91}
        return {(score+1)/2: quantity for score, quantity in enumerate(score_quantities)}

    @property
    def total_ratings(self):
        """ Returns the total number of ratings. 
        NOTE: this should align with number on the user's profile. Though it is taken from reading
        the histogram data collected from self.ratings
        r-type: int """
        return sum(self.rating.values())

    @property
    def avg_rating(self, round_to=2):
        """ Computes the average of the ratings collected in self.ratings.
        r-type: float """
        pre_rounded_score = sum([s*q for s,q in self.rating.items()])/self.total_ratings
        return round(pre_rounded_score, round_to)

def main():
    
    while True:
        username = input("Letterboxd Username: ")
        print(AvgRating(username))
        
        if not yn("\nContinue?\t"):
            print("Goodbye, then!")
            sleep(1)

if __name__ == "__main__":
    main()
