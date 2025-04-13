from langchain.prompts import PromptTemplate
from typing import Dict, Any

# 八字命理报告的提示词模板
BAZI_REPORT_TEMPLATE = """
你是一名资深命理学家，熟读《三命通会》、《渊海子平》，《滴天髓》、《穷通宝鉴》、《子平真诠》等命理经典，请根据以下命主信息进行深度命盘解析：

命主信息:
- 出生日期: {lunar_date}
- 四柱八字: {bazi_str}
- 性别: {gender}
- 当前时间：{cur_date_ymd}
- 当前大运：{cur_dayun_ganzhi}
- 当前流年：{cur_liunian_ganzhi}

请根据以上信息，提供一份详细的八字命理分析报告，包括但不限于以下方面:
1. 命主的五行特点和日主旺衰分析
2. 命局特点和格局分析
3. 性格特点和天赋才能
4. 事业发展方向和建议
5. 财运分析和理财建议
6. 健康状况分析和养生建议
7. 人际关系和婚姻分析

请重点解读：
1. 整体分析格局，考虑身强身弱，分析十神关系，体用平衡。注意逻辑合理，综合各种信息文本判断准确的关系模型，交叉验证，多次迭代后输出最终正确的结果。
2. 绘制命盘能量分布图（用ASCII字符呈现五行强弱）。
3. 排出大运和流年，并列出命主的历史事件，尽量详细，细节丰富，以验证推算的准确性。
4. 分析预测命主的感情状况。
5. 分析预测2025年的运势。

可以参考的命理基础知识：
地支藏干：
子：癸
丑：己、辛、癸
寅：甲、丙、戊
卯：乙
辰：戊、乙、癸
巳：丙、庚、戊
午：丁、己
未：己、丁、乙
申：庚、壬、戊
酉：辛
戌：戊、辛、丁
亥：壬、甲

请使用专业但通俗易懂的语言，避免过于迷信的说法，注重实用性建议。
请使用Markdown格式组织你的回答，使用适当的标题、列表和强调，使报告更加清晰易读。
"""

# 创建提示词模板
bazi_report_prompt = PromptTemplate(
    input_variables=["solar_date_ymd", "lunar_date_ymd", "birth_time_hour", "sizhu_str", "gender", "cur_date_ymd", "cur_dayun_ganzhi", "cur_liunian_ganzhi"],
    template=BAZI_REPORT_TEMPLATE
)

def get_bazi_report_prompt(fate_owner_data: Dict[str, Any]) -> str:
    """
    根据命主信息生成八字命理报告的提示词
    
    Args:
        fate_owner_data: 包含命主信息的字典，包含以下键:
            - gender         : str, 性别 ("male" 或 "female")
            - solar_date_ymd : str, 出生日期, "2000年1月1日"
            - lunar_date_ymd : str, 农历日期, "2000年1月1日"
            - birth_time_hour: str, 出生时辰, "下午2点"
            - sizhu_str      : str, 八字, "庚辰 戊子 丙寅 乙未"
            - current_date   : str, 当前日期, "2025年1月1日"
            - current_dayun  : str, 当前大运, "庚辰"
            - current_liunian: str, 当前流年
    
    Returns:
        格式化后的提示词字符串
    """
    gender_str = "男" if fate_owner_data.get("gender") == "male" else "女"
    
    return bazi_report_prompt.format(
        solar_date_ymd=fate_owner_data.get("birth_date", ""),
        lunar_date_ymd=fate_owner_data.get("lunar_date", ""),
        birth_time_hour=fate_owner_data.get("birth_time", ""),
        sizhu_str=fate_owner_data.get("bazi", ""),
        gender=gender_str,
        cur_date_ymd=fate_owner_data.get("current_date", ""),
        cur_dayun_ganzhi=fate_owner_data.get("current_dayun", ""),
        cur_liunian_ganzhi=fate_owner_data.get("current_liunian", "")
    )