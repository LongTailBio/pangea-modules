"""HUMAnN2 is the next generation of HUMAnN (HMP Unified Metabolic Analysis Network)."""

from mongoengine import FloatField, MapField

from .constants import MODULE_NAME
from .models import Humann2Result
from .modules import Humann2ResultModule
