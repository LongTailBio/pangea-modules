"""DataModels are a set of classes that construct MongoEngine Fields

for common data analysis use cases.
"""

from .model import (
    DataModel,
    FixedGroupModel,
    UnlimitedGroupModel,
)
from .tensor_0 import (
    ScalarModel,
    CategoricalModel,
    Tensor0Model,
)
from .tensor_1 import (
    Tensor1Model,
    VectorModel,
)
from .tensor_2 import (
    Tensor2Model,
    MatrixModel,
)
