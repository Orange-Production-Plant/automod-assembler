import pathlib

# determines if rule is non-moderator exempt
def is_nme(rule):
    if ("moderators_exempt" in rule and rule["moderators_exempt"] == False):
        return True
    else:
        return False

def lint_nme(rule, file : pathlib.Path):
    if (is_nme(rule) and ".nme" not in file.suffixes):
        return False, "Rule is non-moderator-exempt, but file is not properly labelled."
    elif (not is_nme(rule) and ".nme" in file.suffixes):
        return False, "Rule is labelled as being non-moderator-exempt, but rule does not contain this property."
    else:
        return True, ""
    

valid_suffixes = [".yaml", ".disable", ".nme"]

def lint_suffixes(rule, file: pathlib.Path):
    for suffix in file.suffixes:
        if suffix not in valid_suffixes:
            return False, "Rule carries unknown suffix."
    
    return True, ""



lint_stages = [lint_suffixes, lint_nme]


def lint(rule, file : pathlib.Path):
    
    is_lint_okay = True

    for stage in lint_stages:
        is_rule_passed, msg = stage(rule, file)
        
        if (not is_rule_passed):
            print("Warning in file {}. {}".format(file.name, msg))
            is_okay = False
    
    return is_lint_okay