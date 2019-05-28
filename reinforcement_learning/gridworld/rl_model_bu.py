#!/usr/bin/env python
"""
Module containing implementation for the small gridworld example
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class UnknownActionException(Exception):
    
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(UnknownActionException, self).__init__(message)


class Environment:
    
    def __init__(self, agent_state, size=(4,4)):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.nblocks = size[0]*size[1]
        self.nactions = 4
        self.rewards = -np.ones(shape=(self.width, self.height, self.nactions))
        self.states = np.array([(x,y) for x in range(self.width) for y in range(self.height)])
        self.actions = np.array( [[[range(4)] for y in range(self.height)]] for x in range(self.width) )
        self.agent_state = agent_state
    
    def possible_actions(self, state):
        return self.action[state[0], state1]
    
    def transition(self, current_state, action):
        
        if action == 0: # left
            new_x = max(0, current_state[0] - 1)
            new_y = current_state[1] 
        elif action == 1: # right
            new_x = min(self.width-1, current_state[0] + 1)
            new_y = current_state[1]
        elif action == 2: # down
            new_x = current_state[0]
            new_y = max(0, current_state[1] - 1)
        elif action == 3: # up
            new_x = current_state[0]
            new_y = min(self.height-1, current_state[1] + 1)
        else:
            raise UnknownActionException("Unknown action '{}'".format(action))
            
        new_state = (new_x, new_y)
        
        return new_state
    
    def update(self, action):
        reward = self.rewards[self.agent_state[0], self.agent_state[1], action]
        self.agent_state = self.transition(self.agent_state, action)
        return self.agent_state, reward
    
    def plot(self, figsize=(2,2)):
    
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlim(0.0, self.width)
        ax.set_ylim(0.0, self.height)
        ax.set_xticks(range(0,int(self.width)))
        ax.set_xticklabels('')
        ax.set_yticks(range(0,int(self.height)))
        ax.set_yticklabels('')

        # - Agent
        agent_square = mpatches.Rectangle(self.agent_state, 1, 1, linewidth=1, facecolor='grey')
        ax.add_patch(agent_square)
        agent_label_pos_x = self.agent_state[0] + 0.5
        agent_label_pos_y = self.agent_state[1] + 0.5
        ax.text(agent_label_pos_x, agent_label_pos_y, 'A', fontsize=16,
                horizontalalignment='center', verticalalignment='center')

        plt.grid()

        return fig, ax


class Agent:
    
    def __init__(self, environment, policy, gamma=1.0, initial_pos=(1,1)):
        self.environment = environment
        self.current_state = initial_pos
        self.time_step = 0
        self.gamma = gamma
        self.recent_reward = 0.0
        self.gain = 0.0
        self.policy = policy
    
    def get_current_state(self):
        return self.current_state  
        
    def act(self, actions, doPlot=False, figsize=(2,2)):

        for action in actions:
            new_state, reward = self.environment.update(action)
            self.current_state = new_state
            self.recent_reward = reward
            self.gain += ((self.gamma)**(self.time_step))*reward
            self.time_step += 1 

            if doPlot:
                self.environment.plot(figsize=figsize)
        
    def set_policy(self, policy):
        self.policy = policy

    def reset(self):
        self.recent_reward = 0.0
        self.time_step = 0
        self.gain = 0.0

        
    def make_nsteps(self, nsteps):
        
        for step in range(nsteps):
            action = self.policy(self.current_state)
            print("Action: {}".format(action))
            self.act(action)



class Policy:
    """Determines the action in a given state
       Policy is stored in a dictionary:
       - key: agent_state [tuple]
       - value: list of probabilities of a given action (action is given by the end)
       """

    def __init__(self, policy):
        self.policy = policy
    
    def sample(self):
        action = np.random.multinomial(n=self.nactions, pvals=self.probabilities)
        return action
    
    def probabilities(self, state):
        return self.probabilities


def random_policy(state):
    action = np.random.randint(0,3)
    return [action]


def policy_evaluation(environment, policy, initial_value_function):
    
    value_function = initial_value_function
    value_function_shape = value_function.shape
    
    for state in environment.states:

        state_x = state[0]
        state_y = state[1]
        
#       for 
        
#       value_function 


ACTION_LABELS = { 
    (-1,  0): '←', 
    ( 1,  0): '→', 
    ( 0, -1): '↓', 
    ( 0,  1): '↑', 
}

actions = ['left', 'right', 'up', 'down']
