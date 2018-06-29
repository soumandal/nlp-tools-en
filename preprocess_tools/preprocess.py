def elongation_check(token):
    characters = [char for char in token]
    if len(characters) > 2:
        for index in range(2, len(characters)):
            current = characters[index]
            previous_1, previous_2 = characters[index - 1], characters[index - 2]

            if current == previous_1 and current == previous_2:
                characters[index] = ""
        return "".join(characters)
    else:
        return "".join(characters)