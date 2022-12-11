def add_spaces(line, count_spaces):
    i = 0
    splitted_line = line.split()
    total_words = sum(1 for _ in splitted_line)
    if total_words == 1:
        return line
    # start iterate over list if there are more than one word
    while True:
        # if it's last word and it's line still needed more spaces then iterate over list from the start (i = 0)
        if count_spaces != 0 and i == (total_words - 1):
            i = 0
        # check if it's still needed to add spaces to line
        if count_spaces > 0:
            splitted_line[i] += ' '
            count_spaces -= 1
            i += 1
        else:
            break
    return ' '.join(splitted_line)

def justify(text, width):
    # starting variables
    line = ''
    linelength = 0
    finished_text = ''
    # iterate over text, item represents each word
    for item in text.split():
        # check if current line + new word is bigger than given width
        if linelength + len(item) > width:
            # delete space after last word
            line = line[:-1]
            linelength -= 1
            # if length of line is less than width, then add spaces to this line
            if width - linelength > 0:
                line = add_spaces(line, width - linelength)
            # add line with all needed spaces to the final text version
            finished_text += line + '\n'
            # setup variables to starting positions
            line = ''
            linelength = 0
        # if current line + new_word is less than width, then add new_word to current line
        linelength += len(item)
        line += item
        linelength += 1
        line += ' '
    # delete last space because of Kata conditions
    line = line[:-1]
    finished_text += line
    
    return finished_text
