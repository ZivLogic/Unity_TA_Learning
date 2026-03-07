class Core:               #核心系统
    class Event:          #事件系统
        pass
    class Time:           #时间系统
        pass
    class Config:         #配置系统
        pass
    class Input:          #输入系统
        pass
    class Output:
        pass
    class Factory:
        pass
class Combat:             #战斗系统
    class Harm:           #伤害系统
        pass
    class HP:             #血量系统
        pass
    class Buff:           #buff系统
        pass
    class Restrain:       #克制系统
        pass
    class Skill:          #技能系统
        pass
class Entity:             #实体系统
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
        class Movement:   # 移动系统
            pass
    class AI:             #AI系统
        pass
    class Item:           #物品系统
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