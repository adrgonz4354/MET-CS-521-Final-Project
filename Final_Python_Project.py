'''Adrian Gonzalez
CS-521 - Summer 1
06/07/2020
Final Project'''

''' With this program the user will input symptoms and will be given a diagnosis and treatment plan'''


import datetime
import os

symptom_list = {"1": "fever", "2":"aching muscles","3":"chills and sweats","4":"headache", "5":"nasal congestion",
                "6":"sore throat","7":"fatigue and weakness","8":"cough", 
                "9":"shortness of breath", "10":"loss of taste or smell","11":"chest congestion",
                "12":"runny nose", "13":"nausea", "14": "vomiting", "15":"diarrhea", "16":"aching sensation in your chest",
                "17":"heartburn or abdominal pain", "18":"cold sweat", "19": "Lightheadedness", "20":"sudden dizziness"}

current_directory = os.getcwd()

class condition:
    '''
        Description types:
            
            illness
            emergency
        
    '''
    def __init__(self, condition_name, condition_symptoms, condition_treatment, condition_type):
        self.condition_name = condition_name
        self.condition_symptoms = condition_symptoms
        self.condition_treatment = condition_treatment #must be a list
        self.condition_type = condition_type
        
        self.__description = ""
        self.__symptoms_for_spec_illness = "" #symptoms for a specific illness
        for k in symptom_list:
            if k in self.condition_symptoms:
                self.__symptoms_for_spec_illness +=(symptom_list[k] + ", ")
        self.__c_t_l ="" #for converting treatment plan list into a proper sentence or dotted list
        for t in self.condition_treatment:
            self.__c_t_l+=("*"+t + "\n") 
        if(self.condition_type == "illness"):
        
            self.__description = self.condition_name + " is an illness that can cause "   + self.__symptoms_for_spec_illness
            self.__treatment_plan = "In order to treat " + self.condition_name + ", you can do the following: \n" + self.__c_t_l
        elif(self.condition_type == "emergency"):
            self.__description = condition_name + " is a medical emergency that can cause " + self.__symptoms_for_spec_illness
            self.__treatment_plan = "This is a medical emergency, PLEASE GO TO A HOSPITAL IMMEDIATELY!"
        else:
            print("Invalid illness-type")
    def set_similarities(self, value):
        self.__perc = value
    
    def get_similarities(self):
        return self.__perc
        
    def discharge(self):
        time_of_discharge = datetime.datetime.now()
        file_name = (self.condition_name
                     + "_" + str(time_of_discharge.year)
                     + "_" + str(time_of_discharge.day)
                     + "_" + str(time_of_discharge.hour)
                     + "_" + str(time_of_discharge.minute)
                     + "_" + str(time_of_discharge.second) + ".txt")
        try:
            write_to_directory = "/Discharge_Files"
            file_loc = os.path.join(current_directory+write_to_directory,file_name)
            file = open(os.path.join(current_directory+write_to_directory,file_name), "a+")
        
            with open(file_loc, "r+") as f:
                f.seek(0)
                f.write(self.__description + "\n" + 
                        self.__treatment_plan)
                f.truncate()
                print("You can find discharge notes in:" + str(file_loc))
        except EnvironmentError: #used if the folder cannot be found
            print("An error has occured")
        #do nothing for now
        pass
    def __gt__(self, other):
        perc = other.get_similarities()
        if(self.get_similarities() > perc):
            return True
        else:
            return False
#flu variables
flu_symptoms = ("1","2","3","4","5","6", "7", "8")
flu_treatment = ["Rest in bed", "Drink plenty of liquids","Take (OTC) fever reducer",
                 "take anitviral medications such as tamiflu if needed"]

# covid 19 variables
covid_19_symptoms =["1","3","8", "9","7", "2","10","6","11","12","13","14","15"]
covid_19_treatment = ["Rest in bed", "Drink plenty of liquids","Take (OTC) fever reducer", "Quarantine for 14 days",
                      "Get tested at local covid 19 test site"]

# heart attack variables
heart_attack_symptoms = ["16","13","9","18","7","19","2"]
heart_attack_treatment = ["Call 911 for emergency medical help"]

