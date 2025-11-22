import json
import os
import yaml


def read_files():
    rules = {}
    rule_keys = set()
    path = "<location>"
    for (root, _, file) in os.walk(path):
        if ".github" in root:
            continue
        for f in file:
            if '.yml' in f:
                rule_details = {}
                file_name = root + "/" + f
                with open(file_name) as yaml_file:
                    rule = yaml.safe_load(yaml_file)
                    for key, value in rule.items():
                        if key in ("source", "name", "description", "id", "references", "authors"):
                            continue
                        rule_details[key] = value
                        rule_keys.add(str(key))
                    rules[file_name] = rule_details
    return rules, rule_keys


def analyze_rules(rules, rule_keys):
    rule_notes = {}
    for rule_key in rule_keys:
        rule_notes[rule_key] = {}
    for rule in rules:
        for key, values in rules.get(rule).items():
            if type(values) == list:
                for value in values:
                    for note_key in rule_notes:
                        rule_notes = update_notes(note_key, key, str(value), rule_notes)
            else:
                for note_key in rule_notes:
                    rule_notes = update_notes(note_key, key, str(values), rule_notes)
    return rule_notes


def update_notes(note_key, key, value, rule_notes):
    if key == note_key and value:
        try:
            rule_notes[note_key][value] += 1
        except:
            rule_notes[note_key][value] = 1
    return rule_notes


if __name__ == "__main__":
    rules, rule_keys = read_files()
    rule_notes = analyze_rules(rules, rule_keys)
    with open('metadata_output.json', 'w') as f:
        json.dump(rule_notes, f, indent=4)
