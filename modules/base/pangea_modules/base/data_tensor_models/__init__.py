"""DataModels are a set of classes that construct MongoEngine Fields

for common data analysis use cases.


DataModels include a concept called 'promotion' for a group of samples.

Promotion is a way of handling groups of data that provides continuity 
to single data points. The basic concept is that every data model is eventually
composed of tensors: strings, scalars, vectors, matrices, etc. These tensors
are wrapped in fields within a model which provide organization.

While it would be possible to simply return one model per sample this would
make the inhernet organization of a model less useful since it would always
be necessary to iterate over a set of samples in downstream code. Promotion
flips this notion: rather than returning a set of models Promotion returns a
single special model. This special model has the same structure as the
original up to its last level. 

At the last level the promoted model exchanges scalars for vectors, vectors
for matrices, etc. If no exchange is possible the last level simply becomes a
set.
"""

from .models import (
    DataModel,
    MongoWrapperModel,
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
