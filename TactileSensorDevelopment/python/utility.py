import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import shutil
import time

def define_csv_save_location(parentDir, expSet):
    print("\n   --------------------")
    print("This run belongs to experiment set:", expSet, "\n")
    path_to_exp_dir =  os.path.join(parentDir, expSet)
    if os.path.isdir(path_to_exp_dir): 
        print("Directory " + expSet + " already exists. New folder is not created.")
    else: 
        os.mkdir(path_to_exp_dir)
        print("New folder with name: " + expSet + " is created.")
    input("Press enter to continue")
    print("\n\n")
    
    return path_to_exp_dir


def define_csv_save_location_input(parentDir):
    print("\n   --------------------")

    print("Enter csv folder name. If you don't care, just press enter")
    foldername = input()
    if foldername == "": 
        foldername += "testing"

    foldername += "_" + str(int(time.time() * 1000))

    path_to_exp_dir =  os.path.join(parentDir, foldername)

    if os.path.isdir(path_to_exp_dir): 
        print("Directory " + foldername + " already exists. If you continue the prvious file will be deleted.")
        if y_n_prompt("Are you SURE you want to continue? (y/n)"):
            shutil.rmtree(path_to_exp_dir)
            os.mkdir(path_to_exp_dir)
        else:
            print("\nExiting python program to deal with this folder.")
            sys.exit()
    else: 
        os.mkdir(path_to_exp_dir)
        print("New folder with name: " + foldername + " is created.")

    print("The folder name will be followed by '_unix time in ms'\n")
    return path_to_exp_dir, foldername


def plot_and_save_data(plottingData, xAxisLabel, yAxisLabel, label, savingData, 
                        filename, saveDir, display_plot = True, saveData = True, figsize = (6,8)):

    if display_plot:
        # plot the figures
        f, ax = plt.subplots(len(plottingData) ,1,figsize=figsize)
        
        for i in range(len(plottingData)): 
            
            # plotting
            for j in range(len(plottingData[i]) - 1): 
                ax[i].plot(plottingData[i][0], plottingData[i][j+1], label = label[i][j])

            # x axis label
            if xAxisLabel[i] is not None:
                ax[i].set_xlabel(xAxisLabel[i], fontsize = 15)
        
            # y axis title
            if yAxisLabel[i] is not None:
                ax[i].set_ylabel(yAxisLabel[i], fontsize = 15)

            # legend
            if None not in label[i]:
                ax[i].legend(loc = "best")

        plt.title(filename)
        plt.tight_layout()
        plt.show()

    if saveData:
        save_data = np.transpose(np.vstack(savingData))
        np.savetxt(saveDir + '/' + filename + ".csv", save_data, delimiter = ",")


def y_n_prompt(msg):
    prompt = False
    while 1:
        decision = input(msg)
        if decision == "y" or decision == "Y": 
            prompt = True
            break
        elif decision == "n" or decision == "N":
            break
    return prompt

def obtain_some_float_value(description_of_value, default_value, max_value, min_value):

    while 1: 
        value = input("Type the " + description_of_value + "and press enter.\n\
                            Press enter to obtain default value(" + str(default_value) + ")")

        if value == "":
            value = default_value 
            break   
        else: 
            try: 
                value = float(value)

                if value <= max_value and value >= min_value: 
                    break
                else: 
                    print("Enter number betwen", min_value, "and", max_value)
            except:
                print("Enter legitimate number")

    return value

def obtain_csv_filename(save_dir):
    while 1:
        print("\nEnter csv file name. If you don't care, just press enter")
        filename = input()
        if filename == "": 
            filename += "testing_" + str(int(np.random.random() * 1000000))

        files = os.listdir(save_dir)
        breakLoop = True
        for file in files: 
            if file == filename + ".csv": 
                print("You have a file with the same name. If you continue the prvious file will be overriden.")
                breakLoop = y_n_prompt("Are you SURE you want to continue? (y/n)")
        if breakLoop:
            break
    
    print("This data will correspond with csv with name:", filename + ".csv")

    return filename