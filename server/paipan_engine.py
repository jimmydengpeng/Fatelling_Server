from datetime import datetime, timedelta
import sxtwl  # 使用寿星天文历库计算农历和八字
from typing import Dict, Tuple, List
import copy

YEAR          = "year"
MONTH         = "month"
DAY           = "day"
HOUR          = "hour"
STEM          = "tian_gan"
BRANCH        = "di_zhi"
STEM_BRANCH   = "tian_gan_di_zhi"
HIDDEN_STEM   = "cang_gan"
FIVE_ELEMENTS = "wu_xing"
TEN_GODS      = "shi_shen"
DECADE_PILLAR = "da_yun"

NUM_DECADE_PILLAR = 8


class BaziPaipanEngine:
    """八字排盘引擎"""

    # 天干
    TIAN_GAN_NAMES = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

    # 地支
    DI_ZHI_NAMES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    # 六十甲子
    SEXAGENARY_CYCLE = [
        "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
        "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
        "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
        "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
        "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
        "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
    ]
    
    # 节气名称
    JIE_QI_NAMES = [
        "冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", 
        "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"
    ]
    
    # 五行
    TIAN_GAN_2_WU_XING = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }

    # 五行生克关系
    FIVE_ELEMENTS_RELATIONS = {
        "木": {"木": "比劫", "火": "食伤", "土": "财才", "金": "官杀", "水": "印枭"},
        "火": {"木": "印枭", "火": "比劫", "土": "食伤", "金": "财才", "水": "官杀"},
        "土": {"木": "官杀", "火": "食伤", "土": "比劫", "金": "财才", "水": "印枭"},
        "金": {"木": "财才", "火": "官杀", "土": "食伤", "金": "比劫", "水": "印枭"},
        "水": {"木": "印枭", "火": "官杀", "土": "食伤", "金": "财才", "水": "比劫"}
    }

    # 阴阳
    TIAN_GAN_YIN_YANG = {
        "甲": "阳", "乙": "阴", "丙": "阳", "丁": "阴", "戊": "阳",
        "己": "阴", "庚": "阳", "辛": "阴", "壬": "阳", "癸": "阴"
    }

    # 十神名称
    TEN_GODS = {
        ("同", "比劫"): "比肩",
        ("异", "比劫"): "劫财",
        ("同", "印枭"): "偏印",
        ("异", "印枭"): "正印",
        ("同", "官杀"): "七杀",
        ("异", "官杀"): "正官",
        ("同", "财才"): "偏财",
        ("异", "财才"): "正财",
        ("同", "食伤"): "食神",
        ("异", "食伤"): "伤官"
    }

    # 地支藏干对应表
    BRANCH_HIDDEN_STEM = {
        "子": ["癸"],
        "丑": ["己", "辛", "癸"],
        "寅": ["甲", "丙", "戊"],
        "卯": ["乙"],
        "辰": ["戊", "乙", "癸"],
        "巳": ["丙", "庚", "戊"],
        "午": ["丁", "己"],
        "未": ["己", "丁", "乙"],
        "申": ["庚", "壬", "戊"],
        "酉": ["辛"],
        "戌": ["戊", "辛", "丁"],
        "亥": ["壬", "甲"]
    }

    def __init__(self):
        pass

    ## API ##
    def solar_to_lunar(self, year: int, month: int, day: int) -> Dict:
        """将阳历转换为农历"""
        solar_date = sxtwl.fromSolar(year, month, day)
        return {
            "year": solar_date.getLunarYear(),
            "month": solar_date.getLunarMonth(),
            "day": solar_date.getLunarDay(),
            "is_leap_month": solar_date.isLunarLeap()
        }

    ## API ##
    def lunar_to_solar(self, year: int, month: int, day: int, is_leap_month: bool = False) -> Dict:
        """将农历转换为阳历"""
        lunar_date = sxtwl.fromLunar(year, month, day, is_leap_month)
        return {
            "year": lunar_date.getSolarYear(),
            "month": lunar_date.getSolarMonth(),
            "day": lunar_date.getSolarDay()
        }
    
    # TODO: 矫正真太阳时
    # TODO: 区分早晚子时
    ## API ##
    def calculate_bazi(
        self,
        lunar_year: int,
        lunar_month: int,
        lunar_day: int,
        hour: int,
        minute: int,
        is_leap_month: bool,
        gender: str  # "男" or "女"
    ) -> Dict:
        """
        计算八字
        Args:
            lunar_year: 农历年
            lunar_month: 农历月
            lunar_day: 农历日
            hour: 小时（24小时制）
            minute: 分钟
            is_leap_month: 是否闰月
            gender: 性别
        Returns:
            包含八字信息的字典
        """
        # 获取农历日期
        day = sxtwl.fromLunar(lunar_year, lunar_month, lunar_day, is_leap_month)
        
        # 计算年月日时的天干地支
        year_gz  = day.getYearGZ()
        month_gz = day.getMonthGZ()
        day_gz   = day.getDayGZ()
        hour_gz  = self._get_hour_gz(day_gz.tg, hour)
        
        # 获取日干（命主）
        day_stem = self.TIAN_GAN_NAMES[day_gz.tg]
        
        # 组装八字
        bazi = {
            YEAR  : self._create_pillar_info(year_gz.tg, year_gz.dz),
            MONTH : self._create_pillar_info(month_gz.tg, month_gz.dz),
            DAY   : self._create_pillar_info(day_gz.tg, day_gz.dz),
            HOUR  : self._create_pillar_info(hour_gz[0], hour_gz[1])
        }
        
        # 计算五行属性
        bazi[FIVE_ELEMENTS] = self._calculate_five_elements(bazi)
        
        # 计算十神
        bazi[TEN_GODS] = self._calculate_ten_gods(bazi, day_stem)

        # 计算大运
        dayun_info = self._calculate_dayun(day, hour, minute, gender)
        bazi[DECADE_PILLAR] = dayun_info
        
        return bazi

    def _create_pillar_info(self, stem_index: int, branch_index: int) -> Dict:
        """创建柱信息"""
        return {
            STEM       : self.TIAN_GAN_NAMES[stem_index],
            BRANCH     : self.DI_ZHI_NAMES[branch_index],
            HIDDEN_STEM: self.BRANCH_HIDDEN_STEM.get(self.DI_ZHI_NAMES[branch_index], [])
        }
    
    def _calculate_ten_gods(self, bazi: Dict, day_stem: str) -> Dict[str, Dict[str, str]]:
        """
        根据八字干支信息计算日主以外的十神: 计算日干和其他天干、地支藏干的五行生克关系，以及阴阳异同判断十神
        Args:
            bazi: 八字信息字典
            day_stem: 日干
        Returns:
            十神信息字典
        """
        result = {}
        
        for pillar in [YEAR, MONTH, DAY, HOUR]:
            result[pillar] = {}
            
            # 计算天干十神
            stem = bazi[pillar][STEM]
            result[pillar][TEN_GODS] = self._calculate_stem_ten_god(stem, day_stem)
            
            # 计算地支藏干的十神
            branch = bazi[pillar][BRANCH]
            result[pillar][BRANCH] = self._get_branch_ten_god(branch, day_stem)
            
            # 计算地支藏干的十神
            hidden_stems = bazi[pillar][HIDDEN_STEM]
            result[pillar][HIDDEN_STEM] = [
                self._calculate_stem_ten_god(hidden_stem, day_stem)
                for hidden_stem in hidden_stems
            ]
        return result
    
    def _calculate_stem_ten_god(self, stem: str, day_stem: str) -> str:
        """
        计算天干的十神
        Args: 
            stem: 要计算的天干
            day_stem: 日干
        Returns:
            要计算的天干相对于日主天干的十神名称
        """
        stem_element  = self.TIAN_GAN_2_WU_XING[stem]
        day_element   = self.TIAN_GAN_2_WU_XING[day_stem]
        relation      = self.FIVE_ELEMENTS_RELATIONS[day_element][stem_element]
        stem_yin_yang = self.TIAN_GAN_YIN_YANG[stem]
        day_yin_yang  = self.TIAN_GAN_YIN_YANG[day_stem]
        
        return self.TEN_GODS[(
            "同" if stem_yin_yang == day_yin_yang else "异",
            relation
        )]
    
    def _get_branch_ten_god(self, branch: str, day_stem: str) -> str:
        """
        获取地支藏干的十神（简化处理，只返回地支本气的十神）
        Args:
            branch: 地支
            day_stem: 日干
        Returns:
            十神名称
        """
        if branch not in self.BRANCH_HIDDEN_STEM:
            return ""

        # 获取地支的本气（第一个藏干）
        hidden_stem = self.BRANCH_HIDDEN_STEM[branch][0]
        return self._calculate_stem_ten_god(hidden_stem, day_stem)
    
    def _get_hour_gz(self, day_stem: int, hour: int) -> Tuple[int, int]:
        """
        计算时柱天干地支
        Args:
            day_stem: 日柱天干
            hour: 小时
        Returns:
            时柱天干地支的索引元组
        """
        # 将24小时制转换为12地支时辰
        branch_index = (hour + 1) // 2 % 12
        
        # 根据日干推算时干
        stem_index = ((day_stem % 10) * 2 + branch_index) % 10
        
        return (stem_index, branch_index)
    
    # TODO: 计算天干、地支（藏干）的五行数量
    def _calculate_five_elements(self, bazi: Dict) -> List[str]:
        """
        计算八字中的五行属性
        Args:
            bazi: 八字信息字典
        Returns:
            五行属性列表
        """
        five_elements = []
        for pillar in [YEAR, MONTH, DAY, HOUR]:
            stem = bazi[pillar][STEM]
            five_elements.append(self.TIAN_GAN_2_WU_XING[stem])
        return five_elements

    def get_bazi_string(self, bazi: Dict) -> str:
        """
        将八字转换为字符串格式，包括天干、地支和藏干信息，以及起运日期信息
        Args:
            bazi: 八字信息字典
        Returns:
            格式化的八字字符串，包括天干、地支和藏干信息，以及起运日期信息，e.g., "甲子（丙寅） 乙丑（戊辰） 丙寅（庚午） 丁卯（辛未）"，起运日期：1992年7月27日
        """
        result = []
        for pillar in [YEAR, MONTH, DAY, HOUR]:
            stem = bazi[pillar][STEM]
            branch = bazi[pillar][BRANCH]
            hidden_stems = bazi[pillar][HIDDEN_STEM]
            hidden_stem_str = "（" + " ".join(hidden_stems) + "）"
            result.append(f"{stem}{branch}{hidden_stem_str}")
        qiyun_date_solar = bazi[DECADE_PILLAR]['qiyun_date_solar']
        qiyun_date_lunar = bazi[DECADE_PILLAR]['qiyun_date_lunar']
        result.append(f"起运日期：{qiyun_date_solar['year']}年{qiyun_date_solar['month']}月{qiyun_date_solar['day']}日（农历：{qiyun_date_lunar['year']}年{'闰' if qiyun_date_lunar['is_leap_month'] else ''}{qiyun_date_lunar['month']}月{qiyun_date_lunar['day']}日）")
        return " ".join(result)

    
    # <大运计算>
    def _calculate_dayun(self, birth_day: sxtwl.Day, hour: int, minute: int, gender: str) -> Dict:
        """
        计算大运

        八字大运计算规则
            1. 顺逆:
                男命阳年/女命阴年 -> 顺行（从出生日顺推至下一节气）
                男命阴年/女命阳男 -> 逆行（从出生日逆推至上一节气）

            2. 起运时间：
                - 顺行者从出生日顺推至下一节气
                - 逆行者从出生日逆推至上一节气
                
                得到的相隔天数除以3，得数即为命主起大运的岁数，余数1天代表4个月，1个时辰代表10天即：
                - 3天 = 1年
                - 1天 = 4个月
                - 1时辰 = 10天

                
            3. 大运干支排列：
               然后以命主月柱开始，依据顺逆排列大运干支
                - 顺行：按六十甲子顺序从月柱推导（例：月柱为甲子，大运为乙丑->丙寅->丁卯，以此类推）
                - 逆行：按六十甲子逆序从月柱推导（例：月柱为甲子，大运为癸亥->壬戌->辛酉，以此类推）
                
            4. 大运年份:
                - 将所得起运时间加到命主的阳历出生日期上，得出的年份即为命主的第一年大运年份
                - 然后依据"十年一大运"的规则，以第一年大运年份为基础依次加10年，即可得到每一个大运的年份

        Args:
            lunar_date: 农历日期信息字典，包含year, month, day, hour, is_leap_month
            gender: 性别，"男"或"女"
        Returns:
            大运信息字典
        """
        # 获取年干和月柱
        year_gz = birth_day.getYearGZ()
        month_gz = birth_day.getMonthGZ()
        
        # 判断年干阴阳
        is_yang_year = self.TIAN_GAN_YIN_YANG[self.TIAN_GAN_NAMES[year_gz.tg]] == "阳"
        
        # 判断大运顺逆
        is_forward = (gender == "男" and is_yang_year) or \
                     (gender == "女" and not is_yang_year)
        
        # 获取距离某日最近的下/上一个节气时间
        jieqi_idx, jieqi_time = self._get_nearest_jieqi_time(birth_day, is_forward)

        # 计算起运时间
        dayun_start_info = self._calculate_dayun_start_age(
            (birth_day.getSolarYear(), birth_day.getSolarMonth(), birth_day.getSolarDay(), hour, minute),
            (jieqi_time[0], jieqi_time[1], jieqi_time[2], jieqi_time[3], jieqi_time[4])
        )
        start_age = dayun_start_info["start_age"] # 起运岁数：出生后几年几月几天起运
        qiyun_date_solar = dayun_start_info["qiyun_date_solar"] # 起运具体日期：起运时间是哪年哪月哪日
        
        # 计算大运干支和年份
        destiny_cycles = []
        # 获取月柱干支在六十甲子中的索引
        current_gz_index = self.SEXAGENARY_CYCLE.index(
            f"{self.TIAN_GAN_NAMES[month_gz.tg]}{self.DI_ZHI_NAMES[month_gz.dz]}"
        )
        
        # 计算大运干支
        first_cycle_year = qiyun_date_solar["year"]
        for i in range(NUM_DECADE_PILLAR):
            if is_forward:
                current_gz_index = (current_gz_index + 1) % 60
            else:
                current_gz_index = (current_gz_index - 1 + 60) % 60
            
            gz = self.SEXAGENARY_CYCLE[current_gz_index]
            stem = gz[0]
            branch = gz[1]
            
            cycle_info = {
                "tian_gan": stem,
                "di_zhi": branch,
                "cang_gan": self.BRANCH_HIDDEN_STEM.get(branch, []),
                "year": first_cycle_year + i * 10
            }
            destiny_cycles.append(cycle_info)
            

        # TODO: 排出每个大运的年份
        return {
            "cycles": destiny_cycles,
            "start_age": start_age,
            "qiyun_date_solar": dayun_start_info['qiyun_date_solar'],
            "qiyun_date_lunar": dayun_start_info['qiyun_date_lunar'],
            "jieqi_name": self.JIE_QI_NAMES[jieqi_idx], # 生日最近的一个节气名称
            "is_forward": is_forward
        }
    
    def _get_nearest_jieqi_time(self, day: sxtwl.Day, is_forward: bool) -> Tuple[int, Tuple[int, int, int, int, int, int]]:
        """
        获取距离某日最近的下/上一个节气时间
        Args:
            date: 日期对象 (year, month, day)
            is_forward: 是否逆向查找
        Returns:
            (节气索引, 节气时间(年, 月, 日, 时, 分, 秒))
        """
        # 复制一份day对象,避免影响原始对象
        _day = sxtwl.fromSolar(day.getSolarYear(), day.getSolarMonth(), day.getSolarDay())
        while True:
            # 检查当天是否为节气日
            if _day.hasJieQi():
                t = sxtwl.JD2DD(_day.getJieQiJD())
                return _day.getJieQi(), (t.Y, t.M, t.D, round(t.h), round(t.m), round(t.s))
            # 移动到前一天或后一天
            _day = _day.after(1) if is_forward else _day.before(1)
    
    # 计算起运时间（从出生时刻到最近节气的时间差）
    def _calculate_dayun_start_age(self, birth_time: Tuple, jieqi_time: Tuple) -> dict:
        """计算两个日期之间的时间差并转换为年/月/日格式
        
        Args:
            birth_time: 出生时间元组, 格式为 (年, 月, 日, 时, 分) 阳历
            jieqi_time: 节气时间元组, 格式为 (年, 月, 日, 时, 分) 阳历
            
        Return:
            包含以下内容的字典:
            - raw_minutes: 两个日期之间的总分钟数
            - birth_to_jieqi: 出生到节气的时间差（天/小时/分钟）
            - qiyun_age: 起运时间（年/月/日）
            - qiyun_date: 起运具体日期（年/月/日）
        """
        # Parse datetime objects
        dt1 = datetime(birth_time[0], birth_time[1], birth_time[2], birth_time[3], birth_time[4])
        dt2 = datetime(jieqi_time[0], jieqi_time[1], jieqi_time[2], jieqi_time[3], jieqi_time[4])

        # Calculate minutes between dates
        delta_minutes = abs(int((dt2 - dt1).total_seconds() / 60))

        # Convert to days, hours, minutes
        days = delta_minutes // (24 * 60)
        remaining_minutes = delta_minutes % (24 * 60)
        hours = remaining_minutes // 60
        minutes = remaining_minutes % 60

        # Convert to total days including fractional
        total_days = days + (hours / 24) + (minutes / (24 * 60))

        # Convert to years/months/days using 3 days = 1 year
        years = int(total_days // 3)
        remaining_days = total_days % 3 # 带有小数的余数（天数）
        months = int(remaining_days * 4)
        remaining_months_in_days = (remaining_days * 4) % 1
        final_days = int(remaining_months_in_days * 30)

        # 计算具体起运日期
        birth_date = dt1
        
        # 将年、月、日的时间间隔转换为总天数
        total_days = years * 365 + months * 30 + final_days
        qiyun_date = birth_date + timedelta(days=total_days)
        # 将起运日期转换为农历
        qiyun_date_day = sxtwl.fromSolar(qiyun_date.year, qiyun_date.month, qiyun_date.day)
        
        return {
            "raw_minutes": delta_minutes,
            "birth_to_jieqi": {
                "days": days,
                "hours": hours,
                "minutes": minutes
            },
            "start_age": {
                "years": years,
                "months": months, 
                "days": final_days
            },
            "qiyun_date_solar": {
                "year": qiyun_date.year,
                "month": qiyun_date.month,
                "day": qiyun_date.day
            },
            "qiyun_date_lunar": {
                "year": qiyun_date_day.getLunarYear(),
                "month": qiyun_date_day.getLunarMonth(),
                "day": qiyun_date_day.getLunarDay(),
                "is_leap_month": qiyun_date_day.isLunarLeap()
            }
        }


def main():
    try:
        # 直接在代码里设日期和时间
        year, month, day, hour = 1992, 7, 27, 8
        # year, month, day, hour = 2025, 3, 4, 8
        
        # 验证输入
        if not (1900 <= year <= 2100):
            raise ValueError("年份必须在1900-2100之间")
        if not (1 <= month <= 12):
            raise ValueError("月份必须在1-12之间")
        if not (1 <= day <= 31):
            raise ValueError("日期必须在1-31之间")
        if not (0 <= hour <= 23):
            raise ValueError("小时必须在0-23之间")
        
        # 计算八字
        engine = BaziPaipanEngine()
        bazi = engine.calculate_bazi(year, month, day, hour, 0, False, "男")
        
        # 输出结果
        print("\n=== 八字排盘结果 ===")
        print(f"阳历：{year}年{month}月{day}日 {hour:02d}时")
        print("\n=== 八字信息 ===")
        for pillar in [YEAR, MONTH, DAY, HOUR]:
            print(f"{pillar}柱:")
            print(f"  天干: {bazi[pillar][STEM]}")
            print(f"  地支: {bazi[pillar][BRANCH]}")
            print(f"  藏干: {','.join(bazi[pillar][HIDDEN_STEM])}")
        
        print("\n=== 五行信息 ===")
        print("五行:", " ".join(bazi[FIVE_ELEMENTS]))
        
        print("\n=== 十神信息 ===")
        for pillar in [YEAR, MONTH, DAY, HOUR]:
            print(f"{pillar}柱十神: {bazi[TEN_GODS][pillar]}")
            
        print("\n=== 大运信息 ===")
        print("起运年龄:", bazi[DECADE_PILLAR]["start_age"])
        print("-"*10)
        qiyun_date_solar = bazi[DECADE_PILLAR]['qiyun_date_solar']
        qiyun_date_lunar = bazi[DECADE_PILLAR]['qiyun_date_lunar']
        print("起运日期（阳历）:", f"{qiyun_date_solar['year']}年{qiyun_date_solar['month']}月{qiyun_date_solar['day']}日")
        print("起运日期（农历）:", f"{qiyun_date_lunar['year']}年{'闰' if qiyun_date_lunar['is_leap_month'] else ''}{qiyun_date_lunar['month']}月{qiyun_date_lunar['day']}日")
        print("大运流程:", " ".join([f"{cycle['tian_gan']}{cycle['di_zhi']} {cycle['year']}" for cycle in bazi[DECADE_PILLAR]["cycles"]]))

        print("\n=== 八字 String ===")
        print(engine.get_bazi_string(bazi))
        
    except ValueError as e:
        print(f"输入错误：{str(e)}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    main()