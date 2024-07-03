import json
from constant import *


def update_tables_metadata(tier_metadata_path: str) -> json:
    """Update tables path in tables metadata
        Base: tier/path/data
        Updated: model/tier/path/gx


    Args:
        tier_metadata_path (str): path to json file including tables metadata of BRONZE or SILVER

    Returns:
        json: updated json file including tables metadata
    """
    with open(tier_metadata_path, READ) as file:
        tables_metadata = json.load(file)

    for table in tables_metadata:
        table[PATH] = 'model/' + table[PATH]
        table[PATH] = table[PATH].replace("/data", "/gx")
        if "sats" in table[PATH]:
            # Replace "sats" with "satellites" and "data" with "gx"
            table[PATH] = table[PATH].replace("sats", "satellites")
    for table in tables_metadata:
        if not table["keys"]:
            del table['keys']   
    # update json file
    with open(tier_metadata_path, WRITE) as file:
        json.dump(tables_metadata, file, indent=2)

# update_tables_metadata(r"samples\GX\tables_metadata.json")
# import json

# # Read the JSON file
# with open(r'samples\GX\tables_metadata.json', 'r') as file:
#     data = json.load(file)

# # Iterate over each item in the JSON array
# for item in data:
#     # Check if the "keys" list exists and is not empty
#     if 'keys' in item and item['keys']:
#         # Extract and print the value of "keys"
#         keys_value = item['keys']
#         print("Keys:", keys_value)