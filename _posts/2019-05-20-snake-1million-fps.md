---
layout: post
title: "Learning to play snake at 1 million FPS"
date: 2019-05-20
excerpt: "Using advantage actor-critic to learn Snake in under 5 minutes on a massively parallel vectorised environment."
tags: [reinforcement learning, machine learning]
comments: false
---

In this blog post I’ll guide you through my most recent project, which combines two things I find fascinating — 
computer games and machine learning. 
For quite a while now I’ve wanted to get to grips with deep reinforcement learning and I thought there is no better way than to do my own project. 
To that end I implemented the classic mobile game “Snake” in PyTorch and trained a reinforcement learning algorithm to play it. 
This post is divided into three parts.
1. A massively parallel vectorized implementation of the Snake game
2. An explanation of Advantage Actor-Critic (A2C)
3. Results: analysing the behaviour of different agents

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/demo.gif)

_Code for this project is available at https://github.com/oscarknagg/wurm/tree/medium-article-1_ 

# Snake - vectorized

For all it’s impressive achievements, deep reinforcement learning is very slow. 
Incredible results have been achieved in complex games like DotA 2 and Starcraft but these have taken 1000s of years of gameplay. 
In fact even the work that sparked the current wave of interest in deep reinforcement learning, 
i.e. learning to play Atari games, required weeks of gameplay and 100s of millions of frames for each game.

A lot of research since then has been done towards speeding up deep reinforcement learning, 
both in terms of wall clock time by parallelisation and improved implementation and also in terms of sample efficiency. 
Many state of the art reinforcement learning algorithms are trained in multiple copies of an environment simultaneously, 
typically one per CPU core. This yields a roughly linear speed up in how fast you can generate gameplay experience with more CPU cores.

So in order to experiment with deep reinforcement learning you had better have either a lot of computational resources, 
a very fast/parallel environment or be willing to wait a long time. 
Since I don’t have access to a large cluster and want to see results fast I decided to create a vectorized implementation 
of Snake which can achieve a much greater level of parallelisation than the number of CPU cores.

## What is vectorization?

Vectorization is a form of single instruction, multiple data (SIMD) parallelism. 
For those of you who are Python programmers this is the reason that numpy operations can often be orders of magnitude 
faster than explicit for-loops that perform the same calculations.

Essentially, vectorization is possible because if a processor can perform operations on, say, 
256 bits of data in a singe clock cycle and your program’s real numbers are 32 bit single precision numbers 
then you can pack 8 of these numbers into 256 bits and perform 8 operations with each clock cycle. 
So if a program is clever enough to schedule instructions such that there are always 8 operands in place at the right 
time it should be able to achieve, in theory, an 8x speedup over executing instructions on one piece of data at a time.

## Implementation: Representing the environment

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/env-schematic.png)

The key idea is to represent the full state of the environment as a single tensor.
In fact multiple environments are represented as a single 4d tensor in the same way that a batch of images is represented. 
In the case of Snake each image/environment has three channels: one for food objects, 
one for snake heads and one for snake bodies as shown above. 
Doing this lets us leverage the many features and optimizations that PyTorch already has for manipulating this kind of data.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/env-schematic-rendered.png)

<center><i>The example above rendered with a black border. This is a smaller version of the input given to the agent.</i></center>

## Implementation: Moving the snake

So now that we have a way of representing the game environment we need to implement the gameplay using only vectorized tensor operations. 
The first trick is that we can move the position of all the snake heads in every environment by applying a 2D convolution 
with a hand crafted filter to the head channel of our environment tensor.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/env-move-conv.png)

However PyTorch only lets us apply the same convolutional filter to the whole batch but we need to be able to take a 
different action in each environment. 
Hence I apply a second trick to work around this limitation. 
First apply a convolution with 4 output channels (1 for every direction of movement) to each environment then use the 
very useful `torch.einsum` to “select” the correct action using a one-hot vector of actions. 
I’d highly recommend reading [this article](https://rockt.github.io/2018/04/30/einsum) for a very good introduction to 
Einstein summation and its uses in NumPy/PyTorch/Tensorflow.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/einsum.png)

<center><i>
The full head movement procedure. 
See [this gist](https://gist.github.com/oscarknagg/863602483afc83d698ce399a67eb21d4) for a minimal implementation.
</i></center>

Now that we moved the head we need to move the body. 
Firstly we move the tail (i.e. the 1 position on the body) forwards by subtracting 1 from all body locations then applying 
the ReLu function to keep the other elements above 0. 
Secondly we make a copy of the head channel, multiply it by the maximum body value plus 1. 
We then add this copy to the head channel which creates a new front position for the body (position 8 in the diagram).

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/body-movement.png)

<center><i>
Body movement procedure. 
The input action is left. See [this gist](https://gist.github.com/oscarknagg/627dbcfe020cc63dd47d57e1cf6b076c) for a minimal implementation.
</i></center>

## Environment simulation speed

There’s a bit more logic required such as checking for collisions and food collection, 
resetting environments after death and checking snakes aren’t trying to move backwards — 
it was very fun thinking of ways to implement all this in a way that is vectorized across multiple environments. 
The end result of all this optimisation is shown in the plots below. 
With a single 1080Ti and an environment of size 9 I can run a maximum of just over a million steps per second with a 
random agent and just over 70,000 steps/s while training a convolutional agent with A2C 
(using the same hyperparameters as for the later results).

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/env-speeds.png)

<center><i>
Clickbait title - justified [✓], not justified [  ].
</i></center>

# Advantage actor-critic (A2C)

_In this section I assume your familiar with the basic terminology of reinforcement learning e.g. value function, policy, rewards, returns etc._

The idea behind the actor-critic algorithm is simple. 
You train an actor network to map from observed states to a probability distribution over actions i.e. the policy. 
The aim of this network is to learn the best actions to take in a particular state.

At the same time you also train a critic network that maps from states to their expected value 
i.e. the sum of future rewards expected after being in this state. 
The aim of this network is to learn how desirable it is to be in a particular state. 
This network also stabilizes the learning of the policy network by providing a baseline value for states as we’ll see later.

![](https://raw.githubusercontent.com/oscarknagg/oscarknagg.github.io/master/assets/img/symbols-table.png)

<center><i>
Table of symbols to make reading the following part easier.
</i></center>

## Value function learning

The loss of the value function is the squared difference between the predicted value of a particular state and the actual (discounted) return generated from that state. 
Hence value function learning is a regression problem.



