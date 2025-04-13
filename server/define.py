from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class Gender(str, Enum):
    """性别枚举"""
    MALE   = "男"
    FEMALE = "女"

    def __str__(self) -> str:
        """返回性别汉字"""
        return self.value

class HeavenlyStem(str, Enum):
    """十天干枚举"""
    JIA  = "甲"
    YI   = "乙"
    BING = "丙"
    DING = "丁"
    WU   = "戊"
    JI   = "己"
    GENG = "庚"
    XIN  = "辛"
    REN  = "壬"
    GUI  = "癸"

    def __str__(self) -> str:
        """返回天干汉字"""
        return self.value

class EarthlyBranch(str, Enum):
    """十二地支枚举"""
    ZI   = "子"
    CHOU = "丑"
    YIN  = "寅"
    MAO  = "卯"
    CHEN = "辰"
    SI   = "巳"
    WU   = "午"
    WEI  = "未"
    SHEN = "申"
    YOU  = "酉"
    XU   = "戌"
    HAI  = "亥"

    def __str__(self) -> str:
        """返回地支汉字"""
        return self.value

class TenGodType(str, Enum):
    """十神枚举"""
    BI_JIAN    = "比肩"
    JIE_CAI    = "劫财"
    SHI_SHEN   = "食神"
    SHANG_GUAN = "伤官"
    ZHENG_CAI  = "正财"
    PIAN_CAI   = "偏财"
    ZHENG_GUAN = "正官"
    QI_SHA     = "七杀"
    ZHENG_YIN  = "正印"
    PIAN_YIN   = "偏印"

    def __str__(self) -> str:
        """返回十神汉字"""
        return self.value

