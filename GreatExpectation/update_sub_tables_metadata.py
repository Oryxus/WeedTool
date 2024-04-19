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
    # update json file
    with open(tier_metadata_path, WRITE) as file:
        json.dump(tables_metadata, file, indent=2)
