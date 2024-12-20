#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
documentation
'''

import os
import sys
import re
import colorama
from tabulate import tabulate
from colorama import Fore, Back, Style

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
            return None

        # Read the symbol at the current head position
        current_symbol = self.tape[self.head_position] if self.head_position < len(self.tape) else self.blank_symbol

        # Get the transition based on the current state and read symbol
        key = (self.current_state, current_symbol)
        if key not in self.transitions:
            # No transition defined, move to the reject state
            self.current_state = self.reject_state
            return None

        # Transition logic
        written = None
        new_state, write_symbol, direction = self.transitions[key]
        self.current_state = new_state

        # Write the symbol on the tape
        if self.head_position < len(self.tape):
            if self.tape[self.head_position] != write_symbol:
                written = self.head_position
            self.tape[self.head_position] = write_symbol
        else:
            self.tape.append(write_symbol)

        # Move the head
        if direction == 'R':  # Move right
            self.head_position += 1
            if self.head_position >= len(self.tape):
                self.tape.append(self.blank_symbol)
                written = self.head_position
        elif direction == 'L':  # Move left
            if self.head_position > 0:
                self.head_position -= 1
            else:
                self.tape.insert(0, self.blank_symbol)
                self.head_position = 0
                written = self.head_position

        # Continue the execution
        return self.transitions[key] + (written,)

    def formatTape(self, tape, head_pos, changed_symbol_pos):
        s = []
        for i, c in enumerate(tape):
            if i == changed_symbol_pos:
                s.append(Fore.MAGENTA + c + Style.RESET_ALL)
            elif i == head_pos:
                s.append(Fore.BLUE + c + Style.RESET_ALL)
            else:
                s.append(c)
        return ''.join(s)

    def run(self, max_steps=1000):
        """
        Run the Turing machine, printing each step.
        :param max_steps: The maximum number of steps to execute.
        """

        def makeRow(step_count, step_log):
            if step_log:
                new_state, write_symbol, direction, written = step_log
            else:
                written = None
                write_symbol = self.tape[self.head_position]
                direction = ' '
            changed = self.tape[self.head_position] != write_symbol
            row = []
            row.append(step_count),
            row.append(self.current_state)
            row.append(self.formatTape(self.tape, self.head_position, written))
            row.append(direction)
            row.append(changed)
            return row

        step_count = 0
        step_log = ""
        tape_states = [self.tape]
        output = []
        row = makeRow(step_count, None)
        output.append(row)

        while step_count < max_steps:
            step_count += 1
            step_log = self.step()
            tape_states.append(self.tape)
            if not step_log:
                #row = makeRow(step_count, step_log)
                #output.append(row)
                break
            row = makeRow(step_count, step_log)
            output.append(row)

        headers = ["Step", "State", "Tape", "Direction", "Change"]
        print(tabulate(output, headers=headers))

        if self.current_state == self.accept_state:
            print("\nMachine halted in accepting state.")
        elif self.current_state == self.reject_state:
            print("\nMachine halted in rejecting state.")
        else:
            print("\nMachine did not halt after the maximum number of steps.")

# Example usage
if __name__ == "__main__":
    colorama.init()

    # Example Turing machine: increments a binary number on the tape
    states = ['q0', 'carry', 'accept', 'reject']
    alphabet = ['0', '1', '_']
    transitions = {
        # Move to the rightmost bit
        ('q0', '0'): ('q0', '0', 'R'),
        ('q0', '1'): ('q0', '1', 'R'),
        ('q0', '_'): ('carry', '_', 'L'),  # Start the carry phase

        # Handle the carry
        ('carry', '0'): ('accept', '1', 'N'),  # Stop after resolving carry
        ('carry', '1'): ('carry', '0', 'L'),  # Propagate the carry
        ('carry', '_'): ('accept', '1', 'N'),  # Add a new bit to the left if overflow
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
