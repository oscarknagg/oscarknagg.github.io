---
layout: post
title: "A Monte Carlo analysis of the board game Elder Sign"
date: 2021-04-02
excerpt: "Sample text."
tags: [monte carlo, gaming]
comments: false
---

*Status: WIP*

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
including Lovecraft favourites such as Cthulu and Azathoth as well as some newly invented ones with a similar vibe.
A single playthrough involves only a single Ancient One and ends in defeat when the Ancient One acquires a certain number
of Doom Tokens.
Conversely, the game ends in a victory when a certain number (typically around 10) of Elder Signs are placed 
on the Ancient One, sealing it away for good.
Essentially, Elder Signs and Doom Tokens function as independent victory and loss tracks and you want to maximise the
number of the first and minimise the number of the latter.
Each of the Ancient Ones has a special ability that impacts the game and a different number of Elder Signs/Doom Tokens
required to win/lose - I've not attempted to include these points in my analysis.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2021-04-02-elder-sign-monte-carlo/ancient-one-example.png)


## Investigators and items

Investigators are the player controlled characters and have two independent "hitpoints", health and sanity. 
If either of these reach 0 the character dies and is replaced with a new one - in order for this to have consequences, 
dieing also triggers a penalty in the form of a Doom Token.
Investigators can accumulate items of various kinds throughout the game by completing Adventures,
the majority of which are consumables that provide single-use benefits when attempting Adventures.
Like Ancient Ones, there's a large selection of Investigators with differing amounts of health/sanity hitpoints, 
special abilities and starting items.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2021-04-02-elder-sign-monte-carlo/investigator-example.png)

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

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2021-04-02-elder-sign-monte-carlo/adventure-card-anatomy.png)


### Attempting Adventures

So how does one actually attempt an Adventure?
In a nutshell it involves repeatedly rolling a set of non-standard dice and matching symbols on the dice
to symbols on the Adventure card.

Attempting an adventure consists of multiple rounds, at each round you attempt to
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
Dice used this way are not used in any further rounds of the Adventure and the task is considered complete.

Matching the dice is not entirely trivial.
There are three kind of dice with a slightly different set of symbols (see chart below);
Lore, Peril and Terror results must be matched 1:1 with task symbols but Investigation results are numbered
and can be added together for many:1 matching.
The chart below shows the three kinds of dice and what symbols are on each one, 
note that the yellow and red dice are slightly more valuable than the default green dice.  

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2021-04-02-elder-sign-monte-carlo/dice-sides.png)

To help solidify this in your mind, here's an example of completing a task from the rulebook.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2021-04-02-elder-sign-monte-carlo/completing-task-example.png)


If you're a programmer like me then it will help to see the algorithm for attempting an Adventure as pseudocode.

<details>
<summary>Adventure attempt pseudocode.</summary>

```
def attempt_adventure(tasks, dice, clues)
    while len(dice) > 0 and len(tasks) > 0:
        dice_result: List[Symbol] = dice.roll()
        matched_tasks: Dict[Task, Dice] = tasks.match(dice_result)
        if len(matched_tasks) > 0:
            completed_task, used_dice = select_task_to_complete(matched_tasks)
            dice.remove(used_dice)
            tasks.pop(completed_task)
        else:
            if clues > 0:
                # Clues let's
                clue_policy(dice)
                continue
                
            focus_policy(dice)
            dice.pop()  # Remove one dice
            
        if len(tasks) == 0:
            return SUCCESS
        else:
            return FAILURE
```

</details>

#### Randomness in adventures

