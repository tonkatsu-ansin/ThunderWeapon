import pytest
import ThunderWeapon
import pdb
class TestDiceBot:
    def test_valid(self):
        dicebot = ThunderWeapon.DiceBot()
        res =  dicebot.roll("2d6")
        print(res)
        assert res["total"] > 0

    def test_invalid(self):
        dicebot = ThunderWeapon.DiceBot()
        res =  dicebot.roll("ほげほげ")
        assert res is None

    def test_add(self):
        dicebot = ThunderWeapon.DiceBot()
        res =  dicebot.roll("2d6+1")
        assert res
