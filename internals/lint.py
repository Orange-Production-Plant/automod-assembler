import pathlib

# determines if rule is non-moderator exempt
def is_nme(rule):
    if ("moderators_exempt" in rule and rule["moderators_exempt"] == False):
        return True
    else:
        return False

def lint_nme(rule, file : pathlib.Path):
    if (is_nme(rule) and ".nme" not in file.suffixes):
        return (False, "Rule is non-moderator-exempt, but file is not properly labelled.")
    elif (not is_nme(rule) and ".nme" in file.suffixes):
        return (False, "Rule is labelled as being non-moderator-exempt, but rule does not contain this property.")
    else:
        return (True, "")
    
        




def lint(rule, file : pathlib.Path):
    
    nme = lint_nme(rule, file)
    if (not nme[0]):
        print("Warning in file {}. {}".format(file.name, nme[1]))
        return False
    
    return True