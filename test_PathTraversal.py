import pytest
from PathTraversal import PathTraversal


@pytest.mark.parametrize(
    "map_data, letters, path",
    [
        (
            [
                "  @---A---+    ",
                "          |    ",
                "  x-B-+   C    ",
                "      |   |    ",
                "      +---+    ",
            ],
            "ACB",
            "@---A---+|C|+---+|+-B-x",
        ),
        (
            [
                "  @",
                "  | +-C--+",
                "  A |    |",
                "  +---B--+",
                "    |      x",
                "    |      |",
                "    +---D--+",
            ],
            "ABCD",
            "@|A+---B--+|+--C-+|-||+---D--+|x",
        ),
        (
            [
                "  @---A---+    ",
                "          |    ",
                "  x-B-+   |    ",
                "      |   |    ",
                "      +---C    ",
            ],
            "ACB",
            "@---A---+|||C---+|+-B-x",
        ),
        (
            [
                "     +-O-N-+    ",
                "     |     |    ",
                "     |   +-I-+  ",
                " @-G-O-+ | | |  ",
                "     | | +-+ E  ",
                "     +-+     S  ",
                "             |  ",
                "             x  ",
            ],
            "GOONIES",
            "@-G-O-+|+-+|O||+-O-N-+|I|+-+|+-I-+|ES|x",
        ),
        (
            [" +-L-+ ", " |  +A-+", "@B+ ++ H", " ++    x"],
            "BLAH",
            "@B+++B|+-L-+A+++A-+Hx",
        ),
        (
            ["  @-A--+      ", "       |      ", "       +-B--x-C--D"],
            "AB",
            "@-A--+|+-B--x",
        ),
        (
            [
                "  @---A---+    ",
                "          |    ",
                "  x-B-+ -----    ",
                "      |   |    ",
                "      +---C    ",
            ],
            "ACB",
            "@---A---+|-|C---+|+-B-x",
        ),
    ],
)
def test_traverse_path_valid(map_data, letters, path):
    path_traverser = PathTraversal(map_data)
    path_traverser.traverse_path(path_traverser.starting_position, None)
    assert "".join(path_traverser.characters) == letters
    assert "".join(path_traverser.path) == path


@pytest.mark.parametrize(
    "map_data, error_msg",
    [
        (
            [
                "     -A---+    ",
                "          |    ",
                "  x-B-+   C    ",
                "      |   |    ",
                "      +---+    ",
            ],
            "Map is not valid",
        ),
        (
            [
                "   @--A---+    ",
                "          |    ",
                "    B-+   C    ",
                "      |   |    ",
                "      +---+    ",
            ],
            "Map is not valid",
        ),
        (
            [
                "   @--A-@-+    ",
                "          |    ",
                "  x-B-+   C    ",
                "      |   |    ",
                "      +---+    ",
            ],
            "Map is not valid",
        ),
        (
            [
                "   @--A---+    ",
                "          |    ",
                "          C    ",
                "          x    ",
                "      @-B-+    ",
            ],
            "Map is not valid",
        ),
        (
            [
                "   @--A--x     ",
                "               ",
                "  x-B-+        ",
                "      |        ",
                "      @        ",
            ],
            "Map is not valid",
        ),
        (
            [
                "        x-B    ",
                "          |    ",
                "   @--A---+    ",
                "          |    ",
                "     x+   C    ",
                "      |   |    ",
                "      +---+    ",
            ],
            "Map is not valid",
        ),
        (
            [
                "   @--A-+      ",
                "        |      ",
                "               ",
                "        B-x    ",
            ],
            "Not a valid path",
        ),
        (["  x-B-@-A-x    "], "Map is not valid"),
        (["  @-A-+-B-x    "], "Fake turn"),
    ],
)
def test_traverse_path_invalid(map_data, error_msg):
    with pytest.raises(Exception, match=f"{error_msg}"):
        path_traverser = PathTraversal(map_data)
        path_traverser.traverse_path(path_traverser.starting_position, None)


def test_prepare_map_valid():
    map_data = [
        "  @---A---+    ",
        "          |    ",
        "  x-B-+   |    ",
        "      |   |    ",
        "      +---C    ",
    ]
    path_traverser = PathTraversal(map_data)
    assert path_traverser.starting_position == (0, 2)


def test_prepare_map_invalid():
    map_data = [
        "     -A---+    ",
        "          |    ",
        "  x-B-+   C    ",
        "      |   |    ",
        "      +---+    ",
    ]
    with pytest.raises(Exception, match="Map is not valid"):
        PathTraversal(map_data)


def test_validate_map():
    map_data_valid = [
        "  @---A---+    ",
        "          |    ",
        "  x-B-+   |    ",
        "      |   |    ",
        "      +---C    ",
    ]
    path_traverser = PathTraversal(map_data_valid)
    valid = path_traverser.validate_map()
    assert valid


def test_path_traversal_str_not_traversed():
    map_data = [
        "  @---A---+    ",
        "          |    ",
        "  x-B-+   C    ",
        "      |   |    ",
        "      +---+    ",
    ]
    path_traverser = PathTraversal(map_data)
    assert str(path_traverser) == "Path traversal was not initiated!"


def test_path_traversal_str_traversed():
    map_data = [
        "  @---A---+    ",
        "          |    ",
        "  x-B-+   C    ",
        "      |   |    ",
        "      +---+    ",
    ]
    path_traverser = PathTraversal(map_data)
    path_traverser.characters = list("ACB")
    path_traverser.path = list("@---A---+|C|+---+|+-B-x")
    assert str(path_traverser) == ("Letters ACB\n"
        + "Path as characters @---A---+|C|+---+|+-B-x")