# TODO: 把所有命理知识归纳到专门的数据库模块中
# 地支藏干对应表（简化，只列出本气）
BRANCH_HIDDEN_STEM = {
    "子": ["癸", "癸"], 
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


class SolarBirthInfo(BaseModel):
    """阳历生日信息数据结构"""
    gender: str = Field(..., description="性别，male或female")
    year  : int = Field(..., ge=1900, le=2100, description="出生年份，范围1900-2100")
    month : int = Field(..., ge=1, le=12, description="出生月份，范围1-12")
    day   : int = Field(..., ge=1, le=31, description="出生日期，范围1-31")
    hour  : int = Field(..., ge=0, le=23, description="出生小时，范围0-23")
    minute: int = Field(0,   ge=0, le=59, description="出生分钟，范围0-59")
    
    def __str__(self) -> str:
        """返回格式化的生日字符串"""
        return f"{self.year}年{self.month}月{self.day}日 {self.hour:02d}:{self.minute:02d}"


class BasicUserInput(BaseModel):
    """用户提交的基本信息"""
    gender: str = Field(..., description="性别，male或female")
    year  : int = Field(..., ge=1900, le=2100, description="出生年份，范围1900-2100")
    month : int = Field(..., ge=1, le=12, description="出生月份，范围1-12")
    day   : int = Field(..., ge=1, le=31, description="出生日期，范围1-31")
    hour  : int = Field(..., ge=0, le=23, description="出生小时，范围0-23")
    minute: int = Field(0,   ge=0, le=59, description="出生分钟，范围0-59")
    
    def to_solar_birth_info(self) -> SolarBirthInfo:
        """转换为阳历生日信息"""
        return SolarBirthInfo(
            gender=self.gender,
            year=self.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute
        )


class LunarBirthInfo(BaseModel):
    """农历生日信息数据结构"""
    year         : int  = Field(..., ge=1900, le=2100, description="农历年份，范围1900-2100")
    month        : int  = Field(..., ge=1, le=12, description="农历月份，范围1-12")
    day          : int  = Field(..., ge=1, le=30, description="农历日期，范围1-30")
    hour         : int  = Field(..., ge=0, le=23, description="出生小时，范围0-23")
    minute       : int  = Field(0,   ge=0, le=59, description="出生分钟，范围0-59")
    is_leap_month: bool = Field(False, description="是否闰月")
    
    def __str__(self) -> str:
        """返回格式化的农历生日字符串"""
        leap_str = "闰" if self.is_leap_month else ""
        return f"农历{self.year}年{leap_str}{self._to_lunar_month_name(self.month)}月{self._to_lunar_day_name(self.day)} {self.hour:02d}:{self.minute:02d}"

    def _to_lunar_month_name(self, month: int) -> str:
        lunar_month_name = [ "正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊" ] 
        return lunar_month_name[month - 1]

    def _to_lunar_day_name(self, day: int) -> str:
        lunar_day_name = [
            "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", 
            "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", 
            "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"
        ]
        return lunar_day_name[day - 1]


class PillarInfo(BaseModel):
    """单柱信息（天干地支）"""
    heavenly_stem : HeavenlyStem                 = Field(..., description="天干")
    earthly_branch: EarthlyBranch                = Field(..., description="地支")
    hidden_stem   : Optional[List[HeavenlyStem]] = Field(None, description="地支藏干")
    
    def __init__(self, **data):
        super().__init__(**data)
        # 如果没有提供hidden_stem，根据地支查找藏干
        if not self.hidden_stem and self.earthly_branch:
            branch_str = self.earthly_branch.value
            if branch_str in BRANCH_HIDDEN_STEM:
                self.hidden_stem = [HeavenlyStem(stem) for stem in BRANCH_HIDDEN_STEM[branch_str]]

    def __str__(self) -> str:
        """返回天干地支的汉字组合"""
        return f"{self.heavenly_stem}{self.earthly_branch}"


class TenGodInfo(BaseModel):
    """十神信息"""
    heavenly_stem : TenGodType       = Field(..., description="天干十神")
    earthly_branch: TenGodType       = Field(..., description="地支十神")
    hidden_stems  : List[TenGodType] = Field(default_factory=list, description="藏干十神")


class StartAge(BaseModel):
    """起运年龄信息"""
    years : int = Field(..., description="年")
    months: int = Field(..., description="月")
    days  : int = Field(..., description="天")
    
    def __str__(self) -> str:
        """返回格式化的起运年龄字符串"""
        return f"{self.years}岁{self.months}个月{self.days}天"


class DestinyCycleInfo(BaseModel):
    """大运信息数据结构"""
    cycles    : List[PillarInfo] = Field(..., description="大运列表")
    start_age : StartAge         = Field(..., description="起运年龄")
    is_forward: bool             = Field(..., description="是否顺行")
    
    def get_cycles_string(self) -> str:
        """返回格式化的大运信息字符串"""
        cycles_str = []
        for i, cycle in enumerate(self.cycles, 1):
            age = (i * 10) + self.start_age.years
            cycles_str.append(f"{cycle}({age}岁)")
        
        direction = "顺" if self.is_forward else "逆"
        return f"起运：{self.start_age}\n{direction}行：{' '.join(cycles_str)}"


class BaziInfo(BaseModel):
    """八字信息数据结构"""
    
    '''四柱'''
    year_pillar : PillarInfo = Field(..., description="年柱")
    month_pillar: PillarInfo = Field(..., description="月柱")
    day_pillar  : PillarInfo = Field(..., description="日柱")
    hour_pillar : PillarInfo = Field(..., description="时柱")
    
    # TODO: 扩展到地支
    '''五行'''
    five_elements: List[str] = Field(default_factory=list, description="五行")
    
    '''十神'''
    ten_gods: Dict[str, TenGodInfo] = Field(default_factory=dict, description="十神")
    
    '''大运'''
    destiny_cycle: Optional[DestinyCycleInfo] = Field(None, description="大运信息")
    
    def get_bazi_string(self) -> str:
        """返回八字字符串，如'甲子 乙丑 丙寅 丁卯'"""
        return f"{self.year_pillar} {self.month_pillar} {self.day_pillar} {self.hour_pillar}"
    
    def get_bazi_string_with_hidden_stem(self) -> str:
        """返回带藏干的八字字符串"""
        pillars = []
        for pillar in [self.year_pillar, self.month_pillar, self.day_pillar, self.hour_pillar]:
            hidden_stems = f"（{', '.join(str(stem) for stem in pillar.hidden_stem)}）" if pillar.hidden_stem else ""
            pillars.append(f"{pillar}{hidden_stems}")
        return " ".join(pillars)
    
    def get_five_elements_string(self) -> str:
        """返回五行字符串"""
        return " ".join(self.five_elements)