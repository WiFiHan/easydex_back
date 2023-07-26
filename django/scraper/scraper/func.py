import re

def remove_brackets_and_append(source_list):
    result_list = []
    pattern = r'\((.*?)\)'  # Regular expression pattern to match text inside parentheses

    for item in source_list:
        # Remove brackets and extract elements inside them using re.findall()
        elements_inside_brackets = re.findall(pattern, item)

        # Remove the brackets from the original string
        cleaned_item = re.sub(pattern, '', item).strip()

        # Append the cleaned item to the result_list
        result_list.append(cleaned_item)

        # Append elements inside brackets to the result_list
        result_list.extend(elements_inside_brackets)

    # Remove duplicated elements by converting the list to a set and then back to a list
    result_list = list(set(result_list))

    return result_list
