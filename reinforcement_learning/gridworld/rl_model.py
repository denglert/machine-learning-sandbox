#!/usr/bin/env python
"""
Module containing implementation for the small gridworld example
"""

import numpy as np
import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import namedtuple

RIGHT = (1,0)
DOWN = (0,-1)
LEFT = (-1,0)
UP = (0,1)

ACTION_LABELS = { 
                    (-1,  0): '←', 
                    ( 1,  0): '→', 
                    ( 0, -1): '↓', 
                    ( 0,  1): '↑', 
                    (-1,  1): '↖', 
                    ( 1,  1): '↗', 
                    ( 1, -1): '↘', 
                    (-1, -1): '↙',
                }


possible_actions = [
                        (-1,  0),
                        ( 1,  0),
                        ( 0, -1),
                        ( 0,  1),
                        (-1,  1),
                        ( 1,  1),
                        ( 1, -1),
                        (-1, -1)
                     ]


Wind = namedtuple('Wind', ['direction', 'strength'])

class UnknownActionException(Exception):
    
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(UnknownActionException, self).__init__(message)



# - state transition
# state_transitions = { 
#                           state   action   newstate1   p1   newstate2  p2
#                         ( (1,1),  (1,0)) : { (2,1) :   0.9, (1,1,) :  0.1}
#                     }

class Environment:
    
    def __init__(self,
                 agent_position = (0,0),
                 target_position = (4,4),
                 gridsize    = (4,4),
                 walls       = [],
                 winds       = {},
                 Preward      = "default",
                 Ptransition = "default"):
        """Initialize the environment."""

        self.gridsize = gridsize
        self.gridwidth = gridsize[0]
        self.gridheight = gridsize[1]
        self.nblocks = gridsize[0]*gridsize[1]

        # In this simple gridworld the state of the environment can be fully described by the
        # position of the agent
        self.agent_position = agent_position
        self.state = self.agent_position

        # - List of the positions of the wall block elements
        self.walls = walls
        self.winds = winds

        # Similarly the statespace of the environment is the set of agent states
        self.statespace = [(x,y) for x in range(self.gridwidth) for y in range(self.gridheight) if self.is_position_allowed((x,y))]

        # - Target position
        self.target_position = target_position

        ########################################
        ## -- Reward distribution function -- ##
        ########################################

        # - Default reward assignment:
        # - Every possible action, state pair results in -1 reward
        # - signifying one step of the agent.
        if Preward == "default":
            self.Preward = lambda agent_action, agent_state: -1
        # - You can also pass your custom reward distribution function
        # - It should accept two inputs:
        #  - action: (dx,dy)
        #  - state: (x,y)
        else:
            self.Preward = Preward


        ########################################################
        ## -- Transition probability distribution function -- ##
        ########################################################

        if Ptransition == "default":
            self.Ptransition = self.generate_default_Ptransition()
        else:
            self.Ptransition = Ptransition

#       self.rewards = -np.ones(shape=(self.width, self.height, self.nactions))
#       self.states = np.array([(x,y) for x in range(self.width) for y in range(self.height)])
#       self.actions = np.array( [[[range(4)] for y in range(self.height)]] for x in range(self.width) )

        self.agent_position = agent_position

#   def Ptransition_deterministic(self, agent_action, agent_position):

#       if agent_action == RIGHT:
#           agent_position_candidate = (agent_position[0] + 1, agent_position[1]    )
#       elif agent_action == DOWN:
#           agent_position_candidate = (agent_position[0],     agent_position[1] - 1)
#       elif agent_action == LEFT:
#           agent_position_candidate = (agent_position[0] - 1, agent_position[1]    )
#       elif agent_action == UP:
#           agent_position_candidate = (agent_position[0],     agent_position[1] + 1)
#       else:
#           raise UnknownActionException("Unknown action '{}'".format(action))

