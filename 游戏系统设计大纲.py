import time

class Core:               #核心系统
    class Event:          #事件系统
        pass
    class Time:           #时间系统
        pass
    class Config:         #配置系统
        pass
    class Input:          #输入系统
        pass
    class Output:         #输出系统
        pass
    class Factory:        #工厂系统
        def __init__(self,core):
            self.core = core           #获得核心类的使用权限
            self.config = core.config  #获取配置
            self.production_log = []   #生产日志
        def _create_character(self):    #创建角色
            pass
        def _create_consumable(self):   #创建消耗品
            pass
        def _create_map(self):          #创建地图
            pass
class Combat:             #战斗系统
    class Harm:           #伤害系统
        def __init__(self,core,harm_config=None):
            self.core = core
            self.config = core.config
            self.motion_body_harm = 0               #动态身体伤害，类内储存
            self.motion_armor_harm = 0              #动态护甲伤害，类内储存
            self.harm_level = 0                     #等级初始为零
            self.harm_time = 0                      #伤害时间，类内储存
            self.level_start_time = None            #伤害等级开始时间
            self.level_end_time = 0                 #伤害等级超时后的降级时间
            self.harm_pace = 0                      #伤害频率，类内存储
            self.harm_type = []                     #伤害类型，类内存储
            self.events = []                        #事件存储列表
            self.harm_log = []                      #日志
            self.harm_dictionary = {}               #输出字典，所有伤害输出值集合到这
            #伤害系统初始化
            self.harm_list = []
            if harm_config is not None:
                self._init_harm(harm_config)
        def _init_harm(self,config):
            for harm in config:
                harm = {
                    "name":harm["name"],
                    "body_harm_value":harm["body_harm_value"],               #基础身体伤害
                    "armor_harm_value":harm["armor_harm_value"],             #基础护甲伤害
                    "harm_level_max":harm["harm_level_max"],                 #伤害最大等级
                    "harm_level_time":harm["harm_level_time"],               #维持等级的时间
                    "harm_level_end_time":harm["harm_level_end_time"],       #等级超时后的等级持续时间
                    "harm_level_lose_number":harm["harm_level_lose_number"], #默认每次损失等级数
                    "harm_pace":harm["harm_pace"],                           #伤害频率，伤害次数
                    "harm_type":dict(harm["harm_type"])                      #伤害类型，此处为字典
                }
                self.harm_list.append(harm)
        def _get_harm(self,harm_name):                                       #获取单次实例
            for harm in self.harm_list:
                if harm["name"] == harm_name:
                    return  harm
            return None
        def _get_harm_attr(self,harm_name,attr_name):                        #方便使用实例内属性
            harm = self._get_harm(harm_name)
            if harm is None:
                return None
            return harm.get(attr_name,0)
        def _get_armor_harm_value(self,harm_name):
            return self._get_harm_attr(harm_name,"armor_harm_value")
        def _get_body_harm_value(self,harm_name):
            return self._get_harm_attr(harm_name,"body_harm_value")
        def _get_harm_pace(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_pace")
        def _get_harm_type(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_type")
        def _get_harm_level_max(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_level_max")
        def _get_harm_level_time(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_level_time")
        def _get_harm_level_end_time(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_level_end_time")
        def _get_harm_level_lose_number(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_level_lose_number")
        def _add_level(self,harm_name,level_event_number):                      #改变等级方法
            harm_level_max = self._get_harm_level_max(harm_name)
            self.harm_level = min(self.harm_level + level_event_number,harm_level_max)
            if self.harm_level < 0:
                self.harm_level = 0
            self.level_start_time = time.time()      #重置计时
        def _get_current_level(self,harm_name):                                 #获取当前等级
            harm_level_time = self._get_harm_level_time(harm_name)
            if self.harm_level == 0:
                return 0
            elapsed_time = time.time() - self.level_start_time
            if elapsed_time > harm_level_time:
                self._lower_level(harm_name)
                return self._get_current_level(harm_name)
            return self.harm_level
        def _lower_level(self,harm_name):                                       #默认降级方法
            harm_level_end_time = self._get_harm_level_end_time(harm_name)
            harm_level_lose_number = self._get_harm_level_lose_number(harm_name)
            if self.harm_level <= 0:
                return 0
            elapsed_time = time.time() - self.level_start_time
            levels_to_lose = int(elapsed_time / harm_level_end_time) * harm_level_lose_number           #默认过一定时间降x级
            self.harm_level = max(0,self.harm_level - levels_to_lose)
            if self.harm_level > 0:
                self.level_start_time = time.time()
            else:
                self.level_start_time = None
            return self.harm_level
    class HP:             #血量系统
        def __init__(self,core,max_hp,armor,armor_durability_max,body_part_config=None,armor_part_config=None,owner_type="character",source_type="name"):
            self.core = core
            self.config = core.config
            self.max_hp = max_hp                                 #血量上限
            self.hp = max_hp                                     #当前血量
            self.armor = armor                                   #当前护甲
            self.armor_durability_max = armor_durability_max     #护甲上限
            self.low_armor = 0                                   #护甲下限
            self.owner_type = owner_type                         #目标
            self.source_type = source_type                       #来源
            self.events = []                                     #事件
            self.treat_log = []                                  #日志
            self.HP_dictionary = {}                              #输出字典，所有HP输出值集合到这
            #身体部位初始化
            self.body_part_list = []
            if body_part_config is not None:
                self._init_body_parts(body_part_config)
            #护甲部位初始化
            self.armor_part_list = []
            if armor_part_config is not None:
                self._init_amor_parts(armor_part_config)
        def _init_body_parts(self,config):
            for part in config:
                body_part = {
                    "name":part["name"],
                    "hp_max":part["hp_max"],
                    "hp":part["hp_max"],
                    "resistance":dict(part["resistance"]),
                }
                self.body_part_list.append(body_part)
        def _init_amor_parts(self,config):
            for part in config:
                armor_part = {
                    "name":part["name"],
                    "armor_level":part["armor_level"],
                    "durability_lose_speed":part["durability_lose_speed"],      #护甲耐久受到伤害后的消耗速度比率
                    "durability_max":part["durability_max"],
                    "durability":part["durability_max"],
                    "resistance":dict(part["resistance"]),
                }
                self.armor_part_list.append(armor_part)
        def _get_current_armor(self,harm_part):             #获取当前护甲部位
            for part in self.armor_part_list:
                if part["name"] == harm_part:
                    return part
            return None
        def _get_armor_resistance(self,harm_part,damage_type):        #获取当前护甲部位抗性
            armor = self._get_current_armor(harm_part)
            if armor is None:
                return 0
            resistance_value = armor["resistance"].get(damage_type,0)
            return resistance_value
        def _armor_restrain(self,harm,harm_part):                     #计算护甲免伤后的伤害
            armor = self._get_current_armor(harm_part)
            if armor is None:
                return harm
            pass
        def _get_current_body_part(self,harm_part):         #获取当前身体部位
            for part in self.body_part_list:
                if part["name"] == harm_part:
                    return part
            return None
        def _get_body_resistance(self,harm_part,damage_type):         #获取当前身体部位抗性
            body_part = self._get_current_body_part(harm_part)
            if body_part is None:
                return 0
            resistance_value = body_part["resistance"].get(damage_type,0)
            return resistance_value
        def _body_restrain(self,harm):                      #计算身体免伤后的伤害
            pass
        def _subtraction_armor(self,harm):                  #护甲损失上限方法
            pass
        def _armor_lose_durability(self,harm):              #护甲损失耐久方法
            pass
        def _subtraction_body_hp(self,harm):                #生命值损失上限方法
            pass
        def _new_armor(self,harm):                          #计算护甲剩余耐久
            pass
        def _new_body_part_hp(self,harm):                   #部位血量计算
            pass
        def _new_hp(self,harm,harm_type):                   #计算剩余血量
            pass
    class Buff:           #buff系统
        pass
    class Restrain:       #克制系统
        pass
    class Skill:          #技能系统
        pass
class Entity:             #实体系统
    class Interaction:    #交互系统
        pass
    class Position:       #定位系统
        pass
    class Owner:          #目标系统
        pass
    class Source:         #来源系统
        pass
    class Physics:        #物理系统
        class Collider:   #碰撞体
            pass
        class RigidBody:  #刚体
            pass
        class Raycast:    #射线检测
            pass
        class Collision:  #碰撞矩阵
            pass
        class Movement:   #移动系统
            pass
    class AI:             #AI系统
        pass
    class Item:           #物品系统
        pass
    class Inventory:      #仓库系统
        pass
class World:              #世界系统
    class Map:            #地图系统
        pass
    class Level:          #关卡系统
        pass
    class Environment:    #环境系统
        pass
class State:              #状态系统
    class Condition:      #状态检测
        pass
    class Health:         #健康
        pass
    class Down:           #倒地
        pass
    class Die:            #死亡
        pass
    class Soul:           #灵魂，观战系统
        pass
class Picture:            #画面系统
    class Animation:      #动画系统
        pass
    class Camera:         #摄像机
        pass
    class UI:             #UI系统
        pass
class Audio:              #音频系统
    pass
class Save:               #存档系统
    pass