#common cold variables
common_cold_symptoms = ["5","6","8","11","12"]
common_cold_treatment = ["Rest","Soothe a sore throat","Combat stuffiness","Relieve pain","Sip warm liquids",
                         "Add moisture to the air","(OTC) cold and cough medications"]
# Stomach flu
stomach_flu_symptoms = ["1","3","7","13","14","15","18","19","20"]
stomach_flu_treatment = ["drink plenty of fluids", "(OTC) medications such as peptobismal, etc",
                         "BRAT diet", "plenty of rest"]
program_running = True
illness_list = {"flu" : condition("flu", flu_symptoms, flu_treatment, "illness"),
                "covid 19" : condition("Covid 19",  covid_19_symptoms, covid_19_treatment, "illness"), 
                "heart attack" : condition("Heart_Attack", heart_attack_symptoms, heart_attack_treatment, "emergency"),
                "common cold" : condition("Common Cold", common_cold_symptoms, common_cold_treatment, "illness"),
                "stomach flu": condition("Stomach Flu", stomach_flu_symptoms, stomach_flu_treatment, "illness")}
illness_list_names_only = [] #this is only for iterating for names
symptom_comparison = []

def check_symptoms():
    for t in illness_list:
        illness_list_names_only.append(t)
    for i in range(1, len(symptom_list)):
        symptoms_1 = input("Do you have "+ symptom_list[str(i)] + "? y/n: ")
        if symptoms_1.lower() == "y":
            symptom_comparison.append(str(i))
        elif symptoms_1.lower() == "n":
            pass
    temp_data = {}
    for n in range(len(illness_list)):
        similarities = 0 #this variable will be used to take in percentage of the similarities out of the percentage ceiling
        r = illness_list[illness_list_names_only[n]].condition_symptoms #this will take the list of symptoms that will be compared
        percentage_ceiling = len(r)
        for j in range(len(symptom_comparison)): #This for-statement will test whether there is a similar item in the list or not
            if symptom_comparison[j] in r:
                similarities +=1
            temp_data.update({illness_list_names_only[n]: ((similarities/percentage_ceiling) * 100)})
    data = set(temp_data.values())
    data = sorted(data)
    illness_percentage = data[len(data) - 1] #takes the illness with the highest percent of matching symptoms
    illness = ""
    for k in temp_data:
        if temp_data[k] == illness_percentage:
            illness = k
    diagnosis_object = condition(illness, illness_list[illness].condition_symptoms, 
                                 illness_list[illness].condition_treatment, illness_list[illness].condition_type)
    print("You have been diagnosed with: " + illness)
    ask = input("Would you like discharge notes? (y/n): ")
    for r_ in temp_data:
        illness_list[r_].set_similarities(temp_data[r_])
        #print(illness_list[r_].get_similarities())
    treshold = 70
    if ask == "y":
        diagnosis_object.discharge()
        print("Other possible illnesses were:")
        for y in illness_list:
            if(illness_list[illness] > illness_list[y]) and (illness_list[y].get_similarities() > treshold):
                print(illness_list[y].condition_name)
    elif ask == "n":
        pass 

#Welcome message for the program
print("Welcome to the Symptom Checker")
print("To start checking your symptoms, do $start, if you want to exit, do $exit ")
print("If you want help, do $help, if you want to view the credits, do $credits")

#Main loop
while program_running:
    
    cmd = input("(Symptom Checker) >") 
    if (cmd.lower() == "$start"):
        check_symptoms()
    elif (cmd.lower() == "$exit"):
         break
    elif (cmd.lower() == "$help"):
        print("To start checking your symptoms, do $start, if you want to exit, do $exit ")
        print("If you want help, do $help, if you want to view the credits, do $credits")
    elif (cmd.lower() == "$credits"):
        print("Symptom Checker created by Adrian Gonzalez ")
        print("For MET-CS-521 (Information Structures with Python) at Boston University ")
        print("17th of June, 2020")
    else:
        print("Invalid command, if you don't know any commands, do $help")