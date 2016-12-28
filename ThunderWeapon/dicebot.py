# coding: utf-8
import re
import random
from functools import reduce
__DEFAULT__ = 6
class PatternNotFound(Exception):
    """ダイスボットの書式がおかしかった場合のエラiー"""
    def __init__(self, text):
        """ダイスボットがダメ"""
        self.text = text


class Dice:
    def __init__(self,text):
        self.text = text

    def d(self):
        nums = [int(x) for x in self.text.split("d")]
        if len(nums) == 0:
            nums.append(__DEFAULT__)
        return reduce(lambda a,b: a+b, [random.randint(1, nums[1]) for x in range(nums[0])])

    def b(self):
        nums = [int(x) for x in self.text.split("b")]
        if len(nums) == 0:
            nums.append(__DEFAULT__)
        result = []
        for i in range(nums[0]):
            result.append(random.randint(1, nums[1]))
        return result

    def run(self):
        if self.text.find('d') > -1:
            return self.d()
        elif self.text.find('b') > -1:
            return self.b()

class DiceBot:
    def __init__(self, text):
        self.text = text

    def is_valid(self):
       """
       弾くパターン

       - >,>=,=>,<,<=,=<,=が複数以上出てきたとき

       - ダイス表記のとき後ろの数字が101を超えたとき

       - 試行回数(前の数字が)500を超えたとき

       """
       return True

    def run(self):
        pattern = r"[1-9][0-9]*d[1-9][0-9]*"
        findedall = re.findall(pattern, self.text)
        if findedall is None:
            raise PatternNotFound(self.text)
        splited = re.split(pattern, self.text)
        print(findedall)
        print(splited)
        for i,j in enumerate(splited):
            if len(j) == 0:
                dice = Dice(findedall.pop(0))
                splited[i] = dice.run()
        return splited

