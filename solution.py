
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
diagonals = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'], ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]

unitlist = unitlist + diagonals

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    
    # Get all the boxes that have only 2 possible values left
    # Pairs - A list of [Box, Values] of any boxes with exactly 2 values left
    # Box - from values.key() - box_name
    # Values - From Values[box_name] - '123456'
 
    display(values)
    
    for unit in unitlist:
        pairBoxes = [[box, values[box]] for box in unit if len(values[box]) == 2]
    # Go through each box that has only 2 possible values left to find naked twins
    # Pair - A [Box, Values] of a box that has exactly 2 values left
        if len(pairBoxes) == 2:
            box1, box2 = pairBoxes[0], pairBoxes[1]
            print(box1, box2)
            if box1[1] == box2[1]:
                # Check through each box with exactly 2 values left to see if it matches any 2 values of it's peers
                print("Got ourselves a pair of naked twins!")
                print(box1, box2)
                # PeersToEdit - a set of peers of a set of naked twins
                # p - a box_number of a peer of a naked twin
                #removable_peers = [p for p in peersToEdit if len(values[p]) > 2]
                editPeers = [p for p in unit if len(values[p]) > 2]
                print("Peers to edit: ", editPeers)
                for p in editPeers:
                    for v in values[box1[0]]:
                        if v in values[p]:
                            print("Removed a value because of a naked pair!", p, v, values[p])
                            values = assign_value(values, p, values[p].replace(v, ""))
                            display(values)
    
    return values
            
          
                          
    

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
     
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    # Look through every box and value on the board
    for key, value in values.items():
        # Find all the values with only one value left
        if len(value) == 1:
            # Create a list of peers of that box
            neighbors = peers[key]
            # Look through each neighbor, n
            for n in neighbors:
                # Make sure there is more than one value left in the neighbor
                if len(values[n]) > 1:
                           # string = values[box]
                           # values[box] = string.replace(value, "")
                            # replace the single value with nothing from the peer's box with the single value in it
                            values = assign_value(values, n, values[n].replace(value, ""))
                            #print(value, n)
    return values


def only_choice(values):
    
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
   
    # TODO: Implement only choice strategy here


 """
   # print("Only_Choice Removed: ")
    for unit in unitlist:
        for number in '123456789':
            
            possible_options = [box for box in unit if number in values[box]]
            if len(possible_options) == 1:
                values = assign_value(values, possible_options[0], number)
               # print(number, values[possible_options[0]], possible_options[0])
    return values

    


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = naked_twins(values)
        values = only_choice(values)
        values = eliminate(values)
        print("After Full Round")
        display(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    
    if values is False:
        return False
        
    # Choose one of the unfilled squares with the fewest possibilities
    unsolved_boxes = []
    for box in boxes:
        if len(values[box]) > 1:
            unsolved_boxes.append(box)
    
    if len(unsolved_boxes) == 0:
        return values
    else:
        fewest, fbox = min((len(values[box]), box) for box in unsolved_boxes)
        
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for p in values[fbox]:
        new = values.copy()
        new[fbox] = p
        possible = search(new)
        if possible:
            return possible


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
