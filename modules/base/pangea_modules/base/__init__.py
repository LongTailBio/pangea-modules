"""Base types for PangeaModules to subclass."""

from .models import ToolResult, GroupToolResult
from .modules import SampleToolResultModule, GroupToolResultModule
from .utils import get_result_module
