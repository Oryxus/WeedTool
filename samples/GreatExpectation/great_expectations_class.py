import great_expectations as ge
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.exceptions import DataContextError
from typing import Any


class GreatExpectations():
    def __init__(self, context_root_dir: str, expectation_suite_name: str) -> None:
        """
        Args:
            context_root_dir (str): path to table want to create expectation suite
            expectation_suite_name (str): file name of expectation suite
        """
        self.project_root_dir = context_root_dir
        self.expectation_suite_name = expectation_suite_name
        self.context = ge.get_context(context_root_dir=self.project_root_dir)
        self.suite = None

    def get_or_create_suite(self):
        """
        Get or create expectation suite if it's existing

        Returns:
            _type_: ExpectationSuite
        """
        try:
            # If table have an existing expectation suite - get this expectation suite to update
            self.suite = self.context.get_expectation_suite(
                self.expectation_suite_name)
        except DataContextError:
            # If not, add new expectation suite to the table
            self.suite = self.context.add_expectation_suite(
                self.expectation_suite_name)
        return self.suite

    def add_expectation_suite_(self, expectation_type: str, kwargs: dict, meta: dict) -> Any:
        """
        Add an expectation type to the expectation suite

        Args:
            expectation_type (str): The type of expectation 
            kwargs (dict): The keyword arguments for the expectation
            meta (dict): The meta information for the expectation.

        Returns:
            Any
        """
        self.suite = self.get_or_create_suite()
        expectation = ExpectationConfiguration(
            expectation_type=expectation_type,
            kwargs=kwargs,
            meta=meta,
        )

        updated_suite = self.suite.add_expectation(
            expectation_configuration=expectation)
        return updated_suite

    def save_expectation_suite(self) -> None:
        """
        Save the provided ExpectationSuite into the DataContext using the configured ExpectationStore

        Returns:
            None
        """
        return self.context.save_expectation_suite(expectation_suite=self.suite)
