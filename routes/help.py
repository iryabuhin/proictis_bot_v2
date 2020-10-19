from typing import Union, Optional, Dict
from vkbottle import keyboard_gen
from vkbottle.bot import Blueprint, Message
from vkbottle.branch import ClsBranch, rule_disposal
from vkbottle.rule import PayloadRule, CommandRule, VBMLRule
from aiocache import caches
from keyboards import MAIN_MENU_KEYBOARD, SCHEDULE_KEYBOARD, EMPTY_KEYBOARD
from typing import List, Tuple, Dict, AnyStr, Union
from rules import PayloadHasKey, ExitButtonPressed
from utils import fetch_json, return_to_main_menu
from models import DBStoredBranch, UserState
from config import Config
import ujson
import aiohttp


bp = Blueprint(name='help')
bp.branch = DBStoredBranch()

