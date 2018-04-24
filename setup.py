import cx_Freeze
import os

exes = [cx_Freeze.Executable("main.py")]

os.environ['TCL_LIBRARY'] = r'C:/Users/ChimengSoSo/AppData/Local/Programs/Python/Python36-32/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = r'C:/Users/ChimengSoSo/AppData/Local/Programs/Python/Python36-32/tcl/tk8.6'

cx_Freeze.setup(
    name = "COSSING",
    options = {"build_exe":{"packages":["pygame"], 
               "include_files":[ "img/coin.png",
               "img/ghost1.png","img/ghost2.png","img/ghost3.png",
               "img/grave.png",
               "img/icon.png",
               "img/menu.png",
               "img/namegame.png",
               "img/player_crash.png",
               "img/player_drowned.png",
               "img/player_live.png",
               "img/raft1.png",
               "img/raft2.png",
               "img/small_bound.png",
               "img/stroller.png",
               "sound/coin.wav",
               "sound/crash.wav",
               "sound/drown.wav",
               "sound/level_up.wav",
               "sound/sound_bg1.wav",
               "sound/sound_bg2.wav",
               "sound/walk.wav", "img//bg.png"]}},

    description = "Project Game for 204113",
    executables = exes
    )
