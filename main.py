# Author: Hope Crisafi
# this is a program that determines if congressional districts are gerrymandered
from tkinter import *

VOTER_INDEX = 1
DEM_INDEX = 1
REP_INDEX = 2


def print_introduction():
    print()
    print("This program allows you to search through data about")
    print("congressional voting districts and determine whether")
    print("a particular state is gerrymandered.")
    print()


def get_state():
    """
    This function prompts the user for the state they want to search for.
    :return: the state the user wants to search for
    """
    state_input = input("Enter a State: ").lower()
    return state_input


def get_eligible_voters(state, filename):
    """
    This function gets the number of eligible voters for a state.
    :param state: a state
    :param filename: a file name
    :return: number of eligible voters
    """
    myFile = open(filename, 'r')

    for value in myFile:
        data = value.split(',')
        stateLowercase = data[0].lower()

        if stateLowercase == state:
            number_voters = int(data[VOTER_INDEX])
            return number_voters


def get_district_info(state, filename):
    """
    gets the district number, democrat votes, and republican votes for each district
    in a given state
    :param state: a state to search for
    :param filename: a file to search from
    :return: -1 if the state has less than 3 districts, otherwise a list of lists
    """
    myFile = open(filename, 'r')
    all_district_info = []

    for value in myFile:
        data = value.split(',')
        stateLowercase = data[0].lower()

        if stateLowercase == state:
            if data[1] == "AL":
                return -1
            else:
                for index in range(1, len(data), 3):
                    district_info = [int(data[index]), int(data[index + 1]), int(data[index + 2])]
                    all_district_info.append(district_info)
                return all_district_info


def wasted_votes(district_info):
    """
    This function calculates the number of votes wasted in each district.
    :param district_info: information containing each district's number, democrat votes, and republican votes
    """
    dem_votes_total = 0
    rep_votes_total = 0
    dem_wasted = 0
    rep_wasted = 0
    state_total_votes = 0

    for value in district_info:
        democrat = value[DEM_INDEX]
        republican = value[REP_INDEX]
        total_votes = democrat + republican
        state_total_votes += total_votes
        dem_votes_total += democrat
        rep_votes_total += republican

        if democrat > republican:
            votes_needed_to_win = int((total_votes / 2) + 1)
            rep_wasted += republican
            dem_wasted += (democrat - votes_needed_to_win)

        if republican > democrat:
            dem_wasted += democrat
            votes_needed_to_win = int((total_votes / 2) + 1)
            rep_wasted += (republican - votes_needed_to_win)

    print("Democrat votes wasted:", "{:,}".format(dem_wasted))
    print("Republican votes wasted:", "{:,}".format(rep_wasted))

    if rep_votes_total > dem_votes_total:
        vote_percentage = rep_wasted / state_total_votes

        if vote_percentage >= .07:
            print("Gerrymandered to favor Republicans")
        else:
            print("District not gerrymandered")

    else:  # totalDem > totalRep:
        vote_percentage = dem_wasted / state_total_votes

        if vote_percentage >= .07:
            print("Gerrymandered to favor Democrats")
        else:
            print("Not gerrymandered")


def main():
    print_introduction()
    state = get_state()
    eligible_voters = get_eligible_voters(state, "eligible_voters.txt")
    if not eligible_voters:
        print("\"" + state + "\" not found.")
        print('Note: If you are searching for Washington D.C., try "District of Columbia"')
    else:
        district_info = get_district_info(state, "districts.txt")
        if district_info == -1:
            print(state.capitalize() + " cannot be gerrymandered (not enough districts)")
        else:
            print(state.capitalize() + " information:")
            wasted_votes(district_info)


if __name__ == '__main__':
    main()
