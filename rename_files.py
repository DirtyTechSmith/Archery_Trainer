import os

dir_name = 'C:\\Borderlands3\\OakGame\\Content\\Movies\\'

for file_name in os.listdir(dir_name):
    if not file_name.endswith('.bak'):
        continue

    new_name = file_name.replace('.bak', '.mp4')
    old_path = f'{dir_name}{file_name}'
    new_path = f'{dir_name}{new_name}'
    os.rename(old_path,new_path)
