# -*- coding: utf-8 -*-
#
#       Comp 167: Final Project 
#       Calculating the risk factor based on the inputtted demographics for
#       HIV, coronary heart disease, stroke and diabetes within the U.S.
#       Written By: Becky Cutler


import collections, sys,string, argparse, re
import string, math, operator, sys, os

# Node for the graph that contains the key (i.e. male or femaile, etc) and the
# value (risk factor represented as a percentage) 
class Node:
        def __init__ (self, key, value):
                self.id = key
                self.risk = value

# outputs a print statement that explains the general concept of the program
def explain_program():

        print("\nThis program calculates the risk factor for HIV\
, coronary heart disease, a cerebrovascular accident (stroke) and diabetes (type\
 1 and 2) based on the inputted demographic data of U.S. residents.\n\nIf you wish to learn \
more about these diseases/viruses, simply enter 'info' after the \
first promp appears.\n\nIf you wish \
to quit, type 'q' when asked for the specified disease/virus\n") 

# retrieves the data files from the command line 
def get_files():

        # getting the data from the command line
        parser = argparse.ArgumentParser(description= 'Test.')
        parser.add_argument('hiv_file', help= 'test')
        parser.add_argument('heart_disease', help= 'data for heart disease')
        parser.add_argument('stroke', help= 'data for stroke')
        parser.add_argument('diabetes', help= ' data for diabetes')

        # Parsing the arguments and opening the files 
        args = parser.parse_args()
        hiv = args.hiv_file
        hiv_file = open(hiv, 'r')
        heart_disease = args.heart_disease
        heart_file = open(heart_disease, 'r')
        stroke = args.stroke
        stroke_file = open(stroke, 'r')
        diabetes = args.diabetes
        diabetes_file = open(diabetes, 'r')

        return hiv_file, heart_file, stroke_file, diabetes_file

# Puts the given data file into an array with the associated identifier and 
# risk
def initialize_risk_array(input_file):
        risks = []
        
        # looping through the data in the file and appending it onto the list
        for line in input_file:
                id, risk = line.split()
                new_node = Node(id, float(risk))
                risks.append(new_node)

        return risks

# determine which disease the user wishes to know about 
def determine_disease():
        
        disease = raw_input("Please choose a disease or virus: HIV, \
Coronary Heart Disease, Stroke, Diabetes\n")
        return disease.lower()    

def get_info():
        print("Human immunodeficiency virus (HIV) is a chronic virus  that can \
lead to acquired immunodeficiency syndrome (AIDS). HIV can be spread through \
certain bodily fluids such as blood and semen. Currently, there are \
approximately 1.2 million people in the United States infected with HIV, 14% \
of whom are unaware that they are infected.\n")

        print("Coronary heart disease is caused from plaque buildup in the \
arteries of the heart. This plaque is made from fatty materials which block \
the pathway that carries blood and oxygen to the heart. It is the number \
one cause of death for both men and women.\n")

        print("A stroke happens when there is a temporary reduction in the \
amount of blood flowing to the brain. When this occurs, the brain lacks \
necessary nutrients and oxygen, causing cells to die. Each year more than \
795,000 people in the U.S. suffer from a stroke.\n")

        print("Diabetes mellitus (diabetes) refers to an excess amount of \
glucose in the blood. This set of diseases can cause serious health problems \
and lead to a higher risk factor for diseases such as coronary heart disease. \
Approximately 9.3% of the U.S. population has diabetes.\n")


############ calculates the risk factor for HIV based on user input ###########
def hiv_risk_factor(hiv_array):
        
        risk = 0

        gender = raw_input("Please enter your gender (male/female):\n")
        sex_orientation = raw_input("Please enter your sexual \
orientation (heterosexual/homosexual):\n").lower()
        race = raw_input("Please enter your race (Caucasian, African American, \
Asian, Hispanic/Latino, Other):\n").lower()
        race = race.replace(" ", "")
        age = raw_input("Please enter your age\n")
        age = int(age)
        iud = raw_input("Do you use injection drugs? (yes or no)\n").lower()

        if (iud == 'yes'):
                iud = 'iud'

        if (age < 13):
                # there is not enough data for people under 13
                return risk
        elif(age <= 18):
                age = 'under18'
        elif( age > 18 and age < 25):
                age = '19-24'
        elif(age >= 25 and age < 45):
                age = '25-44'
        elif(age >= 45 and age < 65):
                age = '45-64'
        else:
                age = '65+'

        # walking through the list of hiv data
        for node in hiv_array:
                if(gender == node.id):
                        risk += node.risk
                if(sex_orientation == node.id):
                        risk+= node.risk
                if(race == node.id):
                        risk+= node.risk
                if(age == node.id):
                        risk+= node.risk
                if (iud == node.id):
                        risk += node.risk

        # checking for a homosexual male because they are at a higher risk for
        # contracting hiv/aids
        if (gender == 'male' and sex_orientation == 'homosexual'):
                sex_orientation = 'yes'

        return risk, sex_orientation, iud

