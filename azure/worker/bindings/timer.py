import json
import typing

from azure.functions import _abc as azf_abc

from . import meta
from .. import protos


class TimerRequest(azf_abc.TimerRequest):

    def __init__(self, *, past_due: bool) -> None:
        self.__past_due = past_due

    @property
    def past_due(self):
        return self.__past_due


class TimerRequestConverter(meta.InConverter,
                            binding=meta.Binding.timerTrigger):

    @classmethod
    def check_python_type(cls, pytype: type) -> bool:
        return issubclass(pytype, azf_abc.TimerRequest)

    @classmethod
    def from_proto(cls, data: protos.TypedData,
                   trigger_metadata) -> typing.Any:
        if data.WhichOneof('data') != 'json':
            raise NotImplementedError

        info = json.loads(data.json)
        return TimerRequest(
            past_due=info.get('IsPastDue', False))