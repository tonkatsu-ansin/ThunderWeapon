# coding: utf-8
import re
from random import randint
from ast import literal_eval


class DiceBotParseError(Exception):

    def __init__(self, text):
        self.text = text


class DiceBot:

    def __init__(self):
        """constructor"""

    def rollDice(self, num1, num2):
        numbers = []
        total = 0
        for x in range(num1):
            dice = randint(1, num2)
            total += dice
            numbers.append(dice)

        return {
            "n": num2,
            "d": num1,
            "total": total,
            "numbers": numbers
        }

    def roll(self, request):
        try:
            comp = re.findall("[<>]=?\d+", request)[0]
        except:
            comp = None
        formula = re.sub("[<>]=?", '', request)
        dices = re.findall("\d*[dD]\d+", formula)
        res = {}
        rolled = []

        for dice in dices:
            data = dice.split("d")
            result = self.rollDice(int(data[0]), int(data[1]))
            formula = formula.replace(dice, str(result["total"]))
            rolled.append(result)

        try:
            res["reload"] = rolled
            res["total"] = literal_eval(formula)
            if comp is not None:
                res["result"] = "成功" if literal_eval(
                    res.total + comp) else "失敗"
        except:
            return None
        return res
