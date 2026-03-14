import time
import asyncio

class Core:               #核心系统
    class Event:          #事件系统
        def __init__(self):
            self.listeners = {}                     #事件名 -> 回调函数列表
            self.logic_queue = []                   #逻辑队列，处理逻辑事件优先级
            self.render_queue = []                  #渲染队列，处理渲染事件优先级
            self.physics_queue = []                 #物理队列，处理物理事件优先级
            self.audio_queue = []                   #音频队列，处理音频事件优先级
            self.event_log = []                     #事件日志
        def on(self,event_name,callback):                          #订阅事件
            if event_name not in self.listeners:
                self.listeners[event_name] = []                     #定义键名
            self.listeners[event_name].append(callback)             #订阅者
        def off(self,event_name,callback=None):                     #取消订阅
            if callback is None:
                self.listeners.pop(event_name,None)                 #订阅者为空，删除事件键名
            else:
                if event_name in self.listeners:                    #多个订阅者，删除指定订阅者
                    self.listeners[event_name].remove(callback)
        def emit_logic(self,event_name,date=None):                  #逻辑事件
            self.logic_queue.append((event_name,date))
        def emit_render(self,event_name,date=None):                 #渲染事件
            self.render_queue.append((event_name,date))
        def emit_physics(self,event_name,date=None):                #物理事件
            self.physics_queue.append((event_name,date))
        def emit_audio(self,event_name,date=None):                  #逻辑事件
            self.audio_queue.append((event_name,date))
        async def _dispatch(self,event_name,date):                  #派送事件
            if event_name not in self.listeners:                    #无事件则返回
                return
            for callback in self.listeners[event_name]:             #有事件则判断
                if asyncio.iscoroutinefunction(callback):           #iscuroutinefunction为判断是否为携程函数！如果事件对应函数为协程，则传输协程方法值
                    await callback(date)
                else:
                    callback(date)                                  #如果不是协程函数，传输普通值
        async def process_logic(self):                              #逻辑事件处理优先级判断
            while self.logic_queue:
                event_name,date = self.logic_queue.pop(0)           #调取第一个事件同时删除第一个事件
                await self._dispatch(event_name,date)
        async def process_render(self):                             #渲染事件处理优先级判断
            while self.render_queue:
                event_name,date = self.render_queue.pop(0)
                await self._dispatch(event_name,date)
                await asyncio.sleep(0.016)                          #控制帧率为60帧
        async def process_physics(self):                            #物理事件处理优先级判断
            while self.physics_queue:
                event_name,date = self.physics_queue.pop(0)
                await self._dispatch(event_name,date)
                await asyncio.sleep(0.01)                           #控制帧率为100帧
        async def process_audio(self):                              #音频事件处理优先级判断
            while self.audio_queue:
                event_name,date = self.audio_queue.pop(0)
                await self._dispatch(event_name,date)
                await asyncio.sleep(0.033)                          #控制帧率为30帧
        async def _main_event(self):                                #事件同时发布方法
            while True:
                await asyncio.gather(
                    self.process_logic(),
                    self.process_render(),
                    self.process_physics(),
                    self.process_audio(),
                )
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
    class Optimization:   #优化系统
        class ObjectPool: #对象池
            pass
        class LOD:        #细节级别
            pass
        class Culling:    #剔除
            pass
        class Streaming:  #流式加载
            pass
    class Resource:       #资源系统
        class AssetManager:     #资源管理
            pass
        class Loader:           #加载器
            pass
        class Cache:            #缓存
            pass
        class Bundle:           #资源包
            pass
    class Network:
        def __init__(self):
            self.connections = []     #连接的客户端
            self.server = None        #服务器模式
            self.client = None        #客户端模式
        class Sync:                                    #同步系统
            def _sync_position(self,entity):           #同步位置
                pass
            def _sync_combat(self,damage_event):       #同步战斗
                pass
            def _sync_staste(self,state_change):       #同步状态
                pass
        class Room:                                    #房间系统
            def _create_room(self):                    #创建房间
                pass
            def _join_room(self):                      #加入房间
                pass
            def _leave_room(self):                     #离开房间
                pass
        class Protocol:                                #通信系统
            def _encode(self,data):                    #编码
                pass
            def _decode(self,data):                    #解码
                pass
        class Session:                                 #会话系统（处理ip验证）
            pass
class DevTools:           #开发工具
    class Console:        #控制台
        pass
    class Profiler:       #性能分析
        pass
    class Logger:         #日志
        pass
    class Cheat:          #作弊码
        pass
