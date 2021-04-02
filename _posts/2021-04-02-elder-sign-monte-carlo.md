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

### Anatomy of an adventure


### Choose your adventures carefully

Verbally explain tradeoffs and intuitive strategy + what are the difficulties
- Success probability, rewards and penalties
- Overspending
- Intuitive strategy of building up items first on easy adventures then going for the difficult ones

### Example

# Method - rolling the virtual die

- Build a basic simulator of the game 
- Record before and after states (can't just record success fail as e.g. sometimes you won't use all clues available)
- Minor tech flex (multiprocessing, parquet,)

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

My thoughts
