#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试文件：使用pytest测试BaziCalculator类的日期转换静态方法和实例方法
- solar_to_lunar: 阳历转农历（静态方法）
- lunar_to_solar: 农历转阳历（静态方法）
- calculate_bazi_from_lunar: 农历日期计算八字（实例方法）
"""

import pytest
from server.bazi_calculator import BaziCalculator
from server.bazi_calculator import (
    YEAR, MONTH, DAY, HOUR, STEM, BRANCH, HIDDEN_STEM,
    FIVE_ELEMENTS, TEN_GODS, DECADE_PILLAR
)


class TestBaziCalculator:
    """测试BaziCalculator类的日期转换功能"""

    def test_solar_to_lunar(self):
        """测试阳历转农历功能"""
        # 测试用例1：普通阳历日期转换
        result1 = BaziCalculator.solar_to_lunar(2023, 1, 22)
        assert result1["year"] == 2023
        assert result1["month"] == 1
        assert result1["day"] == 1
        assert result1["is_leap_month"] == False

        # 测试用例2：农历春节当天
        result2 = BaziCalculator.solar_to_lunar(2023, 1, 23)
        assert result2["year"] == 2023
        assert result2["month"] == 1
        assert result2["day"] == 2
        assert result2["is_leap_month"] == False

        # 测试用例3：闰月情况
        # 2020年闰四月
        result3 = BaziCalculator.solar_to_lunar(2020, 6, 1)
        assert result3["year"] == 2020
        assert result3["month"] == 4
        assert result3["is_leap_month"] == True

    def test_lunar_to_solar(self):
        """测试农历转阳历功能"""
        # 测试用例1：普通农历日期转换
        result1 = BaziCalculator.lunar_to_solar(2023, 1, 1, False)
        assert result1["year"] == 2023
        assert result1["month"] == 1
        assert result1["day"] == 22

        # 测试用例2：农历闰月测试
        # 2020年闰四月初一
        result2 = BaziCalculator.lunar_to_solar(2020, 4, 1, True)
        assert result2["year"] == 2020
        assert result2["month"] == 5
        assert result2["day"] == 23

        # 测试用例3：农历大月小月测试
        # 2022年农历十二月三十（大月）
        result3 = BaziCalculator.lunar_to_solar(2022, 12, 30, False)
        assert result3["year"] == 2023
        assert result3["month"] == 1
        assert result3["day"] == 21

    def test_bidirectional_conversion(self):
        """测试双向转换的一致性"""
        # 选择几个特殊日期进行双向测试
        test_dates = [
            (2023, 1, 1),    # 元旦
            (2023, 5, 1),    # 劳动节
            (2022, 1, 31),   # 2022年春节前一天
            (2022, 2, 1),    # 2022年春节
            (2020, 5, 23),   # 2020年闰四月初一
            (2020, 6, 21)    # 2020年闰四月三十
        ]
        
        for year, month, day in test_dates:
            # 阳历 -> 农历 -> 阳历，应该回到原始日期
            lunar = BaziCalculator.solar_to_lunar(year, month, day)
            solar = BaziCalculator.lunar_to_solar(
                lunar["year"], 
                lunar["month"], 
                lunar["day"], 
                lunar["is_leap_month"]
            )
            
            assert solar["year"] == year
            assert solar["month"] == month
            assert solar["day"] == day

    def test_calculate_bazi(self):
        """测试八字计算功能"""
        # 创建BaziCalculator实例
        calculator = BaziCalculator()
        
        # 测试用例1：农历日期计算八字
        result1 = calculator.calculate_bazi_from_lunar(
            lunar_year=1992, 
            lunar_month=7, 
            lunar_day=27, 
            hour=8, 
            minute=0, 
            is_leap_month=False, 
            gender='男'
        )
        calculator.print_bazi_result(result1)


        # 验证基本结构是否存在
        assert YEAR in result1
        assert MONTH in result1
        assert DAY in result1
        assert HOUR in result1
        assert FIVE_ELEMENTS in result1
        assert TEN_GODS in result1
        assert DECADE_PILLAR in result1


if __name__ == "__main__":
    pytest.main(["-v", __file__]) 