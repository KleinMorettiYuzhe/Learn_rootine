#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
玄幻人生模拟器 —— 控制台版
回车推进一年，输入 q 退出
"""

import random
import time

# ==================== 基础数据 ====================
SURNAMES = "叶林萧楚苏秦李王张刘陈杨赵黄周吴徐孙胡朱高何郭马罗梁宋郑谢韩唐冯于董萧程曹袁邓许傅沈曾彭吕苏卢蒋蔡贾丁魏薛阎余潘杜戴夏钟汪田任姜范方石姚谭廖邹熊金陆郝孔白崔康毛邱秦江史顾侯邵孟龙万段雷钱汤尹易常武乔贺赖龚文".split()
GIVEN = "天宇浩然逸尘无极辰轩子涵若风云霆渊凌寒雨雪秋月夜夕阳炎焱淼鑫森垚磊沐沧溟鸿鹏鹤鸾麒麟龙".split()
ROOTS = ["废灵根", "杂灵根", "三灵根", "双灵根", "单灵根", "天灵根", "异灵根"]
ROOT_BONUS = {"废灵根": 0.3, "杂灵根": 0.5, "三灵根": 0.7, "双灵根": 0.9,
              "单灵根": 1.0, "天灵根": 1.5, "异灵根": 1.1}
REALMS = ["凡人", "炼气期", "筑基期", "金丹期", "元婴期", "化神期", "合体期", "大乘期", "渡劫期", "真仙"]
REALM_LIFESPAN = {"凡人": 100, "炼气期": 150, "筑基期": 200, "金丹期": 500,
                  "元婴期": 1000, "化神期": 3000, "合体期": 10000,
                  "大乘期": 50000, "渡劫期": float('inf'), "真仙": float('inf')}
SECTS = ["青云宗", "天魔宗", "万剑宗", "灵兽山", "药王谷", "星辰阁", "幽冥殿"]
EVENT_TAGS = set()  # 记录已发生的唯一事件

# ==================== 角色类 ====================
class Character:
    def __init__(self, name):
        self.name = name
        self.age = 0
        self.realm = "凡人"
        self.realm_idx = 0
        self.sect = None
        self.root = None          # 6岁觉醒
        self.tags = set()         # 剧情标记
        self.cd = {}              # 冷却计数器（事件标签 -> 年份）
        self.lifespan_bonus = 0
        self.alive = True

    @property
    def max_age(self):
        return REALM_LIFESPAN[self.realm] + self.lifespan_bonus

    def advance_realm(self):
        if self.realm_idx < len(REALMS) - 1:
            self.realm_idx += 1
            self.realm = REALMS[self.realm_idx]
            return True
        return False

    def set_cd(self, tag, years):
        self.cd[tag] = self.age + years

    def is_ready(self, tag):
        return self.age >= self.cd.get(tag, 0)


# ==================== 事件系统 ====================
class Event:
    def __init__(self, cond, action, weight=1, fixed=False, tag="", once=True, cd=0):
        self.cond = cond          # lambda ch -> bool
        self.action = action      # lambda ch -> str (返回描述)
        self.weight_fn = weight if callable(weight) else (lambda ch: weight)
        self.fixed = fixed        # 固定事件：若满足条件必定触发
        self.tag = tag
        self.once = once          # 是否只触发一次
        self.cd = cd              # 触发后冷却年数

    def check(self, ch):
        if self.once and self.tag in ch.tags:
            return False
        if self.tag and not ch.is_ready(self.tag):
            return False
        try:
            return self.cond(ch)
        except:
            return False

    def run(self, ch):
        if self.tag:
            ch.tags.add(self.tag)
            if self.cd:
                ch.set_cd(self.tag, self.cd)
        return self.action(ch)


# ==================== 创建事件库 ====================
def build_events():
    pool = []

    def add(cond, action, weight=1, fixed=False, tag="", once=True, cd=0):
        pool.append(Event(cond, action, weight, fixed, tag, once, cd))

    # ----- 固定里程碑 -----
    add(lambda c: c.age == 0,
        lambda c: f"你出生在{random.choice(['偏僻山村','繁华城镇','修仙家族旁支','猎户之家','书香门第'])}，取名{c.name}。",
        fixed=True, tag="birth")

    add(lambda c: c.age == 6,
        lambda c: setattr(c, 'root', random.choice(ROOTS)) or f"六岁测灵，测灵石显示：{c.root}！",
        fixed=True, tag="root")

    add(lambda c: c.age == 12,
        lambda c: (
            setattr(c, 'sect', random.choice(SECTS)) if c.root != "废灵根" else setattr(c, 'sect', None),
            f"十二岁拜师，{'被' + c.sect + '收入门下' if c.sect else '因灵根太差无人收留，沦为散修'}。" 
        )[1],
        fixed=True, tag="sect")

    add(lambda c: c.age == 18,
        lambda c: "你成年了，开始独立行走修仙界。",
        fixed=True, tag="adult")

    add(lambda c: c.age == 30 and "world_evil" not in c.tags,
        lambda c: (c.tags.add("world_evil"), "天地异变！魔界裂缝开启，魔潮席卷大陆。")[1],
        fixed=True, tag="world_evil")

    add(lambda c: c.age == 60 and "relic_open" not in c.tags,
        lambda c: (c.tags.add("relic_open"), "东海有上古遗迹现世，各方势力云集。")[1],
        fixed=True, tag="relic_open")

    # ----- 境界突破（可重复尝试，但有冷却）-----
    breakthroughs = [
        ("凡人", "炼气期", 10, 0.6),
        ("炼气期", "筑基期", 30, 0.5),
        ("筑基期", "金丹期", 80, 0.4),
        ("金丹期", "元婴期", 200, 0.3),
        ("元婴期", "化神期", 500, 0.2),
        ("化神期", "合体期", 2000, 0.15),
        ("合体期", "大乘期", 8000, 0.1),
    ]
    for prev, next_r, min_age, base_prob in breakthroughs:
        tag = f"try_{prev}_to_{next_r}"
        def make_act(prev, next_r, base_prob):
            def action(ch):
                prob = base_prob * ROOT_BONUS.get(ch.root, 1.0)
                if random.random() < prob:
                    ch.advance_realm()
                    return f"突破成功！你踏入了全新的境界——{next_r}！"
                else:
                    damage = random.choice(["经脉受损", "修为略有倒退", "心魔丛生"])
                    if "修为倒退" in damage and ch.realm_idx > 0:
                        ch.realm_idx -= 1
                        ch.realm = REALMS[ch.realm_idx]
                    return f"突破失败，{damage}，需要调养。"
            return action
        add(lambda c, prev=prev, next_r=next_r: c.realm == prev and c.age >= min_age,
            make_act(prev, next_r, base_prob),
            weight=lambda c: 5, tag=tag, once=False, cd=15)

    # 飞升天劫（大乘期终极事件）
    def finish_ascend(ch):
        ch.alive = False
        if random.random() < 0.6:
            return "九九重劫降下，你以莫大毅力渡过，飞升仙界！【结局：飞升成仙】"
        else:
            return "天劫之下，肉身崩毁，魂魄散尽。【结局：渡劫失败】"
    add(lambda c: c.realm == "大乘期" and c.age >= 10000 and "try_ascend" not in c.tags,
        finish_ascend, weight=999, fixed=True, tag="try_ascend", once=True)

    # ----- 随机日常事件 -----
    daily_templates = [
        "你在宗门后山静修，心境平和。",
        "你在坊市闲逛，偶有所悟。",
        "你与同门切磋，武艺精进。",
        "你研读前辈手札，理解加深。",
        "你外出游历，增广见闻。",
        "你闭关数日，灵力稳固。",
        "你帮助同门炼丹，获得好感。",
        "你独自在山巅观云，心有所感。",
        "你于瀑布下炼体，气血强盛。",
    ]
    def daily_action(ch):
        return random.choice(daily_templates)
    add(lambda c: True, daily_action, weight=2, tag="daily_random", once=False, cd=1)

    # ----- 奇遇机缘 -----
    def adventure(ch):
        desc, eff = random.choice([
            ("你发现一株千年灵芝，修为提升。", "boost"),
            ("你坠入古洞，获得残缺神通。", "skill"),
            ("你救下一只灵兽，它自愿跟随。", "pet"),
            ("你捡到一枚破损护甲，尚可防御。", "item"),
            ("你误入秘境，得到神秘玉简。", "jade"),
            ("天降陨星，你获得一块天外陨铁。", "metal"),
            ("你帮助老者，被赠予延寿果。", "longevity"),
        ])
        if "longevity" in desc:
            ch.lifespan_bonus += 30
        return desc
    add(lambda c: c.age >= 10, adventure, weight=1.8, once=False, cd=5, tag="adventure_random")

    # ----- 劫难与负面事件 -----
    def disaster(ch):
        desc, action = random.choice([
            ("你修炼时走火入魔，吐血昏迷。", lambda c: None),
            ("你遭遇魔修偷袭，身受重伤。", lambda c: None),
            ("你被同门嫉妒，陷害逐出师门。", lambda c: setattr(c, 'sect', None)),
            ("你误入毒瘴区域，中毒卧床三年。", lambda c: c.age + 2),  # 年龄+2 模拟时间流逝
            ("你被强敌寻仇，法宝损坏。", lambda c: None),
            ("宗门遭魔潮冲击，损失惨重。", lambda c: None),
        ])
        if action:
            action(ch)
        return desc
    add(lambda c: c.age >= 20, disaster, weight=0.9, once=False, cd=8, tag="disaster_random")

    # ----- 人际关系事件 -----
    relation_templates = [
        "你在任务中结识一位挚友。",
        "你与一位女修情投意合。",
        "你遇到一位桀骜不驯的天才。",
        "你在酒馆偶遇一位神秘散修。",
        "你结识了一位炼器大师。",
    ]
    add(lambda c: c.age >= 16, lambda c: random.choice(relation_templates),
        weight=1.5, once=False, cd=3, tag="relation_random")

    # ----- 势力相关任务（宗门/散修）-----
    def sect_quest(ch):
        if not ch.sect:
            return random.choice([
                "你加入散修联盟，接取悬赏。",
                "你在黑市交换情报，小有收获。",
                "你与流浪修士一同猎杀妖兽。",
            ])
        return random.choice([
            f"{ch.sect}派遣你护送物资，顺利完成。",
            f"{ch.sect}举办大比，你参与其中。",
            f"你代表{ch.sect}出使其他宗门。",
        ])
    add(lambda c: c.sect is not None or c.age > 20, sect_quest, weight=1.2, once=False, cd=4, tag="quest_random")

    # ----- 寿命预警与延寿 -----
    add(lambda c: c.max_age - c.age < 20 and "lifespan_warn" not in c.tags,
        lambda c: (c.tags.add("lifespan_warn"), 
                   "你感到气血衰败，寿元将尽，必须寻找延寿之物或突破！")[1],
        weight=10, fixed=True, tag="lifespan_warn", once=True)

    def extend_life_action(c):
        c.lifespan_bonus += 50
        c.tags.discard("lifespan_warn")
        return "侥幸获得一株仙草，为你延寿50年。"

    add(lambda c: "lifespan_warn" in c.tags and "extended" not in c.tags,
        extend_life_action,
        weight=5, once=True, tag="extended")

    # 寿终正寝
    add(lambda c: c.age >= c.max_age and c.alive,
        lambda c: (setattr(c, 'alive', False), 
                   f"你寿元耗尽，安然坐化，享年{c.age}岁。【结局：寿终正寝】")[1],
        fixed=True, weight=999, tag="death_natural")

    return pool


# ==================== 主循环 ====================
def main():
    print("=" * 60)
    print("         🏮 玄幻人生模拟器 🏮")
    print("=" * 60)
    name = input("请输入主角名字（回车随机）：").strip()
    if not name:
        name = random.choice(SURNAMES) + random.choice(GIVEN) + random.choice(GIVEN)
    ch = Character(name)
    events = build_events()
    print(f"\n《{ch.name}传》开始。逐年行车，按回车推进，输入 q 退出。\n")
    time.sleep(0.5)

    while ch.alive:
        # 先检查是否直接寿尽
        if ch.age >= ch.max_age:
            print(f"\n【第{ch.age}年】寿元已尽，你安详离世。")
            break

        # 显示状态
        banner = f"\n{'─' * 40}\n【第 {ch.age} 年】"
        banner += f"\n姓名：{ch.name}\t年龄：{ch.age}\t境界：{ch.realm}"
        banner += f"\n灵根：{ch.root or '未知'}\t宗门：{ch.sect or '散修'}"
        if "lifespan_warn" in ch.tags:
            banner += "\n⚠️ 你已近大限！"
        print(banner)

        cmd = input("按回车继续...").strip()
        if cmd.lower() == 'q':
            print("你主动结束了此生。")
            break

        # 筛选可用事件
        available = [e for e in events if e.check(ch)]
        if not available:
            print("这一年平淡如水，你安静地度过了一年。")
            ch.age += 1
            continue

        # 固定事件必须触发
        fixed = [e for e in available if e.fixed]
        if fixed:
            chosen = fixed[0]
        else:
            # 按权重随机抽取
            weights = [e.weight_fn(ch) for e in available]
            total = sum(weights)
            r = random.uniform(0, total)
            cumulative = 0
            chosen = available[0]
            for ev, w in zip(available, weights):
                cumulative += w
                if r <= cumulative:
                    chosen = ev
                    break

        # 执行事件
        try:
            age_before = ch.age
            desc = chosen.run(ch)
            # 某些事件可能直接修改了年龄（如中毒卧床）
            years_passed = ch.age - age_before
            print(f"\n{desc}")
            if years_passed > 1:
                print(f"（时间流逝，你度过了 {years_passed} 年）")
        except Exception as e:
            print(f"事件执行错误：{e}")
            # 恢复年龄
            ch.age = age_before

        # 若事件未增加年龄则默认+1
        if ch.age == age_before:
            ch.age += 1

        time.sleep(0.3)

    print(f"\n{'═' * 60}")
    print(f"《{ch.name}传》终。")
    print(f"最终修为：{ch.realm}\t享年：{ch.age} 岁")
    print(f"{'═' * 60}\n")
    input("按回车退出……")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n游戏中断。")