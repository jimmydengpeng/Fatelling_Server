#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
独立脚本：输入农历或阳历日期，打印八字计算结果
"""

import os
import sys

# 将父目录添加到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.bazi_calculator import BaziCalculator
from server.bazi_calculator import (
    YEAR, MONTH, DAY, HOUR, STEM, BRANCH, HIDDEN_STEM,
    FIVE_ELEMENTS, TEN_GODS, DECADE_PILLAR
)


def print_bazi_report(lunar_year, lunar_month, lunar_day, hour, minute, is_leap_month, gender):
    """打印八字报告"""
    calculator = BaziCalculator()
    result = calculator.calculate_bazi_from_lunar(
        lunar_year=lunar_year,
        lunar_month=lunar_month,
        lunar_day=lunar_day,
        hour=hour,
        minute=minute,
        is_leap_month=is_leap_month,
        gender=gender
    )
    
    # 打印结果的美化显示
    print("\n" + "="*60)
    print(f"{'八字计算结果':^50}")
    print("="*60)
    
    # 输入信息
    print(f"输入信息: 农历 {lunar_year}年{lunar_month}月{lunar_day}日 {hour}时 性别：{gender}")
    
    # 四柱
    print("\n四柱:")
    print(f"  年柱: {result[YEAR][STEM]}{result[YEAR][BRANCH]} 藏干: {','.join(result[YEAR][HIDDEN_STEM])}")
    print(f"  月柱: {result[MONTH][STEM]}{result[MONTH][BRANCH]} 藏干: {','.join(result[MONTH][HIDDEN_STEM])}")
    print(f"  日柱: {result[DAY][STEM]}{result[DAY][BRANCH]} 藏干: {','.join(result[DAY][HIDDEN_STEM])}")
    print(f"  时柱: {result[HOUR][STEM]}{result[HOUR][BRANCH]} 藏干: {','.join(result[HOUR][HIDDEN_STEM])}")
    
    # 五行
    print(f"\n五行: {','.join(result[FIVE_ELEMENTS])}")
    
    # 十神
    print("\n十神:")
    for pillar in [YEAR, MONTH, DAY, HOUR]:
        pillar_name = {"year": "年", "month": "月", "day": "日", "hour": "时"}[pillar]
        try:
            ten_god = result[TEN_GODS][pillar][TEN_GODS]
            branch_god = result[TEN_GODS][pillar][BRANCH]
            hidden_gods = result[TEN_GODS][pillar][HIDDEN_STEM]
            print(f"  {pillar_name}柱: 天干({ten_god}) 地支({branch_god}) 藏干({','.join(hidden_gods)})")
        except:
            print(f"  {pillar_name}柱: 信息不完整")
    
    # 大运信息
    print("\n大运信息:")
    print(f"  起运日期: {result[DECADE_PILLAR]['qiyun_date_solar']['year']}年{result[DECADE_PILLAR]['qiyun_date_solar']['month']}月{result[DECADE_PILLAR]['qiyun_date_solar']['day']}日")
    print(f"  起运年龄: {result[DECADE_PILLAR]['start_age']['years']}岁{result[DECADE_PILLAR]['start_age']['months']}个月")
    print(f"  顺逆: {'顺行' if result[DECADE_PILLAR]['is_forward'] else '逆行'}")
    print(f"  节气: {result[DECADE_PILLAR]['jieqi_name']}")
    print("  大运列表:")
    for cycle in result[DECADE_PILLAR]['cycles'][:8]:  # 显示8个大运
        print(f"    {cycle['tian_gan']}{cycle['di_zhi']} ({cycle['year']}年起) 藏干: {','.join(cycle['cang_gan'])}")
    
    print("="*60)
    
    return result


def main():
    # 示例1：农历日期
    lunar_year = 1992
    lunar_month = 7
    lunar_day = 27
    hour = 8
    is_leap_month = False
    gender = "男"
    
    print_bazi_report(lunar_year, lunar_month, lunar_day, hour, 0, is_leap_month, gender)
    
    # 示例2：从阳历转农历后计算
    solar_year = 1992
    solar_month = 8
    solar_day = 25
    
    lunar_date = BaziCalculator.solar_to_lunar(solar_year, solar_month, solar_day)
    print(f"\n阳历 {solar_year}年{solar_month}月{solar_day}日 转换为农历: {lunar_date['year']}年{lunar_date['month']}月{lunar_date['day']}日")
    
    print_bazi_report(
        lunar_date['year'], 
        lunar_date['month'], 
        lunar_date['day'], 
        hour, 0, 
        lunar_date['is_leap_month'], 
        "女"
    )


if __name__ == "__main__":
    main() 