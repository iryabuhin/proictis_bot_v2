from vkbottle import Message
from vkbottle.rule import AbstractMessageRule, PayloadRule
from typing import Union, List, Dict, AnyStr, Tuple
import json

class PayloadContainsFieldRule(AbstractMessageRule):
    def __init__(self, fields=Union[str, List[str]], mode=1):
        self.mode = mode
        if isinstance(fields, str):
            self.fields = [fields]
        else:
            self.fields = fields

    @staticmethod
    def dispatch(payload: str) -> dict:
        try:
            return json.loads(payload)
        except json.decoder.JSONDecodeError:
            return dict()

    async def check(self, message: Message) -> bool:
        if message.payload is not None:
            payload = self.dispatch(message.payload)
            if self.mode == 1:
                for field in self.fields:
                    if payload.get(field) is None:
                        return False
                return True


class ExitButtonPressed(PayloadRule):
    def __init__(self, mode=1):
        self.exit_cmd_payload = {'command': 'exit'}
        self.mode = mode

    async def check(self, message: Message) -> bool:
        if message.payload is not None:
            payload = self.dispatch(message.payload)
            if self.mode == 1:
                # EQUALITY
                if payload == self.exit_cmd_payload:
                    return True
            elif self.mode == 2:
                # CONTAIN
                if {**payload, **self.exit_cmd_payload} == payload:
                    return True
