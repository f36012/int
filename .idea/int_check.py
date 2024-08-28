import re
import csv
def extract_interfaces_and_check_dot1x(filename):
    with open(filename, 'r') as file:
        text = file.read()
    pattern = re.compile(r'interface\s+(\S+)(.*?)(?=\n!)', re.DOTALL)
    matches = pattern.findall(text)
    seen_interfaces = set()
    results = []
    for interface, content in matches:
        interface = interface.strip()
        if interface in seen_interfaces:
            continue
        seen_interfaces.add(interface)
        dot1x_present = 'yes' if 'dot1x' in content else 'no'
        results.append((interface, dot1x_present, filename))
    return results
config_files = ['config.txt', 'config_2.txt']
all_results = []
for config_file in config_files:
    results = extract_interfaces_and_check_dot1x(config_file)
    all_results.extend(results)
with open('output_combined.csv', 'w', newline='') as csvfile:
    fieldnames = ['interface', 'dot1x', 'source_file']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for interface, dot1x, source_file in all_results:
        writer.writerow({'interface': interface, 'dot1x': dot1x, 'source_file': source_file})
print("Results have been written to output_combined.csv")
