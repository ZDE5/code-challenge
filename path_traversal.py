from typing import List


class PathTraversal:
    def __init__(self, map: List[str]):
        """
        Initializes the PathTraversal object with a map represented as a list of strings.
        
        Args:
        - map (List[str]): A list where each element is a string representing a row in the map.
        """
        self.map = map
        self.starting_position = ()
        self.path = []
        self.characters = []
        self.chars_control = {}
        self.prepare_map()

    def prepare_map(self):
        """
        Prepares the map for traversal by finding the starting point and validating the map.
        
        Raises:
        - Exception: If the map contains invalid characters, multiple starting points, or no starting point.
        """
        try:
            self.starting_position = self.find_starting_point()
            self.validate_map()            
        except Exception:
            raise
        

    def validate_map(self):
        """
        Validates the map to ensure it contains exactly one starting point '@' and one ending point 'x',
        and only contains allowed characters.
        
        Raises:
        - Exception: If the map contains invalid characters or incorrect counts of '@' or 'x'.
        
        Returns:
        - bool: True if the map is valid, otherwise raises an exception.
        """
        at_count = 0
        x_count = 0

        allowed_characters = {"@", "x", "-", "|", "+", " "}
        allowed_characters.update(
            chr(c) for c in range(ord("A"), ord("Z") + 1)
        )

        for row in self.map:
            if not all(char in allowed_characters for char in row):
                raise Exception("Map contains invalid characteers!")
            at_count += row.count("@")
            x_count += row.count("x")

        if at_count != 1:
            raise Exception("Number of starting points is different from 1!")
        if x_count != 1:
            raise Exception("Number of ending points is different from 1!")

        return True

    def find_starting_point(self):
        """
        Finds the starting point '@' in the map and returns its coordinates (row, column).
        
        Returns:
        - tuple: Coordinates (row, column) of the starting point '@'.
        
        Raises:
        - Exception: If no starting point '@' is found in the map.
        """
        _row = 0
        for row in self.map:
            if "@" in row:
                column = row.index("@")
                return (_row, column)
            else:
                _row += 1
        raise Exception("Starting point is missing!")

    def traverse_path(self, position, direction):
        """
        Recursively traverses the map path starting from the given position and direction.
        
        Args:
        - position (tuple): Coordinates (row, column) of the current position in the map.
        - direction (int or None): Current direction of traversal (0: up, 1: left, 2: right, 3: down).
        
        Raises:
        - Exception: If the traversal encounters an invalid path or a fork in the path.
        """
        current_char = self.map[position[0]][position[1]]
        self.path.append(current_char)

        if (
            current_char.isupper() and
            position not in self.chars_control
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
        """
        Determines the next valid position and direction to traverse based on the current position and direction.
        
        Args:
        - current_char (str): Current character at the given position in the map.
        - position (tuple): Coordinates (row, column) of the current position in the map.
        - direction (int or None): Current direction of traversal (0: up, 1: left, 2: right, 3: down).
        
        Returns:
        - tuple: Coordinates (row, column) of the next valid position to traverse.
        - int: Updated direction of traversal after determining the next position.
        
        Raises:
        - Exception: If there is no valid next position found based on the current position and direction.
        """
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
                        "There is multiple directions from starting point!"
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
                    raise Exception("There is a fork in path")

            else:
                if not (allowed_directions == 1):
                    raise Exception("There is a fork in path")

        if current_char == "+":
            if new_direction == direction:
                raise Exception("Fake turn")

            else:
                if allowed_directions != 1:
                    raise Exception("There is a fork in path")

        return new_position, new_direction

    def __str__(self):
        """
        Returns a string representation of the PathTraversal object in given format, showing the traversed letters and path as characters.
        
        Returns:
        - str: String representation of the PathTraversal object.
        """
        if len(self.characters) == 0:
            return "Path traversal was not initiated!"
        return (
            "Letters "
            + "".join(self.characters)
            + "\n"
            + "Path as characters "
            + "".join(self.path)
        )
