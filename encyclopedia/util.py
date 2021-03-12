import re
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    
    f = open(filename, "w")
    f.write("# " + title)
    f.write("\n\n")
    f.write(content)
    f.close()


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        file_name = f"entries/{title}.md"         
        new_file = default_storage.open(file_name)   
        old = open(file_name,  "r")
        lines = old.readlines()
        del lines[0]
        old.close()
        new_file = open("temp", "w+")
        for line in lines:
            new_file.write(line)
        
        new_file = default_storage.open("temp")
        data = new_file.read().decode("UTF-8")
        new_file.close()
        os.remove("temp")
        return data
        # return new_file
    except FileNotFoundError:
        return None
