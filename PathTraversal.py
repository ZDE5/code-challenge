from typing import List


class PathTraversal:
    def __init__(self, map: List[str]):
        self.map = map
        self.starting_position = self.prepare_map()
        self.path = []
        self.characters = []
        self.chars_control = {}

    def prepare_map(self):
        if not self.validate_map():
            raise Exception("Map is not valid")
        return self.find_starting_point()

    def validate_map(self):
        at_count = 0
        x_count = 0

        allowed_characters = {"@", "x", "-", "|", "+", " "}
        allowed_characters.update(
            chr(c) for c in range(ord("A"), ord("Z") + 1)
        )

        for row in self.map:
            if not all(char in allowed_characters for char in row):
                breakpoint()
                return False
            at_count += row.count("@")
            x_count += row.count("x")

        if at_count != 1 or x_count != 1:
            return False

        return True

    def find_starting_point(self):
        _row = 0
        for row in self.map:
            if "@" in row:
                column = row.index("@")
                return (_row, column)
            else:
                _row += 1

    def traverse_path(self, position, direction):
        current_char = self.map[position[0]][position[1]]
        self.path.append(current_char)

        if (
            current_char.isupper() and
            position not in self.chars_control.keys()
        ):
            self.characters.append(current_char)
            self.chars_control[position] = current_char

        if current_char != "x":
            next_position, direction = self.find_next_position(
                current_char, position, direction
            )
            if next_position is None:
                raise Exception("Not a valid path")
            self.traverse_path(next_position, direction)

    def find_next_position(self, current_char, position, direction):
        x = position[0]
        y = position[1]
        new_position = None
        new_direction = None
        possible_steps = [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]
        allowed_directions = 0
        for step in range(0, 4):
            next_char = None
            if direction is not None:
                if step == (3 - direction):
                    continue
            new_x = possible_steps[step][0]
            new_y = possible_steps[step][1]
            if new_x < 0 or new_y < 0:
                continue
            try:
                next_char = self.map[new_x][new_y]
            except Exception:
                continue

            if current_char == "@":
                if step in [0, 3] and not (
                    next_char.isupper() or next_char in ["|", "+", "x"]
                ):
                    continue
                if step in [1, 2] and not (
                    next_char.isupper() or next_char in ["-", "+", "x"]
                ):
                    continue
                if new_position:
                    raise Exception(
                        "There is multiple directions from starting point"
                    )
                new_position = (new_x, new_y)
                new_direction = step

            if current_char in ["-", "|"]:
                if step == direction and (
                    next_char.isupper() or next_char in ["-", "|", "+", "x"]
                ):
                    return (new_x, new_y), step

            if current_char.isupper() or current_char == "+":
                if step in [0, 3] and not (
                    next_char.isupper() or next_char in ["|", "+", "x", "@"]
                ):
                    continue
                if step in [1, 2] and not (
                    next_char.isupper() or next_char in ["-", "+", "x", "@"]
                ):
                    continue

                allowed_directions += 1
                if step == direction:
                    new_position = (new_x, new_y)
                    new_direction = step
                else:
                    if new_position:
                        continue
                    new_position = (new_x, new_y)
                    new_direction = step

        if current_char.isupper():
            if new_direction == direction:
                if not (allowed_directions in [1, 3]):
                    breakpoint()
                    raise Exception("There is a fork in path")

            else:
                if not (allowed_directions == 1):
                    breakpoint()
                    raise Exception("There is a fork in path")

        if current_char == "+":
            if new_direction == direction:
                raise Exception("Fake turn")

            else:
                if allowed_directions != 1:
                    breakpoint()
                    raise Exception("There is a fork in path")

        return new_position, new_direction

    def __str__(self):
        return (
            "Letters "
            + "".join(self.characters)
            + "\n"
            + "Path as characters "
            + "".join(self.path)
        )
