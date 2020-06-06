# -*- coding: utf-8 -*-
from time import sleep
import configparser
import os

# 死亡标志位和循环运行时间标志位
deathFlag = 0
onRunFlag = 0
waitCleanTime = 0


# 循环
def on_load(server, old_module):
    global deathFlag
    global onRunFlag
    # 检查配置文件
    check_config(server)
    # 获取 前缀 还有 提示
    prefix = str(get_prefix())
    _60sTips = str(get_60s_tips())
    _20sTips = str(get_20s_tips())
    clearTime = int(get_clear_time())
    # 获取运行状态
    onRunFlag = 1
    server.add_help_message('§2[扫地]', ' §5用!!clear或!!clear help查看详细帮助')
    server.say(prefix + '自动清理掉落物已启动')
    server.logger.info(prefix + '自动清理掉落物已启动')
    while True:
        if onRunFlag == 0:
            return False
        clean_wait(server)
        sleep(clearTime)
        clean_wait(server)
        server.say(prefix + _60sTips)
        if onRunFlag == 0:
            return False
        clean_wait(server)
        sleep(40)
        clean_wait(server)
        server.say(prefix + _20sTips)
        clean_wait(server)
        sleep(20)
        clean_wait(server)
        server.execute('kill @e[type = item]')
        if onRunFlag == 0:
            return False


# 关闭插件时运行标志位置0
def on_unload(server):
    global onRunFlag
    global deathFlag
    onRunFlag = 0
    deathFlag = 0
    server.logger.info('[扫地] 自动清理掉落物已关闭')


# 标记到标志位
def on_death_message(server, message):
    global deathFlag
    deathFlag = deathFlag + 1


# 延迟扫地检测
def clean_wait(server):
    global deathFlag
    global waitCleanTime
    # 前缀
    prefix = str(get_prefix())
    # 最大死亡次数 和 每次的等待时间
    maxDeathFlag = int(get_max_death_flag())
    waitTime = int(get_wait_time())
    if deathFlag != 0:
        if deathFlag < maxDeathFlag:
            waitCleanTime = waitTime * deathFlag
            deathFlag = 0
            server.say(prefix + '已延迟扫地§3 ' + str(int(waitCleanTime / 60)) + ' §2分钟')
            sleep(waitCleanTime)
        if deathFlag > maxDeathFlag - 1:
            waitCleanTime = waitTime * maxDeathFlag
            deathFlag = 0
            server.say(prefix + '已延迟扫地§3 ' + str(int(waitCleanTime / 60)) + ' §2分钟')
            sleep(waitCleanTime)


# 输出帮助
def print_helper(server):
    server.say('§2■■■■■■■■帮助列表■■■■■■■■')
    server.say('§2 !!clear help --帮助列表')
    server.say('§2 !!clear version --版本 ')
    server.say('§2 !!clear c --手动清理   ')
    server.say('§2 !!clear add --手动延迟清理时间')
    server.say('§2■■■■■■■■■■■■■■■■■■■■■   ')


