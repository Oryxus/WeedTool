import json
from pyapacheatlas.core import AtlasEntity
from uuid import uuid4
from collections import OrderedDict
import os
import sys

sys.path.append(os.path.abspath("../"))


type_name = "table_entity_def"
join = os.path.join


def convert_ordered_table(data: dict) -> OrderedDict:
    """
    Converts a dictionary representing table data into an ordered dictionary
    with specific fields in a predefined order.

    Args:
    - data (dict): A dictionary containing table data.

    Returns:
    - OrderedDict: An ordered dictionary representing the table data with
      fields ordered as ['typeName', 'attributes'], where 'attributes' contains
      a subset of fields from the input data in the order defined by the 'fields' list.

    """
    fields = ["name", "description", "dataCustodian",
              "sourceSystem", "path", "fileType", "dataPeriod", 
              "frequency", "dataRetention", "nameFormat", "dataProcessingType", "qualifiedName"]

    items = []

    for f in fields:
        if data["attributes"].__contains__(f):
            items.append((f, data["attributes"][f]))

    return OrderedDict(
        [
            ("typeName", data["typeName"]),
            ("attributes", OrderedDict(list(items)))
        ]
    )


def convert_ordered_column(data: dict) -> OrderedDict:
    """
    Converts a dictionary representing column data into an ordered dictionary
    with specific fields in a predefined order.

    Args:
    - data (dict): A dictionary containing column data.

    Returns:
    - OrderedDict: An ordered dictionary representing the column data with
      fields ordered as ['typeName', 'attributes'], where 'attributes' contains
      a subset of fields from the input data in the order defined by the function.

    """
    return OrderedDict(
        [
            ("typeName", data["typeName"]),
            ("attributes", OrderedDict(
                list(
                    {
                        "name": data["attributes"]["name"],
                        "description": data["attributes"]["description"],
                        "tableName": data["attributes"]["tableName"],
                        "key": data["attributes"]["key"],
                        "dataType": data["attributes"]["dataType"],
                        "glossaryTerm": data["attributes"]["glossaryTerm"],
                        "qualifiedName": data["attributes"]["qualifiedName"]
                    }.items()
                )
            )
            )
        ]
    )


def ordered_dict_serializer(object: object) -> dict:
    """
    Serializer function to convert an object to a dictionary. If the object
    is an instance of OrderedDict, it converts it to a regular dictionary.

    Args:
    - obj: The object to be serialized.

    Returns:
    - dict: The serialized object as a dictionary.
    """
    if isinstance(object, OrderedDict):
        return dict(object)
    return object


def is_dir_not_path_exist(path: str) -> bool:
    """
    Checks if the given path does not exist or if it exists but is a directory.

    Args:
    - path (str): The path to be checked.

    Returns:
    - bool: True if the path does not exist or is a directory, False otherwise.

    """
    return not os.path.isfile(path) and not os.path.exists(path)


