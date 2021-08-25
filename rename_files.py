import os

folder = '/Users/francois/Desktop/Cleaned Models'

for file in os.listdir(folder):
    if '.fbx' in file:
        new_name = ''
        for letter in file:
            # If the first letter, don't add _
            if new_name == '':
                new_name += letter.lower()
                continue

            # If uppercase letter or digit, add _ before it
            if letter.isupper() or letter.isdigit():
                # If the previous letter is not already an _, then add an _ before this letter
                if new_name[-1] == '_':
                    new_name += letter.lower()
                else:
                    new_name += '_' + letter.lower()
            else:
                new_name += letter.lower()
            
        os.rename(os.path.join(folder, file), os.path.join(folder, new_name))

print('DONE')