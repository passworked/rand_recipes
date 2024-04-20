import os
import json
import random
# 原始文件夹路径
def format_item_string(input_string):
    """
    Format an item string from format 1 or format 2 to format 3.

    Format 1: '{"item": "minecraft:item_name"}'
    Format 2: '"minecraft:item_name"'
    Format 3: '{"count": number, "item": "minecraft:item_name"}'

    :param input_string: A string in format 1 or format 2.
    :return: A string in format 3.
    """
    # Check if input is in format 1 and convert to dict if so
    if input_string.strip().startswith('{'):
        item_dict = eval(input_string)  # Convert string representation of dict to actual dict
        # If 'count' is not in the dict, add it with a value of 1
        item_dict.setdefault('count', 1)
    else:
        # Input is in format 2, create a new dict with 'item' and default 'count'
        item_dict = {"count": 1, "item": input_string.strip('"')}

    # Convert dict back to string in format 3
    formatted_string = str(item_dict)
    return formatted_string

def format_item_string2(input_string):
    """
    Convert a string from format 1 or format 3 to format 2.

    Format 1: '{"item": "minecraft:item_name"}'
    Format 3: '{"count": number, "item": "minecraft:item_name"}'
    Format 2: '"minecraft:item_name"'

    :param input_string: A string in format 1 or format 3.
    :return: A string in format 2.
    """
    # Check if input is a dictionary in string form
    if input_string.strip().startswith('{'):
        # Convert string representation of dict to actual dict
        item_dict = eval(input_string)
        # Extract the 'item' field and format it as Format 2
        item_name = item_dict.get('item')
        return f'"{item_name}"'
    else:
        # If it's already in Format 2, just return it
        return input_string

def strip_quotes(input_string):
    """
    Remove surrounding single or double quotes from a string.

    :param input_string: A string potentially wrapped in single or double quotes.
    :return: A string without surrounding quotes.
    """
    # Check if the string starts and ends with single or double quotes
    if input_string.startswith(("'", '"')) and input_string.endswith(("'", '"')):
        # Remove the quotes from both ends
        return input_string[1:-1]
    return input_string  # Return the original string if no surrounding quotes

source_folder = r'./recipes'
# 目标文件夹路径，确保这个文件夹可以被创建
target_folder = r'./rand_recipes/data/minecraft/recipes'
# 确保目标文件夹存在
if os.path.exists(target_folder):
    for root, dirs, files in os.walk(target_folder, topdown=False):
        for file in files:
            if file.endswith('.json'):
                os.remove(os.path.join(root, file))
else:
    os.makedirs(target_folder)

# 步骤1：遍历原始目录收集战利品表文件的完整路径
recipes_paths = []
recipes_name = []
for root, _, files in os.walk(source_folder):
    for file in files:
        if file.endswith(".json"):  # 确保只处理JSON文件
            full_path = os.path.join(root, file)
            recipes_paths.append(full_path)
            recipes_name.append(file)

# 限制处理的文件数，可以根据需要修改
# recipes_paths = recipes_paths[:5]

# 读取所有结果
recipes_result = []
for recipe_path in recipes_paths:
    with open(recipe_path, 'r') as f:
        recipe = json.load(f)
        recipes_result.append(recipe.get('result', {}))
# 随机化结果
random.shuffle(recipes_result)

# 修改每个json文件并保存
for recipe_path, name, result in zip(recipes_paths, recipes_name, recipes_result):
    with open(recipe_path, 'r') as f:
        recipe = json.load(f)
    if recipe["type"] == 'minecraft:crafting_shapeless' or recipe["type"] == 'minecraft:crafting_shaped':
        recipe["result"] = eval(format_item_string(str(result)))
    elif recipe["type"] == 'minecraft:smelting' or recipe["type"] == 'minecraft:stonecutting':
        recipe["result"] = strip_quotes((format_item_string2(str(result))))
    if recipe.get("show_notification") is None:
        recipe['show_notification'] = True
    with open(os.path.join(target_folder, name), 'w') as f:
        json.dump(recipe, f, indent=4)

print("处理完成，文件已保存至", target_folder)