# 手动清理
def on_user_info(server, info):
    global deathFlag
    prefix = str(get_prefix())
    maxDeathFlag = int(get_max_death_flag())
    waitTime = int(get_wait_time())
    tempInfo = str(info)
    clearHelp = '!!clear help'
    version = '!!clear version'
    clear = '!!clear c'
    addFlag = '!!clear add'
    killText = '[Server thread/INFO]: Killed'
    noEntity = '[Server thread/INFO]: No entity was found'
    aEgg = '[Server thread/INFO]: Killed Egg'
    tTemp = tempInfo
    if tTemp.endswith('!!clear') == True:
        if check_player_if_not_command(info):
            print_helper(server)
    if clearHelp in tempInfo:
        if check_player_if_not_command(info):
            print_helper(server)
    if version in tempInfo:
        if check_player_if_not_command(info):
            server.say(prefix + 'Hanbings 3219065882@qq.com 2020/6/6')
    if clear in tempInfo:
        if check_player_if_not_command(info):
            server.say(prefix + '即将手动清理 §4警告：手动清理将不会影响自动清理')
            server.execute('kill @e[type = item]')
    if killText in tempInfo:
        if 'entities' in tempInfo:
            # [19:45:13] [Server thread/INFO]: Killed 2 entities
            ttTemp = tempInfo
            server.say(prefix + '共清理 §4' + ttTemp[76: ttTemp.index('entities')] + '§2个掉落物')
    if noEntity in tempInfo:
        server.say(prefix + '§4没有任何掉落物被清理')
    if addFlag in tempInfo:
        if check_player_if_not_command(info):
            deathFlag = deathFlag + 1
            if deathFlag > maxDeathFlag:
                server.say(prefix + '延迟最大时间为 ' + str(maxDeathFlag * waitTime / 60) + ' 分钟')
            else:
                server.say(prefix + '已延迟清理' + ' ' + '现在已延迟的时间是：' + str(int((deathFlag * waitTime) / 60)) + '分钟')
    if aEgg in tempInfo:
        server.say(prefix + '只清理了鸡蛋 QWQ')


# 判断指令是不是处于聊天语句最前方
def check_player_if_not_command(info):
    if str(info.content).index('!!clear') == 0:
        return True
    else:
        return False


# 配置文件
def check_config(server):
    if not os.path.isfile("config/MCDRClear.ini"):
        f = open('config/MCDRClear.ini', 'w')
        server.logger.info('[MCDRClear] config/MCDRClear.ini 创建配置文件')
        config = configparser.ConfigParser()
        config.read("config/MCDRClear.ini")
        config_init(config, server)
        config.write(f)
        f.close()
    else:
        server.logger.info('[MCDRClear] config/MCDRClear.ini 配置文件已存在')
        f = open('config/MCDRClear.ini', 'r')
        config = configparser.ConfigParser()
        config.read("config/MCDRClear.ini")
        if not config.has_section("MCDRClear"):
            f = open('config/MCDRClear.ini', 'w')
            config_init(config, server)
            config.write(f)
            f.close()
        else:
            server.logger.info('[noPasswordLogin] config/MCDRClear.ini MCDRClear键已存在')
            f.close()


# 创建初始值
def config_init(config, server):
    server.logger.info('[MCDRClear] config/MCDRClear.ini 初始化配置文件')
    config.add_section("MCDRClear")
    config.set("MCDRClear", "prefix", "§2[扫地]")
    config.set("MCDRClear", "60sTips", "§360 §2秒后清理掉落物")
    config.set("MCDRClear", "20sTips", "§320 §2秒后清理掉落物")
    config.set("MCDRClear", "ClearTime", "600")
    config.set("MCDRClear", "MaxDeathFlag", "6")
    config.set("MCDRClear", "WaitTime", "300")

# 清理间隔
def get_clear_time():
    config = configparser.ConfigParser()
    config.read("config/MCDRClear.ini")
    return config.get("MCDRClear", "ClearTime")

# 获取最大等待次数
def get_max_death_flag():
    config = configparser.ConfigParser()
    config.read("config/MCDRClear.ini")
    return config.get("MCDRClear", "MaxDeathFlag")


# 获取最大等待时间
def get_wait_time():
    config = configparser.ConfigParser()
    config.read("config/MCDRClear.ini")
    return config.get("MCDRClear", "WaitTime")


# 获取前缀
def get_prefix():
    config = configparser.ConfigParser()
    config.read("config/MCDRClear.ini")
    return config.get("MCDRClear", "prefix") + ' '


# 获取60秒提示语句
def get_60s_tips():
    config = configparser.ConfigParser()
    config.read("config/MCDRClear.ini")
    return config.get("MCDRClear", "60sTips")


# 获取20秒提示语句
def get_20s_tips():
    config = configparser.ConfigParser()
    config.read("config/MCDRClear.ini")
    return config.get("MCDRClear", "20sTips")
