---
## Concept

This is a command-line utility to organize TODOs and priorities on a day-to-day basis.
The concept is to structure the TODOs in a TODO-DAG (or TODAG), where DAG stands for [Directed Acylic Graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph), instead of following the more common TODO-list format.

---
## Implementation
Every 'TODO' is a card, and every card has parents and children that will form the DAG. A card can be marked as done only when all the parents are also flagged as done. The language choosen for the implementation is Python, and the cards are kept in a dictionary. The dictionary is made persistent using the pickle module, and there are high-level CLI API to create and save cards. The basic use cases are to add cards, add parents cards, and run the 'TODO' routine, that consist in finding all the cards with all the parents already completed (to advance in the todo tree). 

---
## Development
The utility is developed using OOP methodologies, and adhereing to the [Google Python style-guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md), especially regarding the documentation. Is encouraged Test-Drived-Development, as the whole utility will be tested periodically using Continuous Integration practices. Up to now there is no plan in writing a external documentation as the in-code documentation should be enough.

---
## Usage
Inside the bin folder there are the two scripts to use the TODAG:
- **open.py**: create new todos in the DAG, delete or print the DAG
- **todo.py**: traverse the DAG and print the todos with highest priority (the roots), and for every todo print the connected components it belongs to

For more detail on the usage you can check the in-code docs