############ determines the risk factor for stroke and heart disease ##########
def heart_stroke_risk(data):
       
        risk = 0

        # getting the demographic information from the user 
        gender = raw_input("Please enter your gender (male/female):\n")
        gender = gender.lower()
        age = raw_input("Please enter your age:\n")
        age = int(age)
        race = raw_input("Please enter your race (Caucasian, African American, \
Asian, Hispanic/Latino, Other):\n").lower()
        race = race.replace(" ", "")

        diet = raw_input("Is your diet high in saturated fats? (yes or no)\
                          \n").lower()
        diabetes = raw_input("Do you have Type 2 diabetes? (yes/no)\n").lower()
        active = raw_input("Are you physically active for at least 3 hours each \
week? (yes or no)\n").lower()

        if(age < 18):
                # there is not enough data for thoes under 18
                return risk, diet, diabetes, active
        elif(age >= 18 and age < 45):
                age = '18-44'
        elif(age >= 45 and age < 65):
                age = '45-64'
        elif(age >= 65 and age < 75):
                age = '65-74'
        else:
                age = '75+'

        # walking through the data 
        for node in data:
                if(gender == node.id):
                        risk += node.risk
                if(race == node.id):
                        risk+= node.risk
                if(age == node.id):
                        risk+= node.risk

        return risk, diet, diabetes, active


#################### determining the risk for diabetes ########################
def diabetes_risk(diabetes_data):
        risk = 0

        # getting the demographic information from the user 
        gender = raw_input("Please enter your gender (male/female):\n")
        gender = gender.lower()
        age = raw_input("Please enter your age:\n")
        age = int(age)
        race = raw_input("Please enter your race (Caucasian, African American, \
Asian, Hispanic/Latino, Other):\n").lower()
        race = race.replace(" ", "")

        blood_pressure = raw_input("Do you have high blood pressure? (yes/no)\
                                   \n").lower()
        obese = raw_input("Are you overweight or obese? (yes/no)\n").lower()
        active = raw_input("Are you physically active for at least 3 hours each \
week? (yes or no)\n").lower()

        if(age < 45):
                age = '0-44'
        elif(age >= 45 and age < 65):
                age = '45-64'
        elif(age >= 65 and age < 75):
                age = '65-74'
        else:
                age = '75+'

        demographics = gender + race + age

        for node in diabetes_data:
                if (demographics == node.id):
                        risk = node.risk

        return risk, blood_pressure, obese, active                

# based of off the user's input, it prints out suggestions to lower the risk of
# coronary heart disease
def reduce_heart_disease(diet, diabetes, active):
        if (diet == 'yes'):
                print("Additionally, a diet high in saturated \
fats causes approximately 31% of coronary heart disease cases\n")
                print("In order to reduce your risk of coronary heart disease \
be sure to eat food that is low in fat and cholesterol. Foods such as fresh \
fruits and vegetables, whole grains and fish are proven to help prevent heart \
disease.\n")
        if (diabetes == 'yes'):
                print("Type 2 diabetes is one of the leading \
risk factors for coronary heart disease. With uncontrolled diabetes, you are \
twice as likely to develop coronary heart disease\n")
                print("In order to control your diabetes, be sure to keep a \
healthy diet (fish, turkey, whole grains, leafy grains), perform 30-60 minutes \
of physical activity at least 3 days a week, check your blood glucose levesl \
daily and do not smoke.\n")

        if(active == 'no'):
                print("Due to your lack of physical activity,\
you are at a higher risk of developing coronary \
heart disease. You can reduce your risk by \
approximately 30% with at least 3 hours of \
moderate physical activity per week.\n")


# based of off the user's input, it prints out suggestions to lower the risk of
# contracting hiv
def reduce_hiv(sex_orientation, iud):

        if (sex_orientation == 'yes'):
                print("Because gay and bisexual men are more affected by HIV \
than any other group, you are at a higher risk of contracting the infection. \
It is important to use a condom every time you engage in sexual activity to \
lower your risk\n") 
        
        if (iud == 'iud'):
                print("Because you inject drugs, you are at a higher risk of \
contracting HIV. To reduce this risk, do not use ilegal injection drugs, \
make sure your injection equiptment is sterile and never share it with \
others\n")

