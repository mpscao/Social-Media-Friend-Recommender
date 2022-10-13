from typing import IO, List


def open_file() -> IO:

    file_name = input("Enter a filename: ")
    file_pointer = None
    while file_pointer is None:
        try:
            file_pointer = open(file_name, "r")
        except IOError:
            print("Error in filename.")
            file_name = input("Enter a filename: ")

    return file_pointer


def read_file(fp: IO) -> List[List[int]]:

    n = fp.readline()
    n = int(n)
    network = []
    for i in range(n):
        network.append([])

    line = fp.readline()
    while line is not None and len(line) >= 3:
        split_line = line.strip().split(" ")
        network[int(split_line[0])].append(int(split_line[1]))
        network[int(split_line[1])].append(int(split_line[0]))
        line = fp.readline()

    return network


def init_matrix(n: int) -> List[List[int]]:

    matrix = []
    for row in range(n):
        matrix.append([])
        for column in range(n):
            matrix[row].append(0)

    return matrix


def num_in_common_between_lists(list1: List[int], list2: List[int]) -> int:

    common = 0
    for i in range(len(list1)):
        for j in range(len(list2)):
            if list1[i] == list2[j]:
                common += 1

    return common



def calc_similarity_scores(network: List[List[int]]) -> List[List[int]]:

    similarity = init_matrix(len(network))
    for i in range(len(network)):
        for j in range(len(network)):
           similarity[i][j] = num_in_common_between_lists(network[i], network[j])

    return similarity



def recommend(user_id: int, network: List[List[int]], similarity_matrix: List[List[int]]) -> int:


    friend_matrix = similarity_matrix[user_id]
    friend_net = network[user_id]
    max_friend = -1
    max_friend_id = 0
    for i in range(len(friend_matrix)):
        if i not in friend_net and i != user_id and friend_matrix[i] > max_friend:
            max_friend_id = i
            max_friend = friend_matrix[i]


    return max_friend_id

def main():

    print("Facebook friend recommendation\n")
    net = read_file(open_file())
    print("\n")
    similar = calc_similarity_scores(net)
    cont = "yes"
    while cont.lower() == "yes":
        n = (input("Enter an integer from the range 0 to " + str(len(net) - 1) + ": "))
        while n.isdigit() == False or int(n) < 0 or int(n) > len(net) - 1:
            print("Error: input must be an int between 0 and " + str(len(net) - 1))
            n = (input("Enter an integer from the range 0 to " + str(len(net) - 1) + ": "))
        print("The suggested friend for " + str(n) + " is " + str(recommend(int(n), net, similar)) + "\n")
        cont = input("Do you want to continue (yes/no)? ")



if __name__ == "__main__":
    main()