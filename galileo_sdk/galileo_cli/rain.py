import curses
import random
import time
import math
 
"""
 
Based on C ncurses version
 
http://rosettacode.org/wiki/Matrix_Digital_Rain#NCURSES_version
 
"""
 
"""
Time between row updates in seconds
Controls the speed of the digital rain effect.
"""
 
ROW_DELAY=.0001
 
def get_rand_in_range(min, max):
    return random.randrange(min,max+1)
    
def isLogo(radius, half_width, center_x, center_y, row, column):

    m = 30/9

    return bool(
                ((((i-center_x)**2 + ((columns_row[i]-center_y)/0.5)**2 > (radius+half_width)**2) or 
                ((i-center_x)**2 + ((columns_row[i]-center_y)/0.5)**2 < (radius-half_width)**2))) and
                (((columns_row[i]-center_y) > -m*(i-center_x) - math.ceil(((radius)/1.2)) or (columns_row[i]-center_y) < -m*(i-center_x) - math.ceil(((radius)/0.7))) or
                ((columns_row[i]-center_y) > math.ceil(((radius)/4.5)) or (columns_row[i]-center_y) < -1*math.ceil(((radius)/4.5)))) and
                (((columns_row[i]-center_y) > -m*(i-center_x) + math.ceil(((radius)/0.7)) or (columns_row[i]-center_y) < -m*(i-center_x)+1*math.ceil(((radius)/1.2))) or
                ((columns_row[i]-center_y) > math.ceil(((radius)/4.5)) or (columns_row[i]-center_y) < -1*math.ceil(((radius)/4.5)))) and
				(((columns_row[i]-center_y) > -m*(i-center_x) + math.ceil(((radius)/0.5)) or (columns_row[i]-center_y) < -m*(i-center_x) - 1*math.ceil(((radius)/2.4))) or
                ((columns_row[i]-center_y) > math.ceil(((radius)/32)) or (columns_row[i]-center_y) < -1*math.ceil(((radius)/32))))
                )
 
try:
    # Characters to randomly appear in the rain sequence.
    chars = ['H', 'y', 'p', 'e', 'r', 'n', 'e', 't']
 
    total_chars = len(chars)
 
    stdscr = curses.initscr()
    curses.noecho()
    curses.curs_set(False)
 
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    stdscr.attron(curses.color_pair(1))
 
    max_x = curses.COLS - 1
    max_y = curses.LINES - 1
    
    center_x = math.ceil(max_x/2)
    center_y = math.ceil(max_y/2)
    
    radius = math.ceil(center_x/2.2)
    half_width = math.ceil(radius/8)
 
    # Create arrays of columns based on screen width.
 
    # Array containing the current row of each column.
 
    columns_row = []
 
    # Array containing the active status of each column.
    # A column draws characters on a row when active.
 
    columns_active = []
 
    for i in range(max_x+1):
        columns_row.append(-1)
        columns_active.append(0)
 
    while(True):
        for i in range(max_x):
            if columns_row[i] == -1:
                # If a column is at the top row, pick a
                # random starting row and active status.
                columns_row[i] = get_rand_in_range(0, max_y)
                columns_active[i] = get_rand_in_range(0, 1)
 
        # Loop through columns and draw characters on rows
 
        for i in range(max_x):
            if columns_active[i] == 1 and isLogo(radius, half_width, center_x, center_y, columns_row[i], i):
                # Draw a random character at this column's current row.
                char_index = get_rand_in_range(0, total_chars-1)
                #mvprintw(columns_row[i], i, "%c", chars[char_index])                
                stdscr.addstr(columns_row[i], i, chars[char_index])
            else:
                # Draw an empty character if the column is inactive.
                #mvprintw(columns_row[i], i, " ");
                stdscr.addstr(columns_row[i], i, " ");
 
 
            columns_row[i]+=1
 
            # When a column reaches the bottom row, reset to top.
            if columns_row[i] >= max_y:
                columns_row[i] = -1
 
            # Randomly alternate the column's active status.
            if get_rand_in_range(0, 1000) == 0:
                if columns_active[i] == 0:      
                    columns_active[i] = 1
                else:
                    columns_active[i] = 0
 
            time.sleep(ROW_DELAY)
            stdscr.refresh()
 
except KeyboardInterrupt as err:
    curses.endwin()    