As you can see, adventuring involves a lot of randomness and although the game does include a few opportunities 
for player choice in attempting an Adventure, 
the skill cap of these choices is low (there's an obviously correct action in most cases) and their effect is quite small.
As the player has relatively little control over the outcome of an Adventure once it's started the most important 
choices are what Adventures to attempt and what consumable items to use for the attempt.
Some items grant additional dice to be used during the attempt and these have to be used in advance of the attempt.
Clue items can also be used during the Adventure but do not have to be commited in advance.
Even though player choice is limited, 
its still crucial to understand the internals of Adventures in order to estimate success probabilities.

Hopefully you can see why I took a Monte Carlo approach to this problem.
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

The scenarios I simulated are listed below and span from a weak board position (green dice locked)
to a very strong board position (geared + blessed).
This is not an exhaustive range of scenarios but I'd say about 99% of board positions in a particular playthrough
will fall in this range.

| Scenario              | Green Dice | Yellow Dice | Red Dice | Clues |
|-----------------------|------------|-------------|----------|-------|
| Green Locked (cursed) | 5          | 0           | 0        | 0     |
| Default               | 6          | 0           | 0        | 0     |
| Blessed               | 7          | 0           | 0        | 0     |
| Yellow                | 6          | 1           | 0        | 0     |
| Red                   | 6          | 0           | 1        | 0     |
| Yellow+Red            | 6          | 1           | 1        | 0     |
| Clue                  | 6          | 0           | 0        | 1     |
| Clue*3                | 6          | 0           | 0        | 3     |
| Geared                | 6          | 1           | 1        | 1     |
| Geared+Blessed        | 7          | 1           | 1        | 3     |

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

| Object         | Value (Elder Signs)            | Comment                                                                                                      |
|----------------|--------------------------------|--------------------------------------------------------------------------------------------------------------|
| Elder Sign     | 1                              | Reference point                                                                                              |
| Doom Token     | -1.1                           | Slightly worse than an Elder Sign is good as acquiring one sometimes triggers additional negative penalties. |
| Trophy Point   | 1/12                           | Based on exchange rate in the base game shop                                                                 |
| 1 Health       | 0.75*1/12                      | Based on exchange rate in the First Aid Station                                                              |
| 1 Sanity       | 0.75*1/12                      | Based on exchange rate in the First Aid Station                                                              |
| Common Item    | 2/12                           | Based on exchange rate in the shop                                                                           |
| Unique Item    | 3/12                           | Based on exchange rate in the shop                                                                           |
| Spell          | 4/12                           | Based on exchange rate in the shop                                                                           |
| Ally           | 5/12                           | Based on exchange rate in the shop                                                                           |
| Clue           | 1/12                           | Based on exchange rate in the shop                                                                           |
| Blessed status | 8/12                           | Based on exchange rate in the chapel                                                                         |
| Cursed status  | -9/12                          | Similar effect to Blessed but opposite in direction                                                          |
| Monster        | -3/12                          | Equivalent to a ~1.5 symbol task being placed on an Adventure                                                |
| Red Dice       | 3.3/12                         | 10% more than a Unique item                                                                                  |
| Yellow Dice    | 2.2/12                         | 10% more than a Common item                                                                                  |

This approach is reminiscent of [material values](https://en.wikipedia.org/wiki/Chess_piece_relative_value) in chess, 
where each piece on the board is assigned a numerical value and the total value of the board is just the sum of over
all pieces.
This analysis is limited in chess, as it doesn't account for piece position or interaction effects where a set of 
pieces can be considered more or less valuable than the sum of their parts.
Similarly, this analysis is limited for Elder Sign as it doesn't account for the stage of the game, 
earlier you care more about items but when you're within striking distance of victory you will care more about 
Elder Signs.

# Results
## Adventures
### Difficulties

Just how difficult are Adventure cards, what are the hardest and easiest?
The chart below shows the cumulative distribution function (CDF) of the Adventure success probabilities
under a range of circumstances.
In the default, item-free, scenario adventures span from essentially impossible to almost guaranteed success.
However, in the strongest scenario even the hardest adventure has about a 35% chance of success.

The dashed lines are the 1/6th and 5/6th percentiles - where you'd expect the hardest and easiest adventure to be 
in the initial draw of 6 Adventure cards.
Players typically start with at least one of an extra red/yellow dice or a clue so I'd expect a board to contain
one adventure with an 80% chance of success.

From this chart we can also see the relative benefits of the yellow dice, red dice and clues and can see
that clue < yellow < red, just as the 1/2/3 pricing in the shop would suggest.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2021-04-02-elder-sign-monte-carlo/success-probability-distribution.png)

### Green-dice equivalents

The proxy I use for card difficulty while playing the game is the minimum number of green dice required to complete a
task AKA green-dice-equivalents or GDEs for short.
This is easily calculated as three times the total number of non-investigation symbols on an Adventure plus the 
number of investigations, all divided by 3.
A slightly better (but less simple) proxy is to treat a non-investigation symbol as 3.25 investigations as these
are the relative weights when doing linear regression to predict card success probability based on task symbols.

It turns out that GDEs are a relatively good proxy for Adventure difficulty - 
the chart below shows the success probability in the default, no item, scenario vs the GDE value of Adventures.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2021-04-02-elder-sign-monte-carlo/min-green-dice-heuristic.png)

The trend is not quite monotonic, with a Spearman's coefficient of 0.88, but it's pretty good!
The outliers from this trend illustrate some of the other factors that influence Adventure difficulty.

The three hardest Adventures with a GDE of 3 are shown below. 
`Something Has Broken Free` (P(success) = 0.18) is an ordered adventure so you can only match dice to the topmost incomplete task and
also has a terror effect (triggered on failing a task while your dice roll shows a terror symbol) that causes you
to fail the adventure entirely!
`You become that which you fear most` (P(success) = 0.28)  and `Ominous Portents` (P(success) = 0.29)  
have no unusual effects but each have a task requiring three dice to be matched simultaneously.
As I'll show in the next section the concentration of symbols within tasks is an important factor in card difficulty.

[something_has_broken_free, you_become_that_which_you_fear_most, ominous_portents]

On the flipside, the outliers on the easy side tend to have non-concentrated task symbols or are composed of 
mostly Investigation symbols which can be matched in multiple ways.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2021-04-02-elder-sign-monte-carlo/cheat-sheet.png)

