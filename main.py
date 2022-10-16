from typing import IO, List


def open_file() -> IO:
    # ask for file name
    file_name = input("Enter a filename: ")
    # file is not changeable
    file_pointer = None
    while file_pointer is None:
        try:
            # try to open and read file now that have access to file pointer loaded in program
            file_pointer = open(file_name, "r")
        except IOError:
            print("Error in filename.")
            # except if the file can't be opened, ask them to input file name again
            file_name = input("Enter a filename: ")

    return file_pointer


def read_file(fp: IO) -> List[List[int]]:
    # number of users in the network
    n = fp.readline()
    # make the number of users an int
    n = int(n)
    # network of users, which is a list
    network = []
    for i in range(n):
        # create n empty lists within network
        network.append([])

    line = fp.readline()
    while line is not None and len(line) >= 3:
        # while there are still lines and the two elements on each line are read, go to next line
        split_line = line.strip().split(" ")
        # place the second element into first element's list since mutual friends
        network[int(split_line[0])].append(int(split_line[1]))
        # place the first element into second element's list since mutual friends
        network[int(split_line[1])].append(int(split_line[0]))
        # continue reading each line into list
        line = fp.readline()
    # return the full network of friends
    return network


def init_matrix(n: int) -> List[List[int]]:
    # create empty matrix
    matrix = []
    for row in range(n):
        # add the number of rows to the matrix
        matrix.append([])
        for column in range(n):
            # in each row, add a column of 0's according to size n
            matrix[row].append(0)
    return matrix


def num_in_common_between_lists(list1: List[int], list2: List[int]) -> int:
    # set common to 0 initially
    common = 0
    for i in range(len(list1)):
        for j in range(len(list2)):
            # check if any friends between the friends of each list1 is equal to friends of each list2
            if list1[i] == list2[j]:
                # add one to common if friends are common between users
                common += 1

    return common



def calc_similarity_scores(network: List[List[int]]) -> List[List[int]]:
    # create a similarity matrix that is of the size network
    similarity = init_matrix(len(network))
    for i in range(len(network)):
        for j in range(len(network)):
           # put how many friends are in common for each user to each element of similarity
           similarity[i][j] = num_in_common_between_lists(network[i], network[j])

    return similarity



def recommend(user_id: int, network: List[List[int]], similarity_matrix: List[List[int]]) -> int:

    # set friend_matrix to the element of similarity matrix whose id is given
    friend_matrix = similarity_matrix[user_id]
    # set friend_net to the element of network matrix whose id is given
    friend_net = network[user_id]
    # make max_friend small first so it gets taken by the first friend of user_id
    max_friend = -1
    # make max_friend_id 0 to set as int
    max_friend_id = 0
    for i in range(len(friend_matrix)):
        # check if the friend is not a friend already, is not the user itself, and if they have more friends in common
        if i not in friend_net and i != user_id and friend_matrix[i] > max_friend:
            # if so, make that friend the new recommended friend
            max_friend_id = i
            # make that number of friends in common the new max number of friends in common
            max_friend = friend_matrix[i]


    return max_friend_id

def main():

    print("Facebook friend recommendation\n")
    # make net the network of friends the program will read
    net = read_file(open_file())
    # skip a line
    print("\n")
    # make similar the similarity matrix of common friends in net
    similar = calc_similarity_scores(net)
    # set continue to yes for the first iteration of while
    cont = "yes"
    # this way, only yes, YES, yEs, ect. makes the program continue,
    # note: Professor said no need to have "no" stop the program, anything other than yes can stop the program
    while cont.lower() == "yes":
        # ask user for an integer that signifies the friend id that will have a friend recommended to him or her
        n = (input(f"Enter an integer from the range 0 to {len(net) - 1} : "))
        # while the id the user types is not a number or is not in the range of valid id's
        # note: Professor said no need to use try-except
        while n.isdigit() == False or int(n) < 0 or int(n) > len(net) - 1:
            # let the user know he or she put an invalid id
            print(f"Error: input must be an int between 0 and {len(net) - 1}")
            # ask the user for another id
            n = (input(f"Enter an integer from the range 0 to {len(net) - 1} : "))
        # print the suggested friend's id
        print(f"The suggested friend for {n} is {recommend(int(n), net, similar)} \n")
        # ask the user if he or she wants to continue with the program
        cont = input("Do you want to continue (yes/no)? ")



if __name__ == "__main__":
    main()
