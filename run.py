import argparse
from path_traversal import PathTraversal


def read_map_from_file(filename):
    with open(filename, 'r') as file:
        return [line.rstrip() for line in file]
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process map files for path traversal.')
    parser.add_argument('map_files', nargs='+', type=str, help='List of map file paths')
    args = parser.parse_args()

    for map_file in args.map_files:

        map_data = read_map_from_file(map_file)
        path_traverser = PathTraversal(map_data)
        path_traverser.traverse_path(path_traverser.starting_position, None)
        print(path_traverser)

