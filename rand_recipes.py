import os
import json
import random
# 原始文件夹路径
source_folder = r'./recipes'
# 目标文件夹路径，确保这个文件夹可以被创建
target_folder = r'./data/minecraft/recipes'
# 确保目标文件夹存在
if os.path.exists(target_folder):
    for root, dirs, files in os.walk(target_folder, topdown=False):
        for file in files:
            if file.endswith('.json'):
                os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
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
    recipe["result"] = result
    if recipe.get("show_notification") is None:
        recipe['show_notification'] = True
    with open(os.path.join(target_folder, name), 'w') as f:
        json.dump(recipe, f, indent=4)

print("处理完成，文件已保存至", target_folder)
