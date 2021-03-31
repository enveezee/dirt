#!/usr/bin/env python3

# Example ticket list
tickets = [
    [2,3,5,54,51,11,True,'2021-03-27'],
]

import json
from sys import argv
from urllib.request import Request, urlopen

class Powerball():
    def __init__(self, game='powerball', tickets=None):
        baseurl = 'https://www.powerball.com/'
        pathurl = f'api/v1/numbers/{game}/'
        fileurl = 'recent?_format=json'
        apiurl = f'{baseurl}{pathurl}{fileurl}'
        request = Request(apiurl)
        request.add_header('User-Agent','Mozilla/5.0')
        self.response = json.loads(urlopen(request).read())

        self.game = game

        if tickets:
            for ticket in tickets:
                # Tickets format: [B1,B2,B3,B4,B5,PB,PowerPlay,DATE]
                for numbers in self.response:
                    if ticket[7] == numbers['field_draw_date']:
                        multiplier = int(numbers['field_multiplier'])
                        if not ticket[6]:
                            multiplier = 1
                        numbers = numbers['field_winning_numbers'].split(',')
                        print(self.checkNumbers(numbers, ticket, multiplier))

        else:
            print(response)

    def checkNumbers(self, numbers, ticket, multiplier=1):
        match = 0

        for number in numbers[0:5]:
            if int(number) in ticket[0:5]:
                match = match + 1

        if int(numbers[5]) == ticket[5]:
            ball = True
        else:
            ball = False

        if not ball and match < 3:
            return f'Lost {self.game} on ticket {ticket}.'

        if multiplier == 10:
            multiplier = 6
        
        won = self.ballWon(match, ball, multiplier)

        return f'Won {won} on {self.game} ticket {ticket[0:6]}.'

    def ballWon(self, match, ball, multiplier):
        if ball:            # With power/star ball.
            if match == 5:  # Matched all numbers
                return 'Jackpot'
            won = {
                'lotto-america': [
                    [2,4,6,8,10],                               # Star ball only
                    [2,4,6,8,10],                               # 1 Ball + Star.
                    [5,10,15,20,25],                            # 2 Balls + Star.
                    [20,40,60,80,100],                          # 3 Balls + Star.
                    [1000,2000,3000,4000,5000]                  # 4 Balls + Star.
                ][match],
                'powerball': [
                    [4,8,12,16,20,40],                          # Powerball only.
                    [4,8,12,16,20,40],                          # 1 Ball + Power.
                    [7,14,21,28,35,70],                         # 2 Balls + Power.
                    [100,200,300,400,500,1000],                 # 3 Balls+ Power.
                    [50000,100000,150000,200000,250000,500000]  # 4 Balls + Power.
                ][match]
            }[self.game]
        else:               # No power/star ball.
            won = {
                'lotto-america': [
                    [5,10,15,20,25],                                    # 3 Balls.
                    [100,200,300,400,500],                              # 4 Balls.
                    [20000,40000,60000,80000,100000]                    # 5 Balls.
                ][match - 3],
                'powerball': [
                    [7,14,21,28,35,70],                                 # 3 Balls.
                    [100,200,300,400,500,1000],                         # 4 Balls.
                    [1000000,2000000,2000000,2000000,2000000,2000000],  # 5 Balls.
                ][match - 3]
        }[self.game]
        return f'${int(won[multiplier - 1]):,}'

if __name__ == '__main__':
    if len(argv) > 1:
        for game in ['2by2','lotto-america','powerball']:
            if argv[1].casefold() in game:
                game = Powerball(game)
    else:
        game = Powerball()
    print(game.response[0])
