---
layout: post
title: "Measuring overfitting in multi-agent reinforcement learning"
date: 2020-09-07
excerpt: "While it is possible to use self-play to learn effective policies with little human input, agents can get stuck in local optima
and overfit to opponent's policies."
tags: [reinforcement learning, machine learning]
comments: false
---

Self-play in reinforcement learning is a powerful yet tricky to use tool.
While it is possible to learn effective policies with little human input, agents can get stuck in local optima
and overfit to opponent's policies.
In this blog post I use (and extend) a recently developed metric for measuring overfitting in multi-agent
reinforcement learning - _joint policy correlation_ - to quantify the policy improvement from two
simple modifications to vanilla self-play.
The first improvement is early-stopping, a ubiquitous method from supervised learning where training is 
stopped before test loss starts to increase.
The second improvement is pool-training, where the self-play opponent is randomly swapped out from a 
pool of opponent policies (that are being trained concurrently).
The combination of these two simple improvements yields a reduction in overfitting that is comparable to 
more complex methods. 


# Introduction

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

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2020-09-07-joint-policy-correlation/jpc-matrix-example.png)

<center><i>An example JPC matrix.</i></center>

The authors define average proportional loss as \\( R_{-} = (\bar{D} - \bar{O}) / \bar{D} \\) where \\(\bar{D}\\)
is the average value of the diagonals and \\(\bar{O}\\) is the average value of the off-diagonals entries and
use this value as the primary performance criteria. 
However I’d argue that its much more important to look at the absolute magnitude of the off-diagonal reward as the 
key performance metric as a set of \\(D\\) random, untrained pairs of policies will result in a complete lack of overfitting 
(i.e. \\(R_{-} = 0\\) ) but also useless policies.


# Method

For this blog post I measured overfitting in two first-person, gridworld, multi-agent environments, 
one co-operative and one competitive. 
The experiments for each environment were repeated for 3 different “maps” with the same dynamics but different sizes 
and levels of partial observability.  

The first environment is `laser_tag` which is a reproduction of the environment of the same name from 
“A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning” .
At the beginning of each episode each of the two agents start on a random spawn point. 
Agents are available to rotate, move in all 4 directions, fire an endless light-beam in their current facing direction 
and perform a no-op. 
If an agent is tagged by another agent's light beam twice that agent is teleported to a random spawn point 
and the source agent is given 1 reward. 
Agents do not receive a negative reward for being tagged and all actions are executed simultaneously 
then resolved in a random order.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2020-09-07-joint-policy-correlation/laser-tag-maps.png)

<center><i>`small2`, `small3` and `small4` maps for the `laser_tag` environment.</i></center>

The second environment is `harvest` which has the same actions as laser_tag but the “fire” action is replaced with a 
“harvest” action. 
Plants (represented by a dark green square) are scattered throughout the environment and if both agents stand within 1 
square of a fruit and simultaneously perform the “harvest” action then the fruit will disappear and both agents 
will receive 1 reward. 
Plants respawn at a fixed frequency that decreases with increased map size.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2020-09-07-joint-policy-correlation/harvest-maps.png)

<center><i>`small2`, `small3` and `small4` maps for the `harvest` environment.</i></center>

Both environments are implemented (see my earlier [blog post](https://towardsdatascience.com/learning-to-play-snake-at-1-million-fps-4aae8d36d2f1))) 
purely with vectorised matrix operations in PyTorch and hence can be run at high levels of batching on a GPU, 
the environment batch size used in this work is 128. 
The architecture of all agents is a 3 layer convolutional network with strides (2, 1, 1) and kernel sizes (4, 5, 3) 
followed by a flattening and Gated Recurrent Unit. 
All agents are trained with PPO.


# Results
## Early stopping

In supervised learning it is typically observed that both train and test loss decrease early in training while later on 
test loss increases while train loss stagnates or decreases only slowly. 
Early stopping is a commonly applied form of regularisation in which training is stopped when test loss begins to increase. 
The same approach can be applied to non zero-sum multiagent games as well if we use diagonal and off-diagonal returns 
in place of train and test loss.

The figure below shows a typical example of a training run from this work (environment=`harvest`, map=`small3`). 
Note that the diagonal return increases monotonically with training whereas the off-diagonal return peaks much earlier in training, 
indicating that agents trained in this way increasingly overfit to each other's behaviour with continued training. 

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2020-09-07-joint-policy-correlation/overfitting-with-training-steps.png)

The figure below shows the percentage improvement in off-diagonal mean episodic return due to early stopping for all size 
(environment, map) combinations.
Note that in order to reduce experimentation time I aimed to train policies until just after maximum off-diagonal reward. 
Hence these numbers could be boosted arbitrarily by say, training all policies for N times as many steps so the 
off-diagonal return would drop further.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2020-09-07-joint-policy-correlation/early-stopping-improvement.png)


## Agent-pool training

An obvious method to reduce the level of overfitting to a single self-play opponent is to not train against a single 
opponent but a pool of opponents, randomly swapping opponents in each episode. 
The generalisation ability of agents trained by pool training can be assessed by examining a JPC matrix as before, 
however in the pool training case some off-diagonal entries can contain returns of two agents which have co-trained. 
Hence, I generalise JPC to block-diagonal JPC where diagonal (i.e. train) return becomes block-diagonal return which 
is the mean of block-diagonal entries with a block size of N-pool. 
Off-diagonal (i.e. test) return is simply the mean of entries not in the block diagonal. 

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2020-09-07-joint-policy-correlation/block-diagonal-jpc-matrix.png)
<center><i>
The figure above shows an example of a block-diagonal JPC matrix containing 16 agents trained in a pool size of 4 where 
darker red indicates greater return. 
The return difference between agents trained in the same pool and in other pools can be seen clearly.
</i></center>

The figure below summarises the pool-training results, 
each plot in the figure shows the diagonal and off-diagonal reward for agents trained in different pool sizes. 
Note that the off-diagonal return increases with pool size in every case except laser_tag-small2. 
The diagonal reward stays roughly constant except for the interesting Harvest-small4 case, as D and O both increase. 
Visual inspection of training runs shows that the reason is for this that the diversity of agents within a pool drives improved exploration. 
In a pool size of 1 a pair of agents typically converges into following a fixed route between 3 plants in the environment, 
these routes typically differ between training runs. 
In pool training agents have to learn to co-operate with agents that have learnt a different path between the plants, 
leveraging the exploration of other agents to reach a greater total number of plants.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/2020-09-07-joint-policy-correlation/pool-size-improvement.png)


## Visualising joint policy correlation

TODO: need more GIFs

# Discussion

TODO


