---
layout: post
title: "Measuring overfitting in multi-agent reinforcement learning"
date: 2020-09-07
excerpt: "Sample post."
tags: [reinforcement learning, machine learning]
comments: false
---

Abstract

Introduction
------------

Self-play is a method of training RL algorithms where an agent repeatedly plays a game against itself and uses 
the experience generated to improve its policy. 
This requires relatively little human input as it's possible to start with an untrained (i.e. completely random) agent
that learns and explores the game from a blank slate.
 
The archetypal self-play success of recent years is [AlphaGo](https://www.nature.com/articles/nature16961) 
(and its successors [AlphaZero](https://deepmind.com/blog/article/alphazero-shedding-new-light-grand-games-chess-shogi-and-go) 
and [MuZero](https://arxiv.org/abs/1911.08265)) which was 
the first computer program to beat a human professional in the ancient game of Go in 2016. 
However self-play has seen good results as far back as 1992 when TD-Gammon achieved professional level play in Backgammon 
through temporal difference learning. 
Self-play has also achieved breakthrough successes in real-time-strategy video games such as 
[Starcraft](https://deepmind.com/blog/article/alphastar-mastering-real-time-strategy-game-starcraft-ii) and 
[Dota 2](https://openai.com/projects/five/) which have much larger action spaces than chess or Go and are 
partially-observable to boot.

Relatively little work has been done on studying overfitting in (multiagent) reinforcement learning - 
something I attribute to the fact that most academic benchmarks have no train/test distinction. 
A notable exception to this is 
“[A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning](https://arxiv.org/pdf/1711.00832.pdf)” 
which introduces a new metric, joint policy correlation (JPC), to quantify overfitting in multiagent RL and 
also a theoretically motivated algorithm, Deep Cognitive Hierarchies (DCH), to train agents with low JPC.

JPC is measured by constructing a JPC matrix - a square matrix of size D. 
To do this D instances of the same self-play experiment are run, differing only in the random seed. 
Each of the D experiments produces two policies \\( (\pi^d_{1}, \pi^d_{2}) \\). 
The value in row i and column j of the JPC matrix is the mean return (i.e. total undiscounted reward) over many episodes 
when player 1 uses policy \\( \pi_{1}^{d_i} \\) and player 2 uses policy \\( \pi_{2}^{d_j} \\).
Entries on the diagonal represent the returns for policies that were trained together, 
i.e. a train-set performance metric and off-diagonal elements show returns for policies that were not trained together, 
i.e. a test-set performance metric.

Example image here

The authors define average proportional loss as \\( R_{-} = (\bar{D} - \bar{O}) / \bar{D} \\) where \\(\bar{D}\\)
is the average value of the diagonals and \\(\bar{O}\\) is the average value of the off-diagonals entries and
use this value as the primary performance criteria. 
However I’d argue that its much more important to look at the absolute magnitude of the off-diagonal reward as the 
key performance metric as a set of \\(D\\) random, untrained pairs of policies will result in a complete lack of overfitting 
(i.e. \\(R_{-} = 0\\) ) but also useless policies.


Method
------

For this blog post I measured overfitting in two first-person, gridworld, multi-agent environments, 
one co-operative and one competitive. 
The experiments for each environment were repeated for 3 different “maps” with the same dynamics but different sizes 
and levels of partial observability.  

The first environment is laser_tag which is a reproduction of the environment of the same name from 
“A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning” .
At the beginning of each episode each of the two agents start on a random spawn point. 
Agents are available to rotate, move in all 4 directions, fire an endless light-beam in their current facing direction 
and perform a no-op. 
If an agent is tagged by another agent's light beam twice that agent is teleported to a random spawn point 
and the source agent is given 1 reward. 
Agents do not receive a negative reward for being tagged and all actions are executed simultaneously 
then resolved in a random order.

Laser-tag images


