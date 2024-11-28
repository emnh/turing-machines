#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

import sys
import re
import os
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class TuringMachine:
    def __init__(self, tape, initial_state, transitions, blank_symbol='_'):
        """
        Turing Machine initialization.
        :param tape: Initial tape content as a list of characters.
        :param initial_state: Starting state of the machine.
        :param transitions: Dictionary of transitions {(state, symbol): (new_state, new_symbol, direction)}
        :param blank_symbol: Symbol representing a blank cell on the tape.
        """
        self.tape = tape
        self.head = 0
        self.state = initial_state
        self.transitions = transitions
        self.blank_symbol = blank_symbol

    def step(self):
        """Executes one step of the Turing Machine."""
        current_symbol = self.tape[self.head] if self.head < len(self.tape) else self.blank_symbol
        key = (self.state, current_symbol)

        if key not in self.transitions:
            return False  # Halting condition

        new_state, new_symbol, direction = self.transitions[key]
        # Update the tape
        if self.head < len(self.tape):
            self.tape[self.head] = new_symbol
        else:
            self.tape.append(new_symbol)

        # Move the head
        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head = max(0, self.head - 1)

        # Update the state
        self.state = new_state
        return True

    def render(self):
        """Renders the current state of the Turing Machine tape and head."""
        display_tape = ''.join(self.tape)
        tape_with_head = ''.join([
            f"{Fore.RED}{Style.BRIGHT}{c}{Style.RESET_ALL}" if i == self.head else c
            for i, c in enumerate(display_tape)
        ])
        return f"Tape: {tape_with_head}\nHead: {' ' * self.head + '^'}\nState: {self.state}"


def animate_turing_machine(machine, delay=0.5):
    """Animates the Turing Machine execution."""
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(machine.render())
            if not machine.step():
                print("\nTuring Machine halted.")
                break
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nAnimation stopped by user!")


# Example Turing Machine setup
if __name__ == "__main__":
    initial_tape = list("1101")  # Input tape
    transitions = {
        ('q0', '1'): ('q0', '1', 'R'),
        ('q0', '0'): ('q1', '1', 'R'),
        ('q1', '_'): ('qH', '_', 'R'),  # Halting state
    }
    tm = TuringMachine(tape=initial_tape, initial_state='q0', transitions=transitions)
    animate_turing_machine(tm)
