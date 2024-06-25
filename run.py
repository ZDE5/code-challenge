from PathTraversal import PathTraversal


if __name__ == "__main__":

    map_data = [
                    "  @",
                    "  | +-C--+",
                    "  A |    |",
                    "  +---B--+",
                    "    |      x",
                    "    |      |",
                    "    +---D--+",
                ]

    map_data2 = [
                    "  @---A---+    ",
                    "          |    ",
                    "  x-B-+ -----    ",
                    "      |   |    ",
                    "      +---C    ",
                ]

    path_traverser = PathTraversal(map_data)
    path_traverser.traverse_path(path_traverser.starting_position, None)
    print(path_traverser)

    path_traverser.__init__(map_data2)
    path_traverser.traverse_path(path_traverser.starting_position, None)
    print(path_traverser)