class Combat:             #战斗系统
    class Harm:           #伤害系统
        def __init__(self,core,harm_config=None,level_mode="permanent"):
            self.core = core
            core.Event.on("harm_raycast_ture",self._on_harm_raycast_ture)       #射线检测通过，伤害合法事件
            self.config = core.config
            self.motion_body_harm = 0               #动态身体伤害，类内储存
            self.motion_armor_harm = 0              #动态护甲伤害，类内储存
            self.level_mode = level_mode            #初始化时设定模式
            self.harm_level = 0 if level_mode == "temporary" else 1     #临时等级初始为零,永久等级初始为一
            self.permanent_level = None             #初始化永久等级
            self.level_buff = 1.0                   #等级增伤类内存储，初始值为1.0
            self.level_buff_dict = {}               #等级增伤字典
            self.harm_time = 0                      #伤害时间，类内储存
            self.level_start_time = None            #伤害等级开始时间
            self.level_end_time = 0                 #伤害等级超时后的降级时间
            self.harm_pace = 0                      #伤害频率，类内存储
            self.harm_type = []                     #伤害类型，类内存储
            self.target = None                      #治疗目标
            self.events = []                        #事件存储列表
            self.harm_log = []                      #日志
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
                    "harm_prep_time":harm["harm_prep_time"],                 #伤害预启动时间
                    "harm_persist_time":harm["harm_persist_time"],           #持续伤害间隔时间
                    "harm_time_max":harm["harm_time_max"],                   #伤害最大持续时间
                    "harm_level_max":harm["harm_level_max"],                 #伤害最大等级
                    "harm_level_time":harm["harm_level_time"],               #维持等级的时间
                    "harm_level_buff":dict(harm["harm_level_buff"]),         #每级对应的增伤数值,此处字典索引应该是数字，不是字符串
                    "harm_level_end_time":harm["harm_level_end_time"],       #等级超时后的等级持续时间
                    "harm_level_lose_number":harm["harm_level_lose_number"], #默认每次损失等级数
                    "harm_pace":harm["harm_pace"],                           #伤害频率，伤害次数
                    "harm_type":dict(harm["harm_type"])                      #伤害类型，此处为字典
                }
                self.harm_list.append(harm)
        def _on_harm_raycast_ture(self,data):                                #解包射线合法事件方法
            pass
        def _on_buff_change_mode(self,data):
            new_mode = data.get("level_mode")
            if new_mode in ["permanent","temporary"]:
                self.level_mode = new_mode
                if new_mode == "temporary":
                    self.harm_level = 0
                    self.level_start_time = time.time()
                else:
                    pass
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
        def _get_harm_prep_time(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_prep_time")
        def _get_harm_persist_time(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_persist_time")
        def _get_harm_time_max(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_time_max")
        def _get_harm_pace(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_pace")
        def _get_harm_type(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_type")
        def _get_harm_level_max(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_level_max")
        def _get_harm_level_time(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_level_time")
        def _get_harm_level_buff(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_level_buff")
        def _get_harm_level_end_time(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_level_end_time")
        def _get_harm_level_lose_number(self,harm_name):
            return self._get_harm_attr(harm_name,"harm_level_lose_number")
        def _get_current_level(self,harm_name):                 #获取当前等级
            if self.level_mode == "permanent":
                if self.permanent_level is not None:
                    self.harm_level = self.permanent_level          #配置可设计当前伤害等
                    return self.harm_level
                else:
                    self.harm_level = self._get_harm_level_max(harm_name)
                    return self.harm_level
            else:
                return self._get_temp_level(harm_name)
        def _add_level(self,harm_name,level_event_number):                      #改变等级方法
            harm_level_max = self._get_harm_level_max(harm_name)
            old_level = self.harm_level
            self.harm_level = min(self.harm_level + level_event_number,harm_level_max)
            if self.harm_level < 0:
                self.harm_level = 0
            if self.harm_level != old_level:
                self.level_buff = self.level_buff_dict.get(self.harm_level,1.0)
            self.level_start_time = time.time()      #重置计时
        def _get_temp_level(self,harm_name):                                 #获取当前临时等级
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
            old_level = self.harm_level
            if self.harm_level <= 0:
                return 0
            elapsed_time = time.time() - self.level_start_time
            levels_to_lose = int(elapsed_time / harm_level_end_time) * harm_level_lose_number           #默认过一定时间降x级
            self.harm_level = max(0,self.harm_level - levels_to_lose)
            if self.harm_level != old_level:
                self.level_buff = self.level_buff_dict.get(self.harm_level,1.0)
            if self.harm_level > 0:
                self.level_start_time = time.time()
            else:
                self.level_start_time = None
            return self.harm_level
        def _level_buff(self,harm_name):        #等级增伤公式
            self.level_buff_dict = self._get_harm_level_buff(harm_name)
            level = self.harm_level
            level_buff = self.level_buff_dict.get(level,1.0)
            self.level_buff = level * level_buff
        def _get_current_level_buff(self):        #获取当前等级增伤
            return self.level_buff
        def _output_harm(self,harm_name):      #输出伤害
            armor_harm_value = self._get_armor_harm_value(harm_name)
            body_harm_value = self._get_body_harm_value(harm_name)
            armor_harm = armor_harm_value * self.harm_level
            body_harm = body_harm_value * self.harm_level
            result = {
                "armor_harm":armor_harm,
                "body_harm":body_harm,
            }
            return result
        def _start_heal(self,harm_name,target,harm_part):     #治疗，持续伤害事件
            self.target = target
            heal_value = self._get_body_harm_value(harm_name) * (-1)
            damage_time = time.time()
            self.core.Event.emit_logic("heal_started",{
                "target":target,
                "heal_id":id(self),
                "heal_value": heal_value,
                "heal_prep_time": self._get_harm_prep_time(harm_name),
                "heal_persist_time": self._get_harm_persist_time(harm_name),
                "heal_time_max": self._get_harm_time_max(harm_name),
                "harm_part": harm_part,
            })
            self.harm_log.append(f"{target}的{harm_name}在{damage_time}时受到治疗(持续伤害)")
        def _harm_event(self,harm_name,target,harm_part):         #伤害事件
            self.target = target
            damage_time = time.time()
            self.core.Event.emit_logic("harm_output",{
                "harm_name":harm_name,
                "target":target,
                "current_level":self._get_current_level(harm_name),
                "output_harm":self._output_harm(harm_name),
                "harm_type":self._get_harm_type(harm_name),
                "harm_part": harm_part,
                "timestamp":time.time(),
            })
            self.harm_log.append(f"{target}的{harm_name}在{damage_time}时受到伤害(瞬时伤害)")
        def _get_log(self,last_n=None):          #获取日志，last_n表示只取最后几条
            if last_n:
                return self.harm_log[-last_n:]
            return self.harm_log
        def _clear_log(self):                    #清空日志
            self.harm_log = []
        def _get_output_dict(self,harm_name):    #输出集合
            return {
                "harm_name":harm_name,
                "current_level":self._get_current_level(harm_name),
                "output_harm":self._output_harm(harm_name),
                "harm_type":self._get_harm_type(harm_name),
                "timestamp":time.time(),
            }
    class HP:             #血量系统
        def __init__(self,core,max_hp,armor,armor_durability_max,body_part_config=None,armor_part_config=None,owner_type="character",source_type="name"):
            self.core = core
            core.Event.on("harm_output",self._on_harm_output)    #订阅伤害输出事件
            self.config = core.config
            self.max_hp = max_hp                                 #血量上限
            self.hp = max_hp                                     #当前血量
            self.armor = armor                                   #当前护甲
            self.armor_level = 0                                 #护甲等级
            self.cached_armor_resistance = {}                    #护甲抗性缓存器
            self.cached_armor_really_rate = {}                   #护甲真实抗性缓存器
            self.cached_armor_to_body = {}                       #护甲防护后对伤害的减伤比例缓存器
            self.cached_armor_to_type = {}                       #护甲防护后对特定类型伤害比例缓存器
            self.cached_body_part_resistance = {}                #身体部位抗性缓存器
            self.cached_body_part_HP = {}                        #身体部位血量缓存器
            self.cached_body_part_HP_max = {}                    #身体部位血量上限缓存器
            self.cached_body_part_HP_max_cost = {}               #身体部位血量上限惩罚缓存器
            self.armor_durability_max = armor_durability_max     #护甲上限
            self.cached_armor_durability = {}                    #护甲当前耐久缓存
            self.owner_type = owner_type                         #目标
            self.source_type = source_type                       #来源
            self.treat_log = []                                  #日志
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
                    "name":part["name"],                                       #部位名字
                    "hp_max":part["hp_max"],                                   #最大血量
                    "hp":part["hp_max"],                                       #当前血量
                    "hp_max_cost":dict(part["hp_max_cost"]),                   #部位完全损伤后带来的血量上限惩罚
                    "resistance":dict(part["resistance"]),                     #抗性值
                }
                self.body_part_list.append(body_part)
        def _init_amor_parts(self,config):
            for part in config:
                armor_part = {
                    "name":part["name"],                                               #部位名字
                    "armor_level":part["armor_level"],                                 #护甲等级
                    "armor_resistance_really":{
                        int(harm_level):rate
                        for harm_level,rate in part["armor_resistance_rate"].items()                            #获取护甲真实抗性比例
                    },
                    "armor_resistance_to_body":{
                        int(harm_level):rate
                        for harm_level,rate in part["armor_resistance_to_body"].items()                         #获取护甲部位对身体减伤
                    },
                    "armor_resistance_to_body_type_rate":dict(part["armor_resistance_to_body_type_rate"]),      #获取特定伤害抗性比例
                    "durability_lose_speed":part["durability_lose_speed"],             #护甲耐久受到伤害后的消耗速度比率
                    "durability_max":part["durability_max"],                           #最大耐久
                    "durability":part["durability_max"],                               #初始耐久
                    "resistance":dict(part["resistance"]),                             #抗性值
                }
                self.armor_part_list.append(armor_part)
        def _on_harm_output(self,data):                     #解包伤害输出事件方法
            harm_part = data["harm_part"]
            armor_harm = data["output_harm"].get("armor_harm",0)
            body_harm = data["output_harm"].get("body_harm",0)
            harm_level = data.get("current_level",0)
            damage_type = data["damage_type"]
            armor_level = self._get_amor_level(harm_part)
            self._armor_lose_durability(armor_harm,harm_part,damage_type,harm_level,armor_level)
            self._new_body_part_hp(body_harm,harm_part,damage_type,harm_level,armor_level)
        def _get_current_armor(self,harm_part):             #获取当前护甲部位
            for part in self.armor_part_list:
                if part["name"] == harm_part:
                    return part
            return None
        def _get_amor_level(self,harm_part):                #获取当前护甲等级
            armor = self._get_current_armor(harm_part)
            armor_level = armor["armor_level"]
            self.armor_level = armor_level
            return armor_level
        def _get_armor_resistance(self,harm_part,damage_type):        #获取当前护甲部位抗性
            cache_key = f"{harm_part}_{damage_type}"
            if cache_key in self.cached_armor_resistance:
                return self.cached_armor_resistance[cache_key]
            armor = self._get_current_armor(harm_part)
            if armor is None:
                return 0
            resistance_value = armor["resistance"].get(damage_type,0)
            self.cached_armor_resistance[cache_key] = resistance_value
            return resistance_value
        def _get_armor_resistance_really_rate(self,harm_part,armor_level,harm_level):  #获取真实部位护甲减伤比例
            cache_key = f"{harm_part}_{armor_level}_{harm_level}"                      #定义键名
            if cache_key in self.cached_armor_really_rate:
                return self.cached_armor_really_rate[cache_key]                        #假如存在，调用类缓存
            armor = self._get_current_armor(harm_part)                                 #不存在，访问配置
            if armor is None:
                return 0.0
            rate = armor["armor_resistance_really"].get(harm_level,0.0)                #获取对应比例
            self.cached_armor_really_rate[cache_key] = rate                            #存储对应部位减伤
            return rate
        def _get_armor_resistance_to_body(self,harm_part,armor_level,harm_level):      #护甲减伤后对身体伤害时的抗性
            cache_key = f"{harm_part}_{armor_level}_{harm_level}"
            if cache_key in self.cached_armor_to_body:
                return self.cached_armor_to_body[cache_key]
            armor = self._get_current_armor(harm_part)
            if armor is None:
                return 0.0
            armor_to_body = armor["armor_resistance_to_body"].get(harm_level,0.0)
            self.cached_armor_to_body[cache_key] = armor_to_body
            return armor_to_body
        def _get_armor_resistance_to_body_type_rate(self,harm_part,armor_level,damage_type):    #护甲减伤的真实比例
            cache_key = f"{harm_part}_{armor_level}_{damage_type}"
            if cache_key in self.cached_armor_to_type:
                return self.cached_armor_to_type[cache_key]
            armor = self._get_current_armor(harm_part)
            if armor is None:
                return 0.0
            type_resistance = armor["armor_resistance_to_body_type_rate"].get(damage_type,0.0)
            self.cached_armor_to_type[cache_key] = type_resistance
            return type_resistance
        def _armor_lose_durability(self,armor_harm,harm_part,damage_type,armor_level,harm_level):       #计算护甲耐久受到的的伤害
            cache_key_resistance = f"{harm_part}_{damage_type}"
            cache_key_rate = f"{harm_part}_{armor_level}_{harm_level}"
            armor = self._get_current_armor(harm_part)
            if armor is None:
                return armor_harm
            base_resistance = self.cached_armor_resistance.get(cache_key_resistance,0)
            really_rate = self.cached_armor_really_rate.get(cache_key_rate,0)
            armor_damage = armor_harm * (1 - base_resistance * really_rate)
            armor["durability"] = max(0,armor["durability"] - armor_damage)
            self.cached_armor_durability[f"{harm_part}_{armor_level}"] = armor["durability"]
            """事件触发"""
            #护甲归零事件
            if armor["durability"] <= 0:
                self.core.Event.emit_logic("armor_broken",{
                    "armor_part": harm_part,
                    "owner": self.owner_type,
                })
            return armor_damage
        def _subtraction_armor(self):                  #护甲损失上限方法
            pass
        def _after_armor_to_body_harm(self,body_harm,harm_part,armor_level,harm_level,damage_type):        #护甲减伤后对身体的伤害
            armor = self._get_current_armor(harm_part)
            if armor is None:
                return body_harm
            armor_to_body = self._get_armor_resistance_to_body(harm_part,armor_level,harm_level)
            resistance_type = self._get_armor_resistance_to_body_type_rate(harm_part,armor_level,damage_type)
            new_body_harm = body_harm * (1 - armor_to_body*resistance_type)
            return new_body_harm
        def _get_current_body_part(self,harm_part):         #获取当前身体部位
            for part in self.body_part_list:
                if part["name"] == harm_part:
                    return part
            return None
        def _get_body_resistance(self,harm_part,damage_type):         #获取当前身体部位抗性
            cache_key = f"{harm_part}_{damage_type}"
            if cache_key in self.cached_body_part_resistance:
                return self.cached_body_part_resistance[cache_key]
            body_part = self._get_current_body_part(harm_part)
            if body_part is None:
                return 0
            resistance_value = body_part["resistance"].get(damage_type,0)
            self.cached_body_part_resistance[cache_key] = resistance_value
            return resistance_value

        def _to_body_harm(self,body_harm,harm_part,armor_level,harm_level,damage_type):                      #计算身体免伤后的伤害
            current_body_harm = self._after_armor_to_body_harm(body_harm,harm_part,armor_level,harm_level,damage_type)
            body_resistance = self._get_body_resistance(body_harm,damage_type)
            new_body_harm = current_body_harm * (1 - body_resistance)
            return new_body_harm
        def _new_body_part_hp(self,body_harm,harm_part,armor_level,harm_level,damage_type):                   #血量计算
            final_damage = self._to_body_harm(
                body_harm,harm_part,armor_level,harm_level,damage_type       #取得伤害值
            )
            body_part = self._get_current_body_part(harm_part)               #获取身体部位
            if body_part is None:
                return self.hp
            cache_key = f"{harm_part}"                                       #定义键名
            if cache_key in self.cached_body_part_HP:
                old_hp = self.cached_body_part_HP[cache_key]                 #获取部位血量
            else:
                old_hp = body_part["hp"]                                     #如果为空，从配置取值
                self.cached_body_part_HP[cache_key] = old_hp
            if final_damage >= old_hp:                                       #判断是否伤害溢出
                overflow = final_damage - old_hp                             #溢出伤害
                new_hp = 0                                                   #部位血量
                damage_to_main = old_hp                                      #原本伤害
            else:
                overflow = 0                                                 #溢出为零
                new_hp = old_hp - final_damage                               #部位不为零
                damage_to_main = final_damage                                #原本伤害
            self.cached_body_part_HP[cache_key] = new_hp                     #更新存值
            body_part["hp"] = new_hp
            self.hp = max(0,self.hp - damage_to_main - overflow)             #判断边界
            self.hp = min(self.hp,self.max_hp)
            if new_hp <= 0:
                #部位血量归零事件
                self.core.Event.emit_logic("body_part_broken",{
                    "body_part": harm_part,
                    "owner": self.owner_type,
                    "overflow": overflow,
                })
                self._subtraction_body_hp(harm_part)                          #引用损失上限惩罚方法
            if self.hp <= 0:
                #倒地事件
                self.core.Event.emit_logic("owner_down",{
                    "owner":self.owner_type,
                })
            return {
                "part_damage": damage_to_main,
                "overflow": overflow,
                "new_part_hp": new_hp,
                "new_main_hp": self.hp,
            }
        def _subtraction_body_hp(self,harm_part):                                #生命值随部位损失上限方法
            cache_key = f"{harm_part}"                                           #定义键名
            body_part = self._get_current_body_part(harm_part)
            if cache_key in self.cached_body_part_HP_max:                        #取值部位现存HP
                old_hp_max = self.cached_body_part_HP_max[cache_key]
            else:
                old_hp_max = harm_part["hp_max"]
                self.cached_body_part_HP_max[cache_key] = old_hp_max
            if cache_key in self.cached_body_part_HP_max_cost:                   #取值部位受伤惩罚值
                hp_max_cost = self.cached_body_part_HP_max_cost[cache_key]
            else:
                hp_max_cost = body_part["hp_max_cost"]
                self.cached_body_part_HP_max_cost[cache_key] = hp_max_cost
            new_hp_max = max(0,old_hp_max - hp_max_cost)                         #扣除血量上限逻辑
            self.cached_body_part_HP_max[cache_key] = new_hp_max                 #类内缓存
            self.hp_max = max(1,self.max_hp - hp_max_cost)                       #主体血量上限更新
            self.hp = min(self.hp,self.max_hp)
            self.treat_log.append(f"部位{harm_part}受损，血量上限-{hp_max_cost}")    #日志
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
        def __init__(self,x=0, y=0,z=0):
            self.x = x                           #横位置
            self.y = y                           #纵位置
            self.z = z                           #高位置
            self.last_x = x                      #上一帧横位置
            self.last_y = y                      #上一帧纵位置
            self.last_z = z                      #上一帧高位置
            self.velocity_x = 0                  #横速度
            self.velocity_y = 0                  #纵速度
            self.velocity_z = 0                  #高速度
            self.last_update =time.time()        #上一帧时间
            self.owner = None                    #目标
        def _distance_to(self,other):                      #3D位置计算
            dx = self.x - other.x
            dy = self.y - other.y
            dz = self.z - other.z
            return (dx**2 + dy**2 + dz**2)**0.5
        def _flat_distance_to(self,other):                 #2D位置计算
            dx = self.x - other.x
            dy = self.y - other.y
            return (dx**2 + dy**2)**0.5
        def _update(self,new_x,new_y,new_z):               #更新位置
            self.last_x, self.last_y, self.last_z = self.x, self.y, self.z
            self.x, self.y, self.z = new_x, new_y, new_z
            now = time.time()
            gap = now - self.last_update
            if gap > 0:
                self.velocity_x = (self.x - self.last_x) / gap
                self.velocity_y = (self.y - self.last_y) / gap
                self.velocity_z = (self.z - self.last_z) / gap
            self.last_update = now
        def _predict_position(self,delta_time):             #预测未来位置
            future_x = self.x + delta_time * self.velocity_x
            future_y = self.y + delta_time * self.velocity_y
            future_z = self.z + delta_time * self.velocity_z
            return future_x,future_y,future_z
        def _get_movement_direction(self):                   #获取移动方向
            speed = (self.velocity_x**2 + self.velocity_y**2 + self.velocity_z**2)**0.5
            if speed == 0:
                return 0,0,0
            return self.velocity_x/speed, self.velocity_y/speed, self.velocity_z/speed
    class Owner:          #目标系统
        pass
    class Source:         #来源系统
        pass
    class Physics:        #物理系统
        class Collider:   #碰撞体
            pass
        class RigidBody:  #刚体
            pass
        class SoftBody:   #软体
            pass
        class Cloth:      #布料
            pass
        class Vehicle:    #载具
            pass
        class Raycast:    #射线检测
            pass
        class Melee:      #近战
            pass
        class Grenade:    #手雷，抛物线
            pass
        class AOE:        #范围攻击
            pass
        class Collision:  #碰撞矩阵
            pass
        class Movement:   #移动系统
            pass
    class AI:             #AI系统
        class PathFinding:      #寻路
            pass
        class Decision:         #决策
            pass
        class BehaviorTree:     #行为树
            pass
        class Leaning:          #学习
            pass
    class Item:           #物品系统
        pass
    class Inventory:      #仓库系统
        pass
class Quest:              #任务系统
    class Story:          #主线
        pass
    class Side:           #支线
        pass
    class Dialogue:       #对话树
        pass
    class Choice:         #选择影响
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
    class Healing:        #打药状态
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