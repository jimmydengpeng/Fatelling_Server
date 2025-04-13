from typing import Dict, List, Optional
from server.paipan_engine import BaziPaipanEngine
from server.define import Gender, SolarBirthInfo, LunarBirthInfo, BaziInfo, PillarInfo, HeavenlyStem, EarthlyBranch, TenGodInfo, TenGodType, DestinyCycleInfo, StartAge


class FateOwner():
    """命主类，包含生日信息和八字信息"""
    name: Optional[str] = None
    gender: Gender
    solar_birth_info: Optional[SolarBirthInfo] = None
    lunar_birth_info: Optional[LunarBirthInfo] = None
    bazi_info: Optional[BaziInfo] = None
    engine: BaziPaipanEngine = BaziPaipanEngine()
    
    def __init__(self, gender: Gender = None, solar_birth_info: SolarBirthInfo = None, lunar_birth_info: LunarBirthInfo = None, name: str = None):
        self.gender = gender
        self.solar_birth_info = solar_birth_info
        self.lunar_birth_info = lunar_birth_info
        self.name = name
        
        # 如果只提供了一种生日信息，自动转换生成另一种
        if self.solar_birth_info and not self.lunar_birth_info:
            self._convert_solar_to_lunar()
        elif self.lunar_birth_info and not self.solar_birth_info:
            self._convert_lunar_to_solar()
    
    def _convert_solar_to_lunar(self):
        """将阳历转换为农历"""
        if not self.solar_birth_info:
            return
            
        # 使用排盘引擎进行转换
        lunar_info = self.engine.solar_to_lunar(
            self.solar_birth_info.year,
            self.solar_birth_info.month,
            self.solar_birth_info.day
        )
        
        # 获取农历信息
        self.lunar_birth_info = LunarBirthInfo(
            year=lunar_info["year"],
            month=lunar_info["month"],
            day=lunar_info["day"],
            hour=self.solar_birth_info.hour,
            minute=self.solar_birth_info.minute,
            is_leap_month=lunar_info["is_leap_month"]
        )
    
    def _convert_lunar_to_solar(self):
        """将农历转换为阳历"""
        if not self.lunar_birth_info:
            return
            
        # 使用排盘引擎进行转换
        solar_info = self.engine.lunar_to_solar(
            self.lunar_birth_info.year,
            self.lunar_birth_info.month,
            self.lunar_birth_info.day,
            self.lunar_birth_info.is_leap_month
        )
        
        # 获取阳历信息
        self.solar_birth_info = SolarBirthInfo(
            year=solar_info["year"],
            month=solar_info["month"],
            day=solar_info["day"],
            hour=self.lunar_birth_info.hour,
            minute=self.lunar_birth_info.minute
        )
    
    def calculate_bazi(self, engine: BaziPaipanEngine = None) -> BaziInfo:
        """计算八字信息"""
        # 使用传入的引擎或默认引擎
        paipan_engine = engine if engine else self.engine
        
        # 确保有农历信息用于计算
        if not self.lunar_birth_info:
            if self.solar_birth_info:
                self._convert_solar_to_lunar()
            else:
                raise ValueError("需要阳历或农历生日信息才能计算八字")
        
        # 使用排盘引擎计算八字
        bazi_dict = paipan_engine.calculate_bazi(
            lunar_year    = self.lunar_birth_info.year,
            lunar_month   = self.lunar_birth_info.month,
            lunar_day     = self.lunar_birth_info.day,
            hour          = self.lunar_birth_info.hour,
            is_leap_month = self.lunar_birth_info.is_leap_month,
            gender        = str(self.gender)
        )
        
        # 构建PillarInfo对象
        year_pillar = PillarInfo(
            heavenly_stem=HeavenlyStem(bazi_dict["year"]["heavenly_stem"]),
            earthly_branch=EarthlyBranch(bazi_dict["year"]["earthly_branch"]),
            hidden_stem=[HeavenlyStem(stem) for stem in bazi_dict["year"]["hidden_stems"]]
        )
        month_pillar = PillarInfo(
            heavenly_stem=HeavenlyStem(bazi_dict["month"]["heavenly_stem"]),
            earthly_branch=EarthlyBranch(bazi_dict["month"]["earthly_branch"]),
            hidden_stem=[HeavenlyStem(stem) for stem in bazi_dict["month"]["hidden_stems"]]
        )
        day_pillar = PillarInfo(
            heavenly_stem=HeavenlyStem(bazi_dict["day"]["heavenly_stem"]),
            earthly_branch=EarthlyBranch(bazi_dict["day"]["earthly_branch"]),
            hidden_stem=[HeavenlyStem(stem) for stem in bazi_dict["day"]["hidden_stems"]]
        )
        hour_pillar = PillarInfo(
            heavenly_stem=HeavenlyStem(bazi_dict["hour"]["heavenly_stem"]),
            earthly_branch=EarthlyBranch(bazi_dict["hour"]["earthly_branch"]),
            hidden_stem=[HeavenlyStem(stem) for stem in bazi_dict["hour"]["hidden_stems"]]
        )
        
        # 构建十神信息
        ten_gods = {}
        if "ten_gods" in bazi_dict:
            for pillar_name, gods in bazi_dict["ten_gods"].items():
                ten_gods[pillar_name] = TenGodInfo(
                    heavenly_stem=TenGodType(gods["heavenly_stem"]),
                    earthly_branch=TenGodType(gods["earthly_branch"]),
                    hidden_stems=[TenGodType(god) for god in gods["hidden_stems"]]
                )
        
        # 计算大运信息
        destiny_cycle = None
        lunar_date = {
            "year": self.lunar_birth_info.year,
            "month": self.lunar_birth_info.month,
            "day": self.lunar_birth_info.day,
            "hour": self.lunar_birth_info.hour,
            "is_leap_month": self.lunar_birth_info.is_leap_month
        }
        destiny_dict = self.engine.calculate_destiny_cycles(lunar_date, str(self.gender))
        
        if destiny_dict:
            destiny_cycles = [
                PillarInfo(
                    heavenly_stem=HeavenlyStem(cycle["heavenly_stem"]),
                    earthly_branch=EarthlyBranch(cycle["earthly_branch"]),
                    hidden_stem=[HeavenlyStem(stem) for stem in cycle["hidden_stems"]]
                )
                for cycle in destiny_dict["cycles"]
            ]
            
            destiny_cycle = DestinyCycleInfo(
                cycles=destiny_cycles,
                start_age=StartAge(**destiny_dict["start_age"]),
                is_forward=destiny_dict["is_forward"]
            )
        
        # 创建八字信息
        self.bazi_info = BaziInfo(
            year_pillar=year_pillar,
            month_pillar=month_pillar,
            day_pillar=day_pillar,
            hour_pillar=hour_pillar,
            five_elements=bazi_dict["five_elements"],
            ten_gods=ten_gods,
            destiny_cycle=destiny_cycle
        )
        
        return self.bazi_info
    
    def get_summary(self) -> str:
        """获取命主信息摘要"""
        summary = [
            f"姓名: {self.name or '未知'}",
            f"性别: {self.gender}"
        ]
        
        if self.solar_birth_info:
            summary.append(f"阳历: {self.solar_birth_info}")
        if self.lunar_birth_info:
            summary.append(f"农历: {self.lunar_birth_info}")
        
        if self.bazi_info:
            summary.extend([
                f"八字: {self.bazi_info.get_bazi_string()}",
                f"八字(含藏干): {self.bazi_info.get_bazi_string_with_hidden_stem()}",
                f"五行: {self.bazi_info.get_five_elements_string()}"
            ])
            
            if self.bazi_info.destiny_cycle:
                summary.append(f"大运: {self.bazi_info.destiny_cycle.get_cycles_string()}")
        
        return "\n".join(summary)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "FateOwner":
        """从字典创建FateOwner实例"""
        # 判断是否包含农历信息
        has_lunar = all(key in data for key in ["lunar_year", "lunar_month", "lunar_day"])
        # 判断是否包含阳历信息
        has_solar = all(key in data for key in ["year", "month", "day"])
        
        if not (has_lunar or has_solar):
            raise ValueError("需要提供阳历或农历生日信息")
        
        # 构建阳历信息
        solar_birth_info = None
        if has_solar:
            solar_birth_info = SolarBirthInfo(
                year=data["year"],
                month=data["month"],
                day=data["day"],
                hour=data.get("hour", 0),
                minute=data.get("minute", 0)
            )
        
        # 构建农历信息
        lunar_birth_info = None
        if has_lunar:
            lunar_birth_info = LunarBirthInfo(
                year=data["lunar_year"],
                month=data["lunar_month"],
                day=data["lunar_day"],
                hour=data.get("hour", 0),
                minute=data.get("minute", 0),
                is_leap_month=data.get("is_leap_month", False)
            )
        
        return cls(
            name=data.get("name"),
            gender=data["gender"],
            solar_birth_info=solar_birth_info,
            lunar_birth_info=lunar_birth_info
        ) 