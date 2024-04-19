from great_expectations_class import GreatExpectations
import json
from constant import *
from config import *
import copy


class AutoExpectations:
    """
    Object including expectation type for tables, columns
    """

    def __init__(self, path: str) -> None:
        """
        Parameters: 
            - path(str): path to the json file including tables metadata
        """
        self.path = path
        with open(self.path, READ) as file:
            self.tables_metadata = json.load(file)

    def expect_table_columns_match_set(self) -> None:
        """
        Add expectation type expecting the columns to match an unordered set.

        Returns:
            None
        """
        for item in self.tables_metadata:
            # get expectation suite name, columns list, path of table to create expectation type
            expectation_suite_name = item.get(EXPECTATION_SUITE)
            columns_set = item.get(COLUMNS)
            context_root_dir = item.get(PATH)

            # set up GreatExpectation:
            gx = GreatExpectations(context_root_dir, expectation_suite_name)

            # setup "kwargs" value
            KWARGS_COlUMNS_MATCH_SET[COLUMN_SET] = columns_set
            kwargs = KWARGS_COlUMNS_MATCH_SET

            # setup "meta" value
            meta = copy.deepcopy(META_COLUMNS_MATCH_SET)
            meta[NOTES][CONTENT] = meta[NOTES][CONTENT].format(columns_set)

            gx.add_expectation_suite_(
                expectation_type=EXPECT_COLUMN_MATCH_SET,
                kwargs=kwargs,
                meta=meta
            )

            gx.save_expectation_suite()

    def expect_colum_value_not_null(self) -> None:
        """
        Add the expectation type expecting the column values to not be null.

        Returns:
            None
        """
        for item in self.tables_metadata:
            expectation_suite_name = item.get(EXPECTATION_SUITE)
            columns_set = item.get(COLUMNS)
            context_root_dir = item.get(PATH)
            gx = GreatExpectations(context_root_dir, expectation_suite_name)

            for column in columns_set:
                # setup "kwargs" value
                kwargs = KWARGS_COLUMN_NOT_NULL.copy()
                kwargs[COLUMN] = kwargs[COLUMN].format(column)

                # setup "meta" value
                meta = copy.deepcopy(META_COLUMN_NOT_NULL)
                meta[NOTES][CONTENT] = meta[NOTES][CONTENT].format(column)

                gx.add_expectation_suite_(
                    expectation_type=EXPECT_COLUMN_NOT_NULL,
                    kwargs=kwargs,
                    meta=meta
                )

                gx.save_expectation_suite()

    def expect_compound_columns_unique(self) -> None:
        """
        Add expectation type expecting the compound columns to be unique.

        Returns:
            None
        """
        for item in self.tables_metadata:
            # get expectation suite name, key columns, path of table to create expectation
            expectation_suite_name = item.get(EXPECTATION_SUITE)
            keys_list = item.get(KEYS)
            context_root_dir = item.get(PATH)

            # set up GreatExpectation:
            gx = GreatExpectations(context_root_dir, expectation_suite_name)

            # setup "kwargs" value
            KWARGS_COMPOUND_UNIQUE[COLUMN_LIST] = keys_list
            kwargs = KWARGS_COMPOUND_UNIQUE

            # setup "meta" value
            meta = copy.deepcopy(META_COMPOUND_UNIQUE)
            meta[NOTES][CONTENT] = meta[NOTES][CONTENT].format(keys_list)

            gx.add_expectation_suite_(
                expectation_type=EXPECT_COMPOUND_UNIQUE,
                kwargs=kwargs,
                meta=meta
            )

            gx.save_expectation_suite()
