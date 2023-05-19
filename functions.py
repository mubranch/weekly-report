def format_child(child):
    new_child = ""
    last_char = ""
    for char in child:
        if char == " " and last_char == " " or char == "\n":
            pass
        else: new_child += char
        last_char = char
        
    return new_child