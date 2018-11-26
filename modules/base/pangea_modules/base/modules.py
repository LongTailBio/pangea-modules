"""AnalysisModule classes."""

from .exceptions import UnsupportedAnalysisMode


class AnalysisModule:
    """
    Base AnalysisModule class.

    AnalysisModules take ToolResult data as input and perform additional analysis.
    """

    @staticmethod
    def name():
        """Return module's unique identifier string."""
        raise NotImplementedError()

    @classmethod
    def result_model(cls):
        """Return a model that can be used with the database engine."""
        model = cls.data_model()
        try:
            return model.get_document_class()
        except AttributeError:
            return model

    @staticmethod
    def data_model():
        """Return data model class for AnalysisModule type."""
        raise NotImplementedError()

    @staticmethod
    def required_modules():
        """List which analysis modules must be complete for this module to run."""
        return []

    @staticmethod
    def transmission_hooks():
        """Return a list of hooks to run before transmission to the client."""
        return []

    @staticmethod
    def single_sample_processor():
        """
        Return function(sample_data) for proccessing sample data.

        Where sample_data is a dictionary dump of a single Sample with appropriate ToolResults.

        It is up to the returned function to check the length of *sample_data to see if
        it was called to process a Sample or a SampleGroup and raise a UnsupportedAnalysisMode
        exception where appropriate.
        """
        raise UnsupportedAnalysisMode

    @staticmethod
    def samples_processor():
        """
        Return function(sample_data) for proccessing sample data.

        Where sample_data is one or more dictionary dumps (with appropriate ToolResults)
        of all Samples in a SampleGroup.

        It is up to the returned function to check the length of sample_data to see if
        it was called with an appropriate number of Samples and raise an EmptyGroupResult
        exception where appropriate.
        """
        raise UnsupportedAnalysisMode

    @staticmethod
    def group_tool_processor():
        """
        Return function(group_tool_result) for proccessing a AnalysisModule.

        Ex. Ancestry, Beta Diversity
        """
        raise UnsupportedAnalysisMode

    @classmethod
    def promote_data(cls, samples):
        """Return the promoted data."""
        sample_tbl = {sample['name']: sample[cls.name()] for sample in samples}
        try:
            return cls.data_model().promote(sample_tbl)
        except AttributeError:
            return sample_tbl
