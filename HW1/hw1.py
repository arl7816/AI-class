from Classes import Queue, LinkedList
import sys

def get_words(path: str) -> set:
    words = set()

    with open(path, "r") as file:
        for wrd in file.read().splitlines():
            words.add(wrd)
    return words

# fix this and it works
def generate_neigh(word: str) -> list[str]:
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
    path = LinkedList()
    path.add(goal)

    current = visited[goal]

    while current != start:
        path.add(current)
        current = visited[current]
    
    path.add(start)
    
    return path

def find_path(start: str, goal: str, words: set) -> None:
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