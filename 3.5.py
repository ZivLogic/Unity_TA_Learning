class Harm:
    def __init__(self,harm_value,harm_time,harm_level):
        #统一伤害属性，做解耦
        self.harm_value = harm_value #基础伤害值
        self.harm_time = harm_time   #伤害时间
        self.harm_level = harm_level #伤害等级最大上限
        self.current_level = 0       #初始等级
    def add_level(self,level):
        #等级增加方法
        self.current_level = min(self.current_level+level,self.harm_level)
        return self.current_level
    def get_current_level(self):
        #当前等级
        return self.current_level
    def burn_persistent_harm(self):
        #火焰灼烧伤害方法
        burn_persistent_harm = self.harm_value * self.get_current_level()
        return burn_persistent_harm
    def projectile_frequency(self):
        #这里巧用等级方法代替弹射次数，解耦复用
        projectile_frequency = self.harm_level + 1 - self.get_current_level()
        return projectile_frequency
    def projectile_harm(self):
        #弹射伤害方法
        i = 1
        if self.projectile_frequency() == self.harm_level:
            i = 1
        elif self.projectile_frequency() < self.harm_level:
            i = 0.3
        else:
            i = 0.1
        projectile_harm = self.harm_value * i
        return projectile_harm
class HP:
    def __init__(self,armor,physics_resistance,magic_resistance,hp,body_part):
        self.armor = armor                           #护甲值
        self.physics_resistance = physics_resistance #物理伤害抗性
        self.magic_resistance = magic_resistance     #魔法伤害抗性
        self.hp = hp                                 #角色最大血量
        self.body_part = body_part                   #角色可受击部位
        self.new_hp = 0                              #角色当前血量
    def harm_calculate(self,harm,harm_type):
        #当前血量计算
        physics = 1
        magic = 2
        physics_and_magic = 3
        if harm_type == physics:
            self.new_hp = (self.hp + self.armor) * (self.physics_resistance + 1) - harm
            self.condition_down()
            return self.new_hp
        elif harm_type == magic:
            self.new_hp = (self.hp + self.armor) * (self.magic_resistance + 1) - harm
            self.condition_down()
            return self.new_hp
        elif harm_type == physics_and_magic:
            self.new_hp = (self.hp + self.armor) * (self.physics_resistance + 1) * (self.magic_resistance + 1) - harm
            self.condition_down()
            return self.new_hp
        else:
            self.new_hp = self.hp
            self.condition_down()
            return self.new_hp
    def get_new_hp(self):
        #获取当前血量
        return self.new_hp
    def condition_down(self):
        if self.get_new_hp() <= 0:
            #发布倒地事件
            self.down_event()
        elif self.get_new_hp() == self.hp:
            #这里是一个逻辑错误！护甲不应该满血清零！是我考虑欠缺了！
            self.armor = 0
    def down_event(self):
        #倒地方法
        pass
    def save_initial(self):
        #队友救援后的初始状态
        new_hp = self.hp * 0.2
        return new_hp
class Health:
    def __init__(self,name):
        self.name = name
    def condition(self):
        #我想把这里做成一个中转站，比如说健康状态下应该有什么样的血量，可以进行什么样的操作（放技能，开枪，奔跑），什么样的界面ui，主要是在每一个系统后面都一个一个引用太麻烦了，不如改成只引用Health.condition()，就简单很多。
        pass