from constant import *
import sys
sys.path.append(BASE_PATH)
from src.metadata_tool.core.platform.common.configs import BRONZE, SILVER
from src.metadata_tool.services.metadata_lookup.dictionary import DictionaryService
from samples.GreatExpectation.auto_expectations import AutoExpectations
# from samples.GreatExpectation.specific_tables_metadata import TablesMetadata
from samples.GreatExpectation.update_sub_tables_metadata import update_tables_metadata
from src.metadata_tool.core.platform.filesystem import EntityFileSystem
from samples.GreatExpectation.tables_metadata import TablesMetadata


def write_expectation(tables_metadata_path: str) -> None:
    """Writing expectaiton suite for each tables in a specific tier (BRONZE, SILVER or GOLD) 

    Args:
        tables_metadata_path (str): path to json file including tables metadata of a specific tier

    Returns:
        None
    """
    ax = AutoExpectations(tables_metadata_path)
    # Add expectation that table columns match an order set
    ax.expect_table_columns_match_set()

    # Add expectation that columns value to be not null
    ax.expect_colum_value_not_null()

    # Add expectation that compound columns to be unique
    ax.expect_compound_columns_unique()


if __name__ == "__main__":
    # set up DictionaryService for BRONZE, SILVER tier
    bronze_dict_service = DictionaryService(BASE_PATH, BRONZE)
    # silver_dict_service = DictionaryService(BASE_PATH, SILVER)
    entity_filesys = EntityFileSystem(BASE_PATH, BRONZE)    
    # specific tables want to create expectation suite


    # Initial TablesMetadata object to get tables metadata from BRONZE, SILVER
    bronze_tables_metadata = TablesMetadata(
        bronze_dict_service, entity_filesys, BRONZE)

    # silver_tables_metadata = TablesMetadata(
    #     silver_dict_service, SILVER)

    # Get table metadata from BRONZE, SILVER
    bronze_tables_metadata.convert_to_json(BRONZE_TABLES_METADATA)
    # silver_tables_metadata.convert_to_json(SILVER_TABLES_METADATA)

    # update metadata of BRONZE & SILVER
    update_tables_metadata(BRONZE_TABLES_METADATA)
    # update_tables_metadata(SILVER_TABLES_METADATA)

    # Write expectationsuite for each tables in BRONZE & SILVER
    write_expectation(BRONZE_TABLES_METADATA)
    # write_expectation(SILVER_TABLES_METADATA)

