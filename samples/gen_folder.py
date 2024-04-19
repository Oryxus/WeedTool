import json
from pyapacheatlas.core import AtlasEntity
from uuid import uuid4 as id
from collections import OrderedDict
import os
import sys

sys.path.append(os.path.abspath("../"))


type_name = "table_entity_def"
join = os.path.join


def convert_ordered_table(data: dict):
    fields = ["name", "description", "dataCustodian",
              "sourceSystem", "path", "fileType", "qualifiedName"]
    items = []
    for f in fields:
        if data["attributes"].__contains__(f):
            items.append((f, data["attributes"][f]))

    # item_dict = {
    #             "name": data["attributes"]["name"],
    #             "description": data["attributes"]["description"],
    #             "dataCustodian": data["attributes"]["dataCustodian"],
    #             "sourceSystem": data["attributes"]["sourceSystem"],
    #             "path": data["attributes"]["path"],
    #             "fileType": data["attributes"]["fileType"],
    #             "qualifiedName": data["attributes"]["qualifiedName"]
    #         }

    return OrderedDict([
        ("typeName", data["typeName"]),
        ("attributes", OrderedDict(list(
            items
        )))
    ])


def convert_ordered_column(data: dict):
    return OrderedDict([
        ("typeName", data["typeName"]),
        ("attributes", OrderedDict(list(
            {
                "name": data["attributes"]["name"],
                "description": data["attributes"]["description"],
                "tableName": data["attributes"]["tableName"],
                "key": data["attributes"]["key"],
                "dataType": data["attributes"]["dataType"],
                "glossaryTerm": data["attributes"]["glossaryTerm"],
                "qualifiedName": data["attributes"]["qualifiedName"]
            }.items()
        )))
    ])


def ordered_dict_serializer(obj):
    if isinstance(obj, OrderedDict):
        return dict(obj)
    return obj


def is_dir_not_path_exist(path):
    return not os.path.isfile(path) and not os.path.exists(path)


def write_entity_to(name: str, path: str, entity: AtlasEntity, typ="table"):
    if is_dir_not_path_exist(path):
        os.makedirs(path, exist_ok=True)
    out = entity.to_json()
    out.pop("guid")
    out['attributes'].pop("columnName", None)

    if typ == "table":
        out = convert_ordered_table(out)
    else:
        out = convert_ordered_column(out)

    print(path)
    full_path = join(path, name)
    with open(full_path, "w+", encoding='utf-8') as f:
        json.dump(out, f, indent=4, default=ordered_dict_serializer,
                  ensure_ascii=False)
    return out


def to_entity(guid: str,
              name: str,
              qualified: str,
              description: str,
              attrs: dict = None,
              type_name: str = type_name
              ):
    entity = AtlasEntity(
        name=name,
        qualified_name=qualified,
        description=description,
        typeName=type_name,
        attributes=attrs,
        guid=guid
    )
    return entity


def get_attr_by_kind(kind, table):
    qualifiedName = table["qualifiedName"]
    if kind == "dataset":
        attrs = {
            "path": table["path"],
            "fileType": table["fileType"],
            "sourceSystem": table["sourceSystem"],
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


def write_table(path: str, kind, guid: str, table: object):
    print(kind)
    attrs, qualifiedName = get_attr_by_kind(kind, table)

    tbl_name = table[f"{kind}Name"] if kind != "dataset" else os.path.basename(
        table[f"{kind}Name"])
    entity = to_entity(guid,
                       tbl_name,
                       #    f"{tbl_name}@{type_name}"
                       qualifiedName,
                       table['description'],
                       attrs=attrs
                       )
    if kind != "dataset":
        table_dir = join(path, tbl_name)
    else:
        tbl_name = os.path.basename(tbl_name)
        table_dir = path

    write_entity_to(f"{tbl_name}.json", table_dir, entity)

    # columns
    cols = table['columns']
    for col in cols:
        # col.pop("tableName")
        col["dataType"] = col["dataType"].lower()
        entity = to_entity(guid,
                           col["columnName"],
                        #    f"{col['columnName']}@{tbl_name}",
                           col["qualifiedName"],
                           col['description'],
                           type_name="column_entity_def",
                           attrs=col,
                           )
        column_dir = join(table_dir, "columns")
        write_entity_to(f"{col['columnName']}.json",
                        column_dir, entity, "column")


def write_all(inp: str, path: str, kind: str = 'hub'):
    with open(inp, "r", encoding='utf-8') as f:
        hubs = json.load(f)
    for hub in hubs:
        gid = id().__str__()
        print(hub)
        if kind == "dataset":
            path_ = join(path, hub["domain"], hub["datasetName"])
        else:
            path_ = path
        print(hub)
        write_table(path_, kind=kind, guid=gid, table=hub)

        if "sats" not in hub and kind != "hub":
            continue

        try:
            sats = hub["sats"]
        except Exception as e:
            raise Exception

        sat_path = join(path, hub["hubName"])
        if is_dir_not_path_exist(sat_path):
            os.mkdir(sat_path)
        sat_path = join(sat_path, "satellites")
        if is_dir_not_path_exist(sat_path):
            os.mkdir(sat_path)
        for sat in sats:
            write_table(sat_path, kind="sat", guid=gid, table=sat)


if __name__ == "__main__":
    # Add just file path
    fp = "./samples/test_bancas_silver.json"
    fp1 = "./samples/test_bancas_bronze.json"
    fp2 = "./samples/test_bancas_ref.json"
    # Adjust kind of table
    kind = "hub"
    path = "./model/silver/hubs"

    kind1 = "dataset"
    path1 = "./model/bronze"

    kind2 = "dataset"
    path2 = "./model/silver/references"    
    # Write to files
    # write_all(fp, path, kind)  # Silver
    write_all(fp1, path1, kind1)  # Bronze
    # write_all(fp2, path2, kind2)  # Ref: Delete attribute sourceSystem at table file