#       # - Accept new position candidate
#       if self.is_position_allowed(agent_position_candidate):
#           return agent_position_candidate
#       # - Agents stays where it is currently
#       else:
#           return agent_position

    def is_position_allowed(self, position):
        """Check if a proposed position is allowed."""
        x, y = position

        if x < 0:
            return False
        if x >= self.gridwidth:
            return False
        if y < 0:
            return False
        if y >= self.gridheight:
            return False

        if position in self.walls:
            return False

        return True

    def update(self, action):
        """Receive agent's action signal, update internal representation,
        send reward and new state to agent."""

        reward = self.Preward(action, self.agent_position)

        state = self.agent_position

        choices = list(self.Ptransition[(state, action)].keys())
        probabilities = list(self.Ptransition[(state, action)].values())
        new_position = choices[np.random.choice(a=len(choices), size=1,
                p=probabilities)[0]]

        self.agent_position = new_position

        return new_position, reward


    def generate_default_Ptransition(self):
        
        Ptransition = {}
        
        for state in self.statespace:
            for action in possible_actions:

                if state in self.winds:
                    Ptransition[(state, action)] = self.gridworld_dynamics(state, action,
                            wind_direction=self.winds[state].direction, wind_strength=self.winds[state].strength)
                else:
                    Ptransition[(state, action)] = self.gridworld_dynamics(state, action,
                            wind_direction=None, wind_strength=None)

        return Ptransition


    def gridworld_dynamics(self, position, action, wind_direction=None, wind_strength=None):
        """Constructs the possible probability space given the 
            - position: current position of the agent
            - action: action of the agent 
            - wind_direction: direction of the wind 
            - wind_strength: strength of the wind
            Returns a dictionary containing the possible states and their associated probabilities
            in the format:
                {
                    position1 : probability1,
                    position2 : probability2,
                    ...
                }."""

        transition_probabilities = {}
    
        # - Accounting for wind effect
        if wind_direction is not None:

            # - New position aligns with agent's intention
            prob1 = 1.0 - wind_strength
            pos1  = (position[0]+action[0], position[1]+action[1])

            # - New position, shifted by the wind
            prob2 = wind_strength
            pos2  = (pos1[0]+wind_direction[0], pos1[1]+wind_direction[1])

            transition_probabilities[pos1] = prob1
            transition_probabilities[pos2] = prob2

        # - There is no wind on this block
        else:
            pos = (position[0]+action[0], position[1]+action[1])
            prob = 1.0

            transition_probabilities[pos] = prob


        not_allowed_states = [state for state in transition_probabilities.keys() if state not in self.statespace]
        for pos in not_allowed_states:
            transition_probabilities.pop(pos)

        # - If neither of the new positions are not allowed then stay in place with probability 1.0
        if not transition_probabilities:
            transition_probabilities[position] = 1.0


        transition_probabilities = normalise_dict_values(transition_probabilities)

        return transition_probabilities

    
    def plot(self, figsize=(2,2)):
    
        fig, ax = plt.subplots(figsize=figsize)

        ax.set_xlim(0.0, self.gridwidth)
        ax.set_ylim(0.0, self.gridheight)
        ax.set_xticks(range(0,int(self.gridwidth)))
        ax.set_xticklabels('')
        ax.set_yticks(range(0,int(self.gridheight)))
        ax.set_yticklabels('')

        # - Agent
        agent_square = mpatches.Rectangle(self.agent_position, 1, 1, linewidth=1, facecolor='blue')
        ax.add_patch(agent_square)
        agent_label_pos_x = self.agent_position[0] + 0.5
        agent_label_pos_y = self.agent_position[1] + 0.5
        ax.text(agent_label_pos_x, agent_label_pos_y, 'A', fontsize=16,
                horizontalalignment='center', verticalalignment='center')


        # - Target
        target_square = mpatches.Rectangle(self.target_position, 1, 1, linewidth=1, facecolor='green')
        ax.add_patch(target_square)
        target_label_pos_x = self.target_position[0] + 0.5
        target_label_pos_y = self.target_position[1] + 0.5
        ax.text(target_label_pos_x, target_label_pos_y, 'T', fontsize=16,
                horizontalalignment='center', verticalalignment='center')

        # - Walls
        for wall in self.walls:
            wall_square = mpatches.Rectangle(wall, 1, 1, linewidth=1, facecolor='grey')
            ax.add_patch(wall_square)
            wall_label_pos_x = wall[0] + 0.5
            wall_label_pos_y = wall[1] + 0.5
            ax.text(wall_label_pos_x, wall_label_pos_y, 'W', fontsize=16,
                    horizontalalignment='center', verticalalignment='center')


        # - Winds
        for position, wind in self.winds.items():
            arrow = mpatches.Arrow(position[0], position[0], wind.direction[0]*wind.strength,
                    wind.direction[1]*wind.strength, linewidth=1, facecolor='skyblue')
            ax.add_patch(arrow)


        plt.grid()

        return fig, ax


class Agent:
    
    def __init__(self, environment, initial_pos, policy, gamma=1.0):
        self.environment = environment
        self.current_state = initial_pos
        self.time_step = 0
        self.gamma = gamma
        self.recent_reward = 0.0
        self.gain = 0.0
        self.policy = policy
        self.experience = []
    
    def get_current_state(self):
        return self.current_state  
        

    def action(self, action, doPlot=False, figsize=(2,2)):
        new_state, reward = self.environment.update(action)

        new_experince = (action, reward, new_state)
        self.experience.append(new_experince)
        self.current_state = new_state

    def actions(self, actions, doPlot=False, figsize=(2,2)):

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

    def follow_policy(self, nsteps):
        
        for step in range(nsteps):
            action = self.policy(self.current_state)
            print("Action: {}".format(action))
            self.action(action)


class DiscreteStochasticProcess:

    def __init__(self, probabilities, values):
        self.probabilities = probabilities
        self.values = values


    def rvs(self, state, action):

        sample = np.random.choice(a=values[(state, action)], size=1,
                p=probabilities[state_action_tuple])[0]

        return sample


    def prob(self, state, action):
        return probabilities[(state, action)]



class StateTransition(DiscreteStochasticProcess):

    def __init__(self, gridsize, wind, actions):

        probabilities = {}
        values = {}

        gridwidth = gridsize[0]
        gridheight = gridsize[1]
        
        for state in itertools.product(range(gridwidth), range(gridheight)):
            for action in actions:
                
                values[(state, action)] = state + action
                probabilities[(state, action)] = 1.0
                

        super().__init__(probabilities, values)




        

        

    


def get_possible_state(state):

    nearby_state






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



def normalise_dict_values(dict, norm=1.0):

    normalised_dict = {}

    s = sum(dict.values())

    for key, value in dict.items():
        normalised_dict[key] = value/s

    return normalised_dict


###################################################

def random_policy(state):
    choices = possible_actions
    action = choices[np.random.choice(len(choices))]
    return action


def policy_evaluation(environment, policy, initial_value_function):
    
    value_function = initial_value_function
    value_function_shape = value_function.shape
    
    for state in environment.states:

        state_x = state[0]
        state_y = state[1]
        
#       for 
        
#       value_function 




