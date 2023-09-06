import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# /Users/miasponseller/Desktop/MIA_08.14.2023_Spatial_W-Maze.Coh17.xlsx - Spatial.csv

# get file
fp = input("Enter file path:\n")
cohort17_data = pd.read_csv(fp)

# rename CIPL column
cohort17_data.rename(columns={"Platform : CIPL": "CIPL"}, inplace=True)

# choose what data you want to look at
while True:
    try:
        data_num = int(input("Enter number of what you want to explore: \n"
                             "1. Across day performance for each rat.\n"
                             "2. Within day performance for each rat.\n"
                             "3. Average performance across all rats, each day.\n"))
        if data_num in [1, 2, 3]:
            break
        else:
            print("\nInvalid input.")
    except ValueError:
        print("\nInvalid input.")


# 1. Across day performance for each rat.
def across_day_performance_indiv():
    # ask for rat num
    while True:
        try:
            rat_num = int(input("Enter rat number, 10939-10948:\n"))
            if 10939 <= rat_num <= 10948:
                break
            else:
                print("\nInvalid input.")
        except ValueError:
            print("\nInvalid input.")

    # filter dataframe to have just rows for that Animal
    cohort17_animal = cohort17_data[cohort17_data["Animal"] == rat_num]

    # create Day column based on Trial number
    cohort17_animal = cohort17_animal.copy()
    cohort17_animal.loc[:, "Day"] = (cohort17_animal["Trial"] - 1) // 6 + 1

    # average CIPL for each day
    avg_cipl_day = cohort17_animal.groupby("Day")["CIPL"].mean()

    # create and print plot
    plt.scatter(avg_cipl_day.index, avg_cipl_day.values, color='blue', marker='o')
    plt.title(f'Average CIPL for Rat {rat_num}')
    plt.xlabel("Day")
    plt.ylabel("Average CIPL")
    plt.grid(True)
    plt.show()


# Within day performance for each rat
def within_day_performance_indiv():
    # ask for rat num
    while True:
        try:
            rat_num = int(input("Enter rat number, 10939-10948:\n"))
            if 10939 <= rat_num <= 10948:
                break
            else:
                print("\nInvalid input.")
        except ValueError:
            print("\nInvalid input.")

    # filter dataframe to have just rows for that Animal
    cohort17_animal = cohort17_data[cohort17_data["Animal"] == rat_num]

    # create Day column based on Trial number
    cohort17_animal = cohort17_animal.copy()
    cohort17_animal.loc[:, "Day"] = (cohort17_animal["Trial"] - 1) // 6 + 1

    # unique color/marker for each day
    color_palette = sns.color_palette("husl", len(cohort17_animal["Day"].unique()))
    marker_cycle = ["o", "v", "s", "*"]

    plt.figure(figsize=(12, 8))

    # iterate through each day and plot CIPL for each trial
    for i, day in enumerate(cohort17_animal["Day"].unique()):
        subset = cohort17_animal[cohort17_animal["Day"] == day]
        color = color_palette[i]
        marker = marker_cycle[i % len(marker_cycle)]

        # plot points for day
        plt.scatter(subset["Trial"], subset["CIPL"], label = f'Day {day}', color = color,
                    marker = marker)

        # trend line
        sns.regplot(x = "Trial", y = "CIPL", data = subset, color = color, scatter = False)

    # labels and legend
    plt.xlabel("Trial")
    plt.ylabel("CIPL")
    plt.legend(loc = "center left", bbox_to_anchor = (1, 0.5))
    plt.title(f"Within Day Performance for {rat_num}")
    plt.tight_layout()

    plt.grid(True)
    plt.show()


def avg_daily_cipl_all():
    # create Day column based on Trial number
    cohort17_data.loc[:, "Day"] = (cohort17_data["Trial"] - 1) // 6 + 1

    # group by Day and calculate average CIPL for each day
    daily_avg_cipl = cohort17_data.groupby("Day")["CIPL"].mean().reset_index()

    # plot
    plt.scatter(daily_avg_cipl["Day"], daily_avg_cipl["CIPL"])

    # labels
    plt.xlabel("Day")
    plt.ylabel("Average CIPL")
    plt.title("Average Daily CIPL Across All Rats")

    plt.grid(True)
    plt.show()


# run function depending on data selection input
if data_num == 1:
    across_day_performance_indiv()
elif data_num == 2:
    within_day_performance_indiv()
elif data_num == 3:
    avg_daily_cipl_all()

