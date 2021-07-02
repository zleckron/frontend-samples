from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():

    ingredients = ["White Flour","White Rice","Pasta","Bread","Chocolate Chip Cookies","Uncooked Ground Beef",
        "Uncooked Beef Roasts","Uncooked Beef Steaks","Bacon","Pork Chops","Ham","Bologna","Chicken Breast","Chicken Leg",
        "Turkey","Eggs","Milk","Cheddar Cheese","Ice Cream","Bananas","Oranges","Grapes","Lemons","Peaches","White Potatoes",
        "Iceberg Lettuce","Tomatoes","Broccoli","Sweet Peppers","Orange Juice","Beans","White Sugar","Margarine"]

    return render_template('index.html', ingredients_list=ingredients)

@app.route("/recipe", methods=["get", "post"])
def recipe():

    if request.method == 'POST':

        #return "Ingredients: " + ing1 + ing2 + ing3

        #return request.form
        print("Request form:", request.form)
        data = request.form
        print("Request args", data)
        matches = give_recipes(data)
        formatted_matches = format_matches(matches)

        return render_template('results.html', recipes=formatted_matches)

    else:
        print(request.method)
        return ("oh no")
def lower_list(raw_list):
    lower = []
    for elem in raw_list:
        lower.append(elem.lower())
    return lower

def make_recipes(path):
    recipes = []
    recipefp = open(path, "r")
    recipes_lines = recipefp.readlines()
    recipefp.close()
    #for each line, first item is the title
    for raw_line in recipes_lines:
        line = raw_line.strip()
        new_recipe = {}
        line_data = line.split(',')
        #print(line_data)
        #remember that the first
        new_recipe["Title"] = line_data[0]
        new_recipe["URL"] = line_data[1]
        for i in range(2, len(line_data) - 2, 4):
            new_recipe[line_data[i]] = float(line_data[i+1])
        recipes.append(new_recipe)
    return recipes

def match_recipes(pantry, recipes, max_cost):
    matches = []
    #for every recipe, get the price difference we would need to complete it
    for recipe in recipes:
        cost = 0.0
        to_buy = []
        needed_goods = recipe.keys()
        #for each ingredient required, we only care if we don't already have it
        #TODO: let user indicate quantity of ingredients that they have
        for good in needed_goods:
            #print(recipe[good])
            if good != "Title" and good != "URL":
                if not (good.lower() in lower_list(pantry)):
                    to_buy.append(good)
                    #will give us the cost of the food in this recipe
                    cost += recipe[good]
        if cost < max_cost:
            #add this recipe to matches
            matches.append([recipe, to_buy])
    return matches

def give_recipes(user_ingredients):
    print(type(user_ingredients))
    user_ingredients = dict(user_ingredients)
    values = [user_ingredients["ing1"][0], user_ingredients["ing2"][0],user_ingredients["ing3"][0], user_ingredients["max"][0]]
    #values = list(user_ingredients.values())
    print(len(values))
    print(values)
    #cut off the last value in the dict (it's the budget)
    matching = match_recipes(values[:-1], make_recipes("Recipes_URL.csv"), float(values[-1]))
    return matching
    #return render_template('results.html', ingredients_list=ingredients)

#matches is a list of 2D lists with dictionary as the first elem, list as the second elem
#formatted is a list of lists of strings
def format_matches(matches):
    formatted = []
    for match in matches:
        #get the Title
        header = match[0]["Title"]
        header = header + ": " + match[0]["URL"]
        header += '\n'
        details = ""
        details = details + "You still need to buy "
        for ingredient in match[1]:
            details = details + ingredient
            if ingredient != match[1][-1]:
                details += ", "
        formatted.append([header, details])
    return formatted

if __name__ == "__main__":
    app.run('0.0.0.0', port=80)