# based of off the user's input, it prints out suggestions to lower the risk of
# having a stroke
def reduce_stroke(risk, diet, diabetes, active):

        had_stroke = raw_input("Have you suffered from a prior \
stroke? (yes/no)\n").lower()
        smoke = raw_input("Do you smoke? (yes/no)\n").lower()
        blood_pressure = raw_input("Do you have high blood \
pressure? (yes/no)\n").lower()

        print_risk_factor(risk)

        if (had_stroke == 'yes'):
                print ("Because you have had a prior stroke, you are almost 10\
 times more likely to have a stroke then someone of the same age and \
gender who has not suffered from a stroke\n")
        if (smoke == 'yes'):
                print ("Smoking causes clots and plaque build up. In order \
to reduce your risk of haivng a stroke, it is necessary to quit smoking\n")
                print("Because you smoke, your risk factor is double what it would be \
if you did not smoke. Thus, to account for your smoking habit:")
        print_risk_factor(risk * 2)

        if (blood_pressure == 'yes'):
                print ("High blood pressure is the greatest cause of stroke \
and is also the most vital controllable risk factor. In order to significantly \
reduce your risk of having a stroke, try to lower your blood pressure\n")
        if (diet == 'yes'):
                print("A diet filled with saturated and trans fats can \
increase blood pressure and raise cholesterol, which both significantly \
increase the risk of having a stroke. Because of this, it is important \
to have at least five servings of fuits and each day\n")
        if (diabetes == 'yes'):
                print("Because you have diabetes, you have a higher risk of \
having a stroke because you likely have high blood pressure and cholesterol. \
It is important to control your diabetes and maintain a health diet.\n")
        if (active == 'no'):
                print(" Because you are inactive, you are more likely to have \
high blood pressure and cholesterol and therefore are at a greater risk for \
haivng a stroke. It is important to get approximately 30 minutes of exercise \
each day to lower your risk.\n")


# based of off the user's input, it prints out suggestions to lower the risk of
# contracting diabetes
def reduce_diabetes(blood_pressure, obese, active):
        if (blood_pressure == 'yes'):
                print("Because you have high blood pressure, you have a higher \
risk of getting diabetes, specifically type 2. In order to lower your risk, \
it is important to lower your blood pressure.\n")
        if (obese == 'yes'):
                print("Since you are overweight, you have more fatty tissues, \
which makes your cells resistant to insulin and increases your risk of getting \
diabetes. Try to loose weight by maintaining an active and healthy lifestyle.\n")
        
        if (active == 'no'):
                print("Because you are not physically active, you have a \
higher risk of getting diabetes. Working out helps you loose fatty tissue \
and helps your cells become more responsive to insulin.\n")


# outputts the given risk factor to std output
def print_risk_factor(risk):
        print "\nYour risk factor out of 100 is:"
        print risk
        print '\n'

# primary function in the program, it gets the specified disease/virus from the
# user, determines the correct risk factor, and outputs various suggestions to
# lower the risk factor if needed
def determ_risk_factor(hiv_array, heart_disease, stroke, diabetes_data):
       
        disease = ''
        no_data = "Unfortunately, there is not enough data to \
calculate your risk factor from the given demographics\n"

        # while the user does not type 'q' (quit)
        while (disease != 'q'):
                # first, determine the disease from the user
                disease = determine_disease()

                if (disease == 'info'):
                        get_info()

                # if the user chose HIV        
                elif (disease == 'hiv'):
                        risk, sex_orientation, iud =  hiv_risk_factor(hiv_array)
                        if (risk == 0):
                                print no_data 
                        else:
                                print_risk_factor(risk)
                                if(sex_orientation == 'yes' or iud == 'iud'):
                                        reduce_hiv(sex_orientation, iud)

                # If the user chose Coronary Heart Disease
                elif (disease == 'coronary heart disease'):
                        risk, diet, diabetes, active = heart_stroke_risk(heart_disease)
                        if (risk == 0):
                                print no_data
                        else:
                                print_risk_factor(risk)
                                # prints out suggestions to reduce  the risk of
                                # heart disease
                                reduce_heart_disease(diet, diabetes, active)

                # if the user chose Stroke
                elif (disease == 'stroke'):
                        risk, diet, diabetes, active = heart_stroke_risk(stroke)
                        if (risk == 0):
                                print no_data 
                        else:
                                reduce_stroke(risk, diet, diabetes, active)
                
                # if the user chooses diabetes
                elif (disease == 'diabetes'):
                        risk, blood_pressure, obese, active = diabetes_risk(diabetes_data)
                        if (risk == 0):
                               print no_data
                        else:
                                print_risk_factor(risk)
                                reduce_diabetes(blood_pressure, obese, active)
                                

                # If the user's input was not recognized 
                elif (disease != 'q'):
                        print "Oops! You did not specify a known disease\n"


############################# main implementation #############################

# Explaining the program to the user
explain_program()

# getting the data files from the command line
hiv_file, heart_file, stroke_file, diabetes_file = get_files()

# initializing the data
disease = ""
hiv_array = initialize_risk_array(hiv_file)
heart_disease = initialize_risk_array(heart_file)
stroke = initialize_risk_array(stroke_file)
diabetes = initialize_risk_array(diabetes_file)

#closing the files
hiv_file.close()
heart_file.close()
stroke_file.close()
diabetes_file.close()

# determine the risk factor for the user specified desease/virus
determ_risk_factor(hiv_array, heart_disease, stroke, diabetes)

# delete lists 
del hiv_array[:]
del heart_disease[:]
del stroke[:]
del diabetes[:]
