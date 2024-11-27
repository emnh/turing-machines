#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

import os
import sys
import re

class TuringMachine:
    def __init__(self, states, alphabet, transitions, start_state, accept_state, reject_state, blank_symbol='_'):
        """
        Initialize the Turing Machine.
        :param states: A list of states.
        :param alphabet: A list of tape symbols, including the blank symbol.
        :param transitions: A dictionary representing the transition function.
                            Format: {(current_state, read_symbol): (new_state, write_symbol, direction)}
        :param start_state: The initial state of the Turing machine.
        :param accept_state: The accepting state.
        :param reject_state: The rejecting state.
        :param blank_symbol: The symbol for an empty tape cell.
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol
        self.reset()
    
    def reset(self):
        """Reset the Turing machine to its initial state and clear the tape."""
        self.tape = [self.blank_symbol]
        self.head_position = 0
        self.current_state = self.start_state

    def load_tape(self, input_string):
        """Load the tape with the given input string."""
        self.tape = list(input_string)
        self.head_position = 0

    def step(self):
        """
        Perform one step of the Turing machine.
        :return: True if the machine should continue, False if it has halted.
        """
        if self.current_state in [self.accept_state, self.reject_state]:
            # Halt if the machine is in an accepting or rejecting state
            return False
        
        # Read the symbol at the current head position
        current_symbol = self.tape[self.head_position] if self.head_position < len(self.tape) else self.blank_symbol
        
        # Get the transition based on the current state and read symbol
        key = (self.current_state, current_symbol)
        if key not in self.transitions:
            # No transition defined, move to the reject state
            self.current_state = self.reject_state
            return False

        # Transition logic
        new_state, write_symbol, direction = self.transitions[key]
        self.current_state = new_state

        # Write the symbol on the tape
        if self.head_position < len(self.tape):
            self.tape[self.head_position] = write_symbol
        else:
            self.tape.append(write_symbol)
        
        # Move the head
        if direction == 'R':  # Move right
            self.head_position += 1
            if self.head_position >= len(self.tape):
                self.tape.append(self.blank_symbol)
        elif direction == 'L':  # Move left
            if self.head_position > 0:
                self.head_position -= 1
            else:
                self.tape.insert(0, self.blank_symbol)
                self.head_position = 0
        
        # Continue the execution
        return True

    def run(self, max_steps=1000):
        """
        Run the Turing machine, printing each step.
        :param max_steps: The maximum number of steps to execute.
        """
        print("Initial tape:", ''.join(self.tape))
        print("Initial state:", self.current_state)
        step_count = 0
        
        while step_count < max_steps:
            step_count += 1
            print(f"\nStep {step_count}:")
            print("Tape:", ''.join(self.tape))
            print("State:", self.current_state)
            print("Head position:", self.head_position)
            if not self.step():
                break
        
        if self.current_state == self.accept_state:
            print("\nMachine halted in accepting state.")
        elif self.current_state == self.reject_state:
            print("\nMachine halted in rejecting state.")
        else:
            print("\nMachine did not halt after the maximum number of steps.")

# Example usage
if __name__ == "__main__":
    # Example Turing machine: increments a binary number on the tape
    states = ['q0', 'q1', 'q2', 'accept', 'reject']
    alphabet = ['0', '1', '_']
    transitions = {
        ('q0', '1'): ('q0', '1', 'R'),
        ('q0', '0'): ('q0', '0', 'R'),
        ('q0', '_'): ('q1', '1', 'L'),
        ('q1', '1'): ('q1', '1', 'L'),
        ('q1', '0'): ('q1', '0', 'L'),
        ('q1', '_'): ('accept', '_', 'R'),
    }
    start_state = 'q0'
    accept_state = 'accept'
    reject_state = 'reject'
    blank_symbol = '_'

    # Create the Turing machine
    tm = TuringMachine(states, alphabet, transitions, start_state, accept_state, reject_state, blank_symbol)

    # Load an initial tape (binary number 110)
    tm.load_tape('110')

    # Run the machine
    tm.run()
