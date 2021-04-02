---
layout: post
title: "A Monte Carlo analysis of the board game Elder Sign"
date: 2021-04-02
excerpt: "Sample text."
tags: [monte carlo, gaming]
comments: true
---

Elder Sign is a Lovecraft-themed co-operative board game that I've been playing a lot of during the UK's
second lockdown.
Like any mathematically inclined person my first thought was to see if I could beat the game by calculating
the best choice in any particular scenario.
However, the game contains a bunch of mechanics that resist an exact analysis so I decided to take a computational
approach instead - Monte Carlo analysis.
Monte Carlo analysis just means rolling the (virtual) dice many times and seeing what happens, it's equivalent 

# Elder Sign in a nutshell 

In order for this blog post to be interesting, you'll either need to have played Elder Sign or at least have an outline
of how it works and what are the important choices that determine whether you win or lose.
There are three important types of object in Elder Sign; Investigators, Adventures and the Ancient One.

## The Ancient One

This is the big bad guy you are working together to defeat, there's a selection of these with various difficulties
including Lovecraft favourites such as Cthulu and Azathoth as well as some invented for Elder Sign with a similar vibe.
A single playthrough involves only one Ancient One and ends in a loss when the Ancient One acquires a certain number
of Doom Tokens and conversely ends in a victory when a certain number (typically around 10) of Elder Signs are placed 
on the Ancient One, sealing it away for good.
Essentially, Elder Signs and Doom Tokens function as independent victory and loss tracks and you want to maximise the
number of the first and minimise the number of the latter.
Each of the Ancient Ones has a special ability that impacts the game and a different number of Elder Signs/Doom Tokens
required to win/lose - I've not attempted to include these points in my analysis.

[Example ancient one]

## Investigators and items

Investigators are the player controlled characters and have two independent "hitpoints", health and sanity. 
If either of these reach 0 the character dies and is replaced with a new one - in order for this to have consequences, 
dieing also triggers a penalty in the form of a Doom Token.
Investigators can accumulate items of various kinds throughout the game by completing Adventures,
the majority of which are consumables that provide single-use benefits when attempting Adventures.
Like Ancient Ones, there's a large selection of Investigators with differing health/sanity hitpoints, special abilities
and starting items.

[Example investigator]

## Adventures

