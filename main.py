import ThunderWeapon
import pytest
if __name__ == '__main__':
    a = ThunderWeapon.DiceBot("2d6<12")
    print(a.run())
