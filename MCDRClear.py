# -*- coding: utf-8 -*-
from time import sleep

# 死亡标志位和循环运行时间标志位
deathFlag = 0
onRunFlag = 0
waitCleanTime = 0


# 循环
def on_load(server, old_module):
    global deathFlag
    global onRunFlag
    onRunFlag = 1
    server.say('§2[扫地] 自动清理掉落物已启动')
    server.logger.info('[扫地] 自动清理掉落物已启动')
    while True:
        if onRunFlag == 0:
            return False
        clean_wait(server)
        sleep(600)
        clean_wait(server)
        server.say('§2[扫地] §360 §2秒后清理掉落物')
        if onRunFlag == 0:
            return False
        clean_wait(server)
        sleep(40)
        clean_wait(server)
        server.say('§2[扫地] §320 §2秒后清理掉落物')
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


# 最大延迟数量为5，即25分钟
# 延迟扫地检测
def clean_wait(server):
    global deathFlag
    global waitCleanTime
    if deathFlag != 0:
        if deathFlag < 6:
            waitCleanTime = 300 * deathFlag
            deathFlag = 0
            server.say('§2[扫地] 已延迟扫地§3 ' + str(int(waitCleanTime / 60)) + ' §2分钟')
            sleep(waitCleanTime)
        if deathFlag > 5:
            waitCleanTime = 300 * 6
            deathFlag = 0
            server.say('§2[扫地] 已延迟扫地§3 ' + str(int(waitCleanTime / 60)) + ' §2分钟')
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
def on_info(server, info):
    global deathFlag
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
            server.say('§2[扫地] Hanbings 3219065882@qq.com 2020/4/11')
    if clear in tempInfo:
        if check_player_if_not_command(info):
            server.say('§2[扫地] 即将手动清理 §4警告：手动清理将不会影响自动清理')
            server.execute('kill @e[type = item]')
    if killText in tempInfo:
        if 'entities' in tempInfo:
            # [19:45:13] [Server thread/INFO]: Killed 2 entities
            ttTemp = tempInfo
            server.say('§2[扫地] 共清理 §4' + ttTemp[76: ttTemp.index('entities')] + '§2个掉落物')
    if noEntity in tempInfo:
        server.say('§2[扫地] §4没有任何掉落物被清理')
    if addFlag in tempInfo:
        if check_player_if_not_command(info):
            deathFlag = deathFlag + 1
            if deathFlag > 6:
                server.say('§4[扫地] 延迟最大时间为 25 分钟')
            else:
                server.say('§4[扫地] 已延迟清理' + ' ' + '现在已延迟的时间是：' + str(int((deathFlag * 300) / 60)) + '分钟')
    if aEgg in tempInfo:
        server.say('§2[扫地] 只清理了鸡蛋 QWQ')


# 判断指令是不是处于聊天语句最前方
def check_player_if_not_command(info):
    if str(info.content).index('!!clear') == 0:
        print(str(info.content).index('!!clear'))
        return True
    else:
        return False