Each turn, a player choose which of the available (typically between 6 and 9) Adventures to attempt.
An Adventure has a bunch of tasks (I'll get to what these actually are in a moment), 
all of which must be completed to successfully complete the Adventure.
These tasks are visible in advance and taken together determine how difficult it is to succeed at a particular
adventure.
Each Adventure has a visible, fixed reward for success and a visible, fixed penalty for failure.
These rewards and penalties include things such as Doom Tokens or Elder Signs, which directly 
get you closer to victory or defeat, and items that can be used for advantages in later Adventures.
Additionally, when an Adventure is completed it is replaced with another from a deck and the Investigator
who completed gets a certain number of Trophy Points that act as currency at an in-game shop.

The "main loop" of the game involves weighing up the Adventures currently on the board,
identifying which has the best risk/reward tradeoff and then attempting that one.
These sounds simple but as we'll see in the next section evaluating the success probability of a particular 
Adventure is non-trivial.

### Anatomy of an Adventure

There's no better way to understand all of this than to look at a few examples and luckily the 
rulebook has done this for me already.

[Adventure Card Anatomy from the rulebook]

### Attempting Adventures

So how does one actually attempt an Adventure?
In a nutshell it involves repeatedly rolling a set of non-standard dice and matching symbols on the dice
to symbols on the Adventure card.
This involves a lot of randomness and although the game does include a few opportunities for player choice in 
attempting an Adventure, the skill cap of these choices is low (there's an obviously correct action in most cases) 
and their effect is quite small.

As the player has relatively little control over the outcome of an Adventure once it's started the most important 
choices are what Adventures to attempt and what consumable items to use before attempting as these grant additional
dice to be used throughout the attempt.
Clue items can also be used during the Adventure but do not have to be commited in advance.
Even though player choice is limited, 
its still crucial to understand the internals of Adventures in order to estimate success probabilities.

The algorithm for attempting an (un-ordered) Adventure is summarised below in Python-esque pseudocode.
```
def attempt_adventure(tasks, dice, clues)
    while len(dice) > 0 and len(tasks) > 0:
        dice_result: List[Symbol] = dice.roll()
        matched_tasks, matched_dice: List[bool], List[Dice] = tasks.match(dice_reseult)
        if any(matched_tasks):
            completed_task, used_dice = select_task_to_complete(matched_tasks, matched_dice)
            dice.remove(used_dice)
            tasks.pop(completed_task)
        else:
            if clues > 0:
                # Clues act as a partial re-roll
                clue_policy(dice)
                continue
                
            focus_policy(dice)
            dice.pop()  # Remove one dice
            
        if len(tasks) == 0:
            return SUCCESS
        else:
            return FAILURE
```

In words I'd describe this as follows. 
Attempting an adventure consists of multiple rounds of dice rolling, at each round you attempt to
match the result shown on the dice to any of the tasks (or just the current task if its an ordered Adventure).
You finish the attempt when you've either run out of dice (failure) or completed all tasks (success).

If you can't match the result of your roll to any of the tasks you have a few options.
1. Use a Clue (a consumable item) to re-roll any number of dice and then check again for matches.
2. "Focus" a single dice by setting it aside and not re-rolling it in the next round.
After an unsuccessful round with no matches you must discard a dice of your choice from the dice pool.
Both of these options involve some player choice, however in both cases it seems like the obvious choice is to
re-roll only the un-matched dice/focus a matched dice. 
If you fail a round and your result contains a "terror" symbol (looks like some tentacles) then you trigger the
Terror effect printed on the Adventure (if any).
   
If you can match one or more tasks to the result of you roll you must choose one of the tasks to complete by placing 
the matched dice on the corresponding symbols of the task.
Dice used this way are not used in any further rounds of the Adventure and the task is consider complete.

Matching the dice is not entirely trivial.
There are three kind of dice with a slightly different set of symbols (see chart below);
Lore, Peril and Terror results must be matched 1:1 with task symbols but Investigation results are numbered
and can be added together for many:1 matching.

[Dice Sides chart from the rulebook]

Hopefully you can see from this section why I took a Monte Carlo approach to this problem.
Calculating the probability of succeeding a single task given a set of dice is easily achievable with a bit of 
combinatorics but calculating the success probability of a whole Adventure is much harder.
The focus mechanic, the option to do partial re-rolls using Clue items and the possibility of triggering Terror effects 
all tip the scales in favour of a Monte-Carlo over analytic approach.

### Choose your adventures carefully

It's relatively easy to rank the available Adventures in terms of difficulty using a proxy like the minimum number 
of dice needed to succeed at an adventure, yet it's impossible for mere-mortals like myself to
work out the concrete success probability of an Adventure in my head.
Furthermore, it's unclear how to assess the relative value of the rewards vs penalties of a particular card
and hence completely impossible to put Adventure selection (which is pretty much the entirety of the game)
on a quantitative footing.
I suspect this design was intentional on the behalf of the game-designers to make it difficult for munchkins like 
me to metagame too hard.
Well, all I can say is that they didn't try hard enough.


# Method - the Monte-Carlo virtual casino

- One paragraph history of Monte Carlo method, maybe throw in a good quote or two

## Technical details

I implemented the core mechanics of Elder Sign in Python ([Github](https://github.com/oscarknagg/eldersign)).
To get the data for this blog post was a simple as setting running simulations of Adventure attempts for each Adventure
card under a range of scenarios (i.e. number of dice/clues available).
I recorded the success/failure of each attempt + a before/after snapshot of the board state as parquet files.
If you're a `pandas` user I'd strongly recommend serialising your dataframes as parquet instead of csv, in my case
this reduced the storage of the raw results data from 3.5GB to ~0.5GB.

Due to the _embarassingly parallel_ nature of Monte Carlo I was able to get a linear speedup proportional to the 
number of processors on my machine by using the Python `multiprocessing` library to assign each core to run simulations
independently. On my Ryzen 3950X (16C/32T) I was able to run 8192 attempts for each Adventure/scenario (98*11) pair in just
over 3 minutes.

## Assigning values in Elder Sign equivalents

Once I'd acquired this raw data there was a single missing step - converting the diverse rewards/penalties into a 
single scalar value.
To do this I treated acquiring an Elder Sign as having a value of 1 and rescaled all other rewards/penalties around that.
The base game (before expansions) used to let you exchange 10 trophy points for an Elder Sign but this was removed 
for being too easy (and also a boring mechanic as it let you grind easy, low-risk adventures only and still win).
Hence I've set the value of a trophy point as 1/12 Elder Sign equivalents.
Luckily, the shop lets you exchange trophy points for various items and I use the rates in the shop to fix the items.
I've also assigned a value to having a red/yellow dice that to incorporate the opportunity cost of spending an item to
get a red/yellow dice when attempting an adventure.
This is important as otherwise this analysis would always recommend spending all of your items on adventure to boost
your success probability, even for already easy adventures where the marginal success probability improvement 
might not be worth spending an item.

[Value table]

This approach is reminiscent of [material values](https://en.wikipedia.org/wiki/Chess_piece_relative_value) in chess, 
where each piece on the board is assigned a numerical value and the total value of the board is just the sum of over
all pieces.
This analysis is limited in chess, as it doesn't account for piece position or interaction effects where a set of 
pieces can be considered more or less valuable than the sum of their parts.
Similarly, this analysis is limited for Elder Sign as it doesn't account for the stage of the game, 
earlier you care more about items but when you're within striking distance of victory you will care more about 
Elder Signs.

# Results - adventures
## Adventure difficulty cheat sheet

- Matrix of n-symbols vs item-setup 
- Can I make it even simpler?
    - i.e. just number of symbols + some second order effects such as S vs 1/2/3/4
    - Matrix of n-symbols vs item-setup  
- Rule of thumb for some effects such as 
    - Ordered vs unordered
    - Terror: fail this adventure
    - Can I factor out a substitution rule for S/1/2/3/4
- Rule of thumb I've used is to count number of total dice needed to complete
    - What about second order effects? Is an S/SSS easier than SS/SS?


## Adventure tier list


# Results - understanding mechanics

## Dice vs clues

## Focusing, is it a big deal?

# Conclusion

- Limitations of the analysis
- My thoughts on the game
- Link to code