<center>A "cheat sheet" of card difficulties vs GDEs for a range of item scenarios.</center>

### Factors influencing Adventure difficulty

We've seen that the green-dice equivalent is a simple yet fairly good proxy for Adventure difficulty,
what other factors influence difficulty and what rules can we discern?

To make this section I simulated various task layouts 1 million times each in the default no-item, 6 green dice scenario 
to determine their success probabilities.
I've developed a shorthand for task layouts with the following rules:
- `S` denotes a non-investigation symbol 
- A number denotes an investigation symbol with a particular value 
- `/` separates tasks

Note that we don't need to distinguish between symbols in the default scenario as they are all equally likely on the
green dice.
#### More concentrated tasks are harder

An Adventure has more "concentrated" tasks if more of the symbol requirements are located in a single task.
In general, if two Adventures contain the same number of symbols, the one with the more concentrated tasks is harder.
This rule holds for almost all printed cards with the exception that `SS/S` and `S/S/S` are about equally hard.
Also, `S/S/S/S` is harder than `SS/S/S` but no Adventure with tasks of the form `S/S/S/S` is printed anywhere 
(in the expansions I have).

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2021-04-02-elder-sign-monte-carlo/symbol-concentration.png)

#### Investigations are easier than other symbols but a mix is easier still

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2021-04-02-elder-sign-monte-carlo/symbols-vs-investigations.png)


#### Ordering makes relatively little difference
- Investigation easier than symbols
    - Result: Linear regression on symbols + investigation count to predict success proba weights 3.25:1
    - Simulations
        - S vs 3 vs 4 vs 5
            - (97.8% vs 99.9% vs 99.2% vs 97.3%)
        - SS vs S3 vs 6
            - (80.4% vs 90.2% vs 92.4%)
        - SSS vs SS3 vs S6 vs 9
            - (28.1% vs 50.2% vs 62.1% vs 46.0%)
        - SSSS vs SSS3 vs SS6 vs S9 vs 12
            - (2.9% vs 9.0% vs 16.5% vs 14.4% vs 6.3%)
- Ordered vs unordered
    - Unordered vs ordered for some representative tasks
        - S/S
        - SS/SS
            - Ordered: 14.1%, Unordered: 14.1%
        - SS/S
            - Ordered: 48.1%, Unordered: 57.6%
        - S/SS
            - Ordered: 49.0%, Unordered: 57.6%
        - SSS/S
        - S/SSS
            - Ordered: 8.5%, Unordered: 12.4%
        - S/S/SS
            - Ordered: 18.5%
        - SS/S/S
            - Ordered: 18.2%

### Expected returns on Adventure attempts

Now that we've got a good handle on what our chances of success are when attempting Adventures we can start to 
draw some conclusion about which particular adventures have positive or negative expected returns in different scenarios.
The chart below shows the CDF of the expected return in Elder Sign equivalents (ESEs) of all 98 Adventure cards for a 
range of different item scenarios.
The dashed lines are 1/6th and 5/6th percentiles - about where you'd expect the best and worst Adventure in a draw of 6.

The first thing that stands out to me is that a lot of the CDF is in the positive expected return region, for all scenarios.
This tells me that most of the time there will be a positive expected return Adventure (if you can identify it) and
this agrees with my anecdotal experience that the game is a little easy with ~75% of games ending in victory.

The unintuitive part of this chart is that the scenarios with the most items do not always have the best expected returns
due to the opportunity cost of spending those items.
In fact, the scenario with arguably the best returns is spending items to get just the yellow and red dice.
I think that I may have overestimated the opportunity costs in my value table

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2021-04-02-elder-sign-monte-carlo/expected-return-distribution.png)


S-tier
- Great hall of Celeano: Great rewards, middling difficulty but best of all is that there is a minimal failure penalty
- The elder sign: similar to above
- The dreamlands: really easy, few penalties so its basically an elder sign on a plate

A-tier

- Yuggoth: Amazing rewards with middle of the road penalties. However you need to be well prepared to attempt it which keeps it out of S
- Grazed writings: a very easy elder with few penalties. However less good peripheral rewards than the dreamlands
- Sudden Attack: Relatively easy, good rewards

B-tier

- Forgotten knowledge:


Trash tier

- Please do not touch the exhibits: Doom token terror effect and penalty
- Light's out: Incredibly difficult adventure for 1 elder sign. The fact that the penalty is a doom token and the max prob
    of success is < 0.5 even in the best scenario means this card never works out positive in expectation
- Too quiet:
- It's quiet


## Understanding game mechanics

### Dice vs clues

- Can extract relevant information from first success probability cdf chart
- Give a few charts of success probabilities for median card under defauly, yellow, red, clue
- Do I think shop prices are justified

### Focusing, is it a big deal?

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2021-04-02-elder-sign-monte-carlo/focus-success-probability-boost.png)

- Yes, see chart above

# Conclusion

- Limitations of the analysis
- My thoughts on the game
- Link to code
