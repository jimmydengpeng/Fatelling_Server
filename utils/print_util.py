from server.terminology import *

def print_bazi_result(bazi):
    # 打印结果的美化显示
    print("\n" + "="*60)
    print(f"{'八字计算结果':^50}")
    print("="*60)
    
    # 输入信息
    lunar_year_val = 1992
    lunar_month_val = 7
    lunar_day_val = 27
    hour_val = 8
    gender_val = '男'
    print(f"输入信息: 农历 {lunar_year_val}年{lunar_month_val}月{lunar_day_val}日 {hour_val}时 性别：{gender_val}")
    
    # 四柱
    print("\n四柱:")
    print(f"  年柱: {bazi[YEAR][STEM]}{bazi[YEAR][BRANCH]} 藏干: {','.join(bazi[YEAR][HIDDEN_STEM])}")
    print(f"  月柱: {bazi[MONTH][STEM]}{bazi[MONTH][BRANCH]} 藏干: {','.join(bazi[MONTH][HIDDEN_STEM])}")
    print(f"  日柱: {bazi[DAY][STEM]}{bazi[DAY][BRANCH]} 藏干: {','.join(bazi[DAY][HIDDEN_STEM])}")
    print(f"  时柱: {bazi[HOUR][STEM]}{bazi[HOUR][BRANCH]} 藏干: {','.join(bazi[HOUR][HIDDEN_STEM])}")
    
    # 五行
    print(f"\n五行: {','.join(bazi[FIVE_ELEMENTS])}")
    
    # 十神
    print("\n十神:")
    for pillar in [YEAR, MONTH, DAY, HOUR]:
        pillar_name = {"year": "年", "month": "月", "day": "日", "hour": "时"}[pillar]
        try:
            ten_god = bazi[TEN_GODS][pillar][TEN_GODS]
            branch_god = bazi[TEN_GODS][pillar][BRANCH]
            hidden_gods = bazi[TEN_GODS][pillar][HIDDEN_STEM]
            print(f"  {pillar_name}柱: 天干({ten_god}) 地支({branch_god}) 藏干({','.join(hidden_gods)})")
        except:
            print(f"  {pillar_name}柱: 信息不完整")
    
    # 大运信息
    print("\n大运信息:")
    print(f"  起运日期: {bazi[DECADE_PILLAR]['qiyun_date_solar']['year']}年{bazi[DECADE_PILLAR]['qiyun_date_solar']['month']}月{bazi[DECADE_PILLAR]['qiyun_date_solar']['day']}日")
    print(f"  起运年龄: {bazi[DECADE_PILLAR]['start_age']['years']}岁{bazi[DECADE_PILLAR]['start_age']['months']}个月")
    print(f"  顺逆: {'顺行' if bazi[DECADE_PILLAR]['is_forward'] else '逆行'}")
    print(f"  节气: {bazi[DECADE_PILLAR]['jieqi_name']}")
    print("  大运列表:")
    for cycle in bazi[DECADE_PILLAR]['cycles'][:5]:  # 显示前5个大运
        print(f"    {cycle['tian_gan']}{cycle['di_zhi']} ({cycle['year']}年起) 藏干: {','.join(cycle['cang_gan'])}")
    
    print("="*60)