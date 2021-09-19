# This is the backend Python code for the HealthAssistant chatbot developed using Google's Dialogflow framework
# The HealthAssistant chatbot provides the user with a personalized diet and exercise recommendation based on the user's
# responses to their age, weight, current weight, desired weight, health goals, previous injuries, and food allergies

from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    #the variables we will store information in to eventually give personalized recommendations
    user_name, age, current_weight, desired_weight, height, goal, injuries, food_allergies, age, age_based_rec, \
        l_exercises, l_food, old_bmi, new_bmi = ""

    #get the JSON object that stores the values from Dialogflow
    req = request.get_json(silent=False, force=False, cache=True)
    query_result = req.get('queryResult')

    if query_result['intent']['displayName'] == "UserInputsName/ask for age":
        # intent is user enters their name and bot asks for goal
        user_name = query_result.get('parameters').get('person').get('name')
        user_name = user_name[0].upper() + user_name[1:]  # get the name of the user

    elif query_result['intent']['displayName'] == "userInputsage/ask for current weights":
        # intent is user enters their age and bot asks for weight
        age = int(query_result.get('parameters').get('age').get('amount'))

    elif query_result['intent']['displayName'] == "UserInputsCurrentWeight/ask for desired weight":
        # intent is user enters their current weight and bot asks for desired weight
        current_weight = query_result.get('parameters').get('number')

    elif query_result['intent']['displayName'] == "UserInputsDesiredWeight/ask for height":
        # intent is user enters their desired weight and bot asks for height
        desired_weight = query_result.get('parameters').get('number')

    elif query_result['intent']['displayName'] == "userInputsHeight/ask for goals":
        # intent is user enters their height and bot asks for health goal
        height = query_result.get('parameters').get('number')

    elif query_result['intent']['displayName'] == "UserInputsGoal/ask for injuries":
        # intent is user enters their health goal and bot asks for injuries
        goal = query_result.get('queryText')

    elif query_result['intent']['displayName'] == "UserInputsInjuries/ask for food allergies":
        # intent is user enters their injuries and bot asks for food allergies
        injuries = query_result.get("queryText")

    elif query_result['intent']['displayName'] == "UserInputsAllergies/give health rec":
        # intent is user enters their allergies and bot will give personalized health recommendations
        food_allergies = query_result.get("queryText")

    old_bmi = round((float(current_weight) * 0.453592) / (
            (float(height) * 0.0254) ** 2), 1)  # this wil give the user's current BMI
    new_bmi = round((float(desired_weight) * 0.453592) / ((float(
            height) * 0.0254) ** 2), 1)  # this will give the user's desired BMI based on the weight goal they entered

    # the following code consists of the different free weight and machine related exercises to build muscle and the
    # muscles/body parts needed
    free_weight_list = ["bench press", "bicep curls", "shoulder press", "deadlifts", "dumbbell fly"]
    free_weight_dict = {"bench press": ["arms", "chest", "shoulders"], "bicep curls": ["arms"],
                        "shoulder press": ["arms", "back", "chest", "shoulders"],
                        "deadlifts": ["back", "glutes", "hamstrings"],
                        "dumbbell fly": ["arms", "chest", "shoulders"]}

    machine_list = ["leg press", "cables/pulleys", "pec deck", "lat pulldown", "lateral raises"]
    machine_dict = {"leg press": ["hamstrings", "quads"], "cables/pulleys": ["arms", "chest", "shoulders"],
                    "pec deck": ["chest"],
                    "lat pulldown": ["back"], "lateral raises": ["shoulders"]}

    # the following code consists of the different body weight and cardio related exercises to lose weight and the
    # the muscles and body parts needed
    bodyweight_list = ["pullups", "chinups", "pushups", "squats", "planks"]
    bodyweight_dict = {"pullups": ["back", "arms", "shoulders", "chest"],
                       "chinups": ["back", "arms", "shoulders", "chest"],
                       "pushups": ["chest", "shoulders", "arms"], "squats": ["hamstrings", "quads", "hip", "glutes"],
                       "planks": ["chest", "back", "shoulders"]}

    cardio_list = ["treadmill", "rowing machine", "elliptical"]
    cardio_dict = {"treadmill": ["hamstrings", "quads", "glutes", "cardiovascular", "chest"],
                   "rowing machine": ["shoulders", "back", "glutes", "quads", "chest", "cardiovascular"],
                   "elliptical": ["glutes", "hamstrings", "quads", "chest", "back", "arms", "cardiovascular"]}

    # these are lists of the recommended foods to build muscle and lose weight
    build_muscle_foods = ["quinoa", "brown rice", "buckwheat", "eggs", "chicken", "salmon", "tuna",
                          "greek yogurt",
                          "beans", "protein powders"]
    lose_fat_foods = ["eggs", "kale", "spinach", "collards", "salmon", "tuna", "avocados", "oats", "quinoa", "fruit",
                      "coconut oil"]
    
    #this will give an age based recommendation
    if age < 30:
        age_based_rec = "we recommend doing anaerobic (strength training) and aerobic (cardio) exercises."
    elif age < 40:
        age_based_rec = "we recommend doing more strength training with intervaled cardio a few days a week."
    elif age < 50:
        age_based_rec = "we recommend doing mostly cardio exercises and a little bit of strength training."
    elif age < 60:
        age_based_rec = "we recommend focusing on leg strength and combine it with sports like tennis and swimming."
    elif age >= 60:
        age_based_rec = "we recommend doing cardio and focus on things like yoga. It is also important to not push " \
                            "yourself too much at this age and just maintain consistency and discipline."

    l_exercises = [] # this list will consist of the exercises the user can do when injuries have been taken into account
    # we will now generate recommendation taking injuries into account
    injuries = [injuries]
    
    #loops necessary to be able to work with the list of injuries
    for first_bracket in injuries:
        for second_bracket in first_bracket:
            for all_injuries in second_bracket:
                injured = sorted(all_injuries.split(","))
                
                #if the goal is to build muscle
                if goal == "Build muscle":
                    #iterate through the free weight dictionary to see which which injuries prevent customers from doing certain exercises
                    for exercise in free_weight_dict:
                        for injury in injured:
                            injury = injury.strip()
                            if injury not in free_weight_dict[exercise] and exercise not in l_exercises:
                                l_exercises.append(exercise)
                            elif injury in free_weight_dict[exercise] and exercise in l_exercises:
                                l_exercises.remove(exercise)
                                break
                            elif injury in free_weight_dict[exercise]:
                                break
                    
                    #iterate through the machine dictionary to see which injuries prevent customers from doing certain exercises
                    for exercise in machine_dict:
                        for injury in injured:
                            injury = injury.strip()
                            if injury not in machine_dict[exercise] and exercise not in l_exercises:
                                l_exercises.append(exercise)
                            elif injury in machine_dict[exercise] and exercise in l_exercises:
                                l_exercises.remove(exercise)
                                break
                            elif injury in machine_dict[exercise]:
                                break
                                
                #if goal is to lose weight
                else:
                    #iterate through the bodyweight dictionary to see which injuries prevent customers from doing certain exercises
                    for exercise in bodyweight_dict:
                        for injury in injured:
                            injury = injury.strip()
                            if injury not in bodyweight_dict[exercise] and exercise not in l_exercises:
                                l_exercises.append(exercise)
                            elif injury in bodyweight_dict[exercise] and exercise in l_exercises:
                                l_exercises.remove(exercise)
                                break
                            elif injury in bodyweight_dict[exercise]:
                                break
                    
                    #iterate through the cardio dictionary to see which injuries prevent customers from doing certain exercises
                    for exercise in cardio_dict:
                        for injury in injured:
                            injury = injury.strip()
                            if injury not in cardio_dict[exercise] and exercise not in l_exercises:
                                l_exercises.append(exercise)
                            elif injury in cardio_dict[exercise] and exercise in l_exercises:
                                l_exercises.remove(exercise)
                                break
                            elif injury in cardio_dict[exercise]:
                                break

    if len(l_exercises) == 0: # this is the conditional for if there are no exercises to recommend which happens if the customer has too many injuries
        l_exercises = "we do not have any exercises that would be suitable for you"

    l_food = [] # this list will consist of the foods the user can eat when allergies have been taken into account
    #goal is to build muscle
    if goal == "Build muscle":
        for food in build_muscle_foods:
            if food not in food_allergies:
                l_food.append(food)
    
    #goal is to lose weight
    else:
        for food in lose_fat_foods:
            if food not in food_allergies:
                l_food.append(food)

    if len(l_food) == 0: #this is the conditional for if there are no foods to recommened which happens if the customer has too many allergies
        l_food = "We do not have any suitable foods for you."

    #when the customer is ready to get their recommendation, a JSON object will be returned to Dialogflow
    if query_result['intent']['displayName'] == "I'm ready":
        #if there is at least one exercise the user can do l_exercise will be a list
        if type(l_exercises) == list:
            return {"fulfillmentText": "Your current BMI is " + str(old_bmi) + " and the BMI you are trying to get to is " +
                    str(new_bmi) + ". Based on your injuries, we recommend doing the following exercises: " + ", ".join(l_exercises) +
                    ". Based on your age " + age_based_rec + " We also recommend following a diet that consists of the following "
                    "foods: " + ", ".join(l_food) + ". Our final recommendation is to exercise caution when doing exercise so you do "
                    "not suffer more injuries. Good luck with your health plan."}
        
        #if there are no exercises for the user to do due to injuries, l_exercise is a string as shown in line 167
        else:
            return {"fulfillmentText": "Your current BMI is " + str(old_bmi) + " and the BMI you are trying to get to is "
                    + str(new_bmi) + ". Based on your injuries," + str(l_exercises) + ". Based on your age " + age_based_rec +
                    " We also recommend following a diet that consists of the following foods: " + ", ".join(l_food) + ". Our final "
                    "recommendation is to exercise caution when doing exercise so you do not suffer more injuries. "
                    "Good luck with your health plan."}

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()
