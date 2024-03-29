from Classes import Queue, LinkedList
import sys

def get_words(path: str) -> set[str]:
    """
    Gets the set of all words we are aware of

    Args:
        path (str): the text file of all words that are given to us

    Returns:
        set[str]: the set of all words in the text file
    """
    words = set()

    with open(path, "r") as file:
        for wrd in file.read().splitlines():
            words.add(wrd)
    return words

# fix this and it works
def generate_neigh(word: str) -> list[str]:
    """
    Generates all possible neighbors for a given word, where each letter in the word
    is then replaced by every letter in the alphebet

    Args:
        word (str): the current word

    Returns:
        list[str]: all possible words that can be formed by replacing one letter in the word
    """
    word = list(word)
    words = []
    alphebet = [chr(n) for n in range(ord("a"), ord("z") + 1)]

    for index in range(len(word)):
        cpy = word[:]
        for let in alphebet:
            cpy[index] = let
            words.append("".join(cpy))
    

    return words

def construct_path(visited: dict, start: str, goal: str) -> LinkedList:
    """
    Constructs the path using a visited hashmap

    Args:
        visited (dict): key is the child node, value is the parent node
        start (str): the initial state
        goal (str): the end state

    Returns:
        LinkedList[str]: the path represented by a linked list
    """
    path = LinkedList()
    path.add(goal)

    current = visited[goal]

    while current != start:
        path.add(current)
        current = visited[current]
    
    path.add(start)
    
    return path

def find_path(start: str, goal: str, words: set[str]) -> LinkedList:
    """Finds the path from a start word to some goal word

    Args:
        start (str): the initial word
        goal (str): the end goal
        words (set[str]): all known words

    Returns:
        LinkedList[str]: the path from one word to another as start -> ... -> end word
        defaults to None when no path is found
    """

    queue = Queue()
    visited = {}
    current = None
    queue.enqueue(start)
    
    visited[start] = start

    while True:
        if queue.get_size() == 0:
            break
        current = queue.dequeue()

        if current == goal:
            return construct_path(visited, start, goal)

        for wrd in generate_neigh(current):
            if wrd not in visited and wrd in words:
                queue.enqueue(wrd)
                visited[wrd] = current
        
    return None

def main() -> None:
    """
    Performs a BFS search to find the shortest path in changing words from
    start word to goal word

    @pre-cond: argv = [file path, start word, goal word]
    """
    start, goal = sys.argv[2], sys.argv[3]

    words = get_words(sys.argv[1])

    path = find_path(start, goal, words)
    if path:
        current = path.root
        while current is not None:
            print(current.get_value())
            current = current.get_right_link()
    else:
        print("No solution")

    return

if __name__ == "__main__":
    main()