def write_entity_to_json_file(
    file_name: str,
    dir_path: str,
    entity: AtlasEntity,
    entity_type: str = "table"
) -> dict:
    """
    Writes the attributes of an AtlasEntity object to a JSON file.

    Args:
    - file_name (str): The name of the output JSON file.
    - dir_path (str): The directory path where the JSON file will be saved.
    - entity (AtlasEntity): The AtlasEntity object containing the attributes to be written.
    - entity_type (str): The type of entity ("table" or "column"). Defaults to "table".

    Returns:
    - dict: The JSON data that was written to the file.
    """
    if is_dir_not_path_exist(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    output = entity.to_json()
    output.pop("guid")
    output['attributes'].pop("columnName", None)

    if entity_type == "table":
        output = convert_ordered_table(output)
    else:
        output = convert_ordered_column(output)

    full_path = join(dir_path, file_name)
    with open(full_path, "w+", encoding='utf-8') as f:
        json.dump(output, f, indent=4, default=ordered_dict_serializer,
                  ensure_ascii=False)
    return output


def to_entity(
    guid: str,
    name: str,
    qualified: str,
    description: str,
    attrs: dict = None,
    type_name: str = type_name
) -> AtlasEntity:
    """
    Creates an AtlasEntity object with the specified attributes.

    Args:
    - guid (str): The GUID of the entity.
    - name (str): The name of the entity.
    - qualified (str): The qualified name of the entity.
    - description (str): The description of the entity.
    - attrs (dict): Additional attributes of the entity. Defaults to None.
    - type_name (str): The type name of the entity. Defaults to the global variable 'type_name'.

    Returns:
    - AtlasEntity: The created AtlasEntity object.

    """
    entity = AtlasEntity(
        name=name,
        qualified_name=qualified,
        description=description,
        typeName=type_name,
        attributes=attrs,
        guid=guid
    )
    return entity


def get_attr_by_table_type(table_type: str, table: object) -> tuple:
    """
    Retrieves attributes and qualified name based on the type of table.

    Args:
    - table_type (str): The type of the table ("dataset", "ref", or any other).
    - table (object): The table object containing attributes.

    Returns:
    - tuple: A tuple containing attributes dictionary and qualified name.

    """
    qualifiedName = table["qualifiedName"]
    if table_type == "dataset":
        attrs = {
            "path": table["path"],
            "fileType": table["fileType"],
            "sourceSystem": table["sourceSystem"],
            "description": table["description"],
            "dataCustodian": table["dataCustodian"],
            "dataPeriod": table["dataPeriod"],
            "frequency": table["frequency"],
            "dataRetention": table["dataRetention"],
            "nameFormat": table["nameFormat"],
            "dataProcessingType": table["dataProcessingType"],
        }
    elif table_type == "ref":
        attrs = {
            "path": table["path"],
            "fileType": table["fileType"],
            "description": table["description"],
            "dataCustodian": table["dataCustodian"],
        }
    else:
        attrs = {
            "fileType": table["fileType"],
            "path": table["path"],
            "description": table["description"],
            "dataCustodian": table["dataCustodian"]
        }
    return attrs, qualifiedName


def write_table(
        output_dir_path: str,
        table_type: str,
        guid: str,
        table: object
):

    attrs, qualified_name = get_attr_by_table_type(table_type, table)

    table_name = table[f"{table_type}Name"] if table_type != "dataset" else os.path.basename(
        table[f"{table_type}Name"])

    entity = to_entity(
        guid,
        table_name,
        #    f"{table_name}@{type_name}"
        qualified_name,
        table['description'],
        attrs=attrs
    )

    if table_type != "dataset":
        table_dir = join(output_dir_path, table_name)
    else:
        table_name = os.path.basename(table_name)
        table_dir = output_dir_path

    write_entity_to_json_file(f"{table_name}.json", table_dir, entity)

    # columns
    cols = table['columns']
    for col in cols:
        col["dataType"] = col["dataType"].lower()

        entity = to_entity(
            guid,
            col["columnName"],
            #    f"{col['columnName']}@{tbl_name}",
            col["qualifiedName"],
            col['description'],
            type_name="column_entity_def",
            attrs=col,
        )

        column_dir = join(table_dir, "columns")

        write_entity_to_json_file(f"{col['columnName']}.json",
                        column_dir, entity, "column")


def write_all(
        input_file_path: str,
        output_dir_path: str,
        table_type: str
):

    with open(input_file_path, "r", encoding='utf-8') as f:
        tables = json.load(f)

    for table in tables:
        guid = uuid4().__str__()

        if table_type == "dataset":
            output_path = join(output_dir_path,
                               table["domain"], table["datasetName"])
        elif table_type == "ref":
            output_path = join(output_dir_path, table["refName"])
        else:
            output_path = output_dir_path

        write_table(
            output_dir_path=output_path,
            table_type=table_type,
            guid=guid,
            table=table
        )

        if "sats" not in table and table_type != "hub":
            continue

        try:
            sats = table["sats"]
        except Exception as e:
            raise Exception

        sat_path = join(output_dir_path, table["hubName"])

        if is_dir_not_path_exist(sat_path):
            os.mkdir(sat_path)

        sat_path = join(sat_path, "satellites")

        for sat in sats:
            write_table(
                output_dir_path=sat_path,
                table_type="sat",
                guid=guid,
                table=sat)

    print("Done!")


if __name__ == "__main__":
    # Add just file path
    fp = "./samples/test_bronze_visa.json"
    fp1 = "./samples/test_bancas_silver.json"
    fp2 = "./samples/test_bancas_ref.json"
    # Adjust kind of table
    kind = "dataset"
    path = "./model/bronze"
    kind1 = "hub"
    path1 = "./model/silver/hubs"
    kind2 = "ref"
    path2 = "./model/silver/references"
    # Write to files
    write_all(fp, path, kind)  # Bronze
    # write_all(fp1, path1, kind1)  # Silver
    # write_all(fp2, path2, kind2)  # Ref
