import cx_Freeze
import os

exes = [cx_Freeze.Executable("play.pyw")]

os.environ['TCL_LIBRARY'] = r'C:/Users/ChimengSoSo/AppData/Local/Programs/Python/Python36-32/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = r'C:/Users/ChimengSoSo/AppData/Local/Programs/Python/Python36-32/tcl/tk8.6'

cx_Freeze.setup(
    name = "CROSSING",
    options = {"build_exe":{"packages":["pygame"], 
               "include_files":[ "coin.png", "ghost1.png", "ghost2.png", "ghost3.png",
               "grave.png", "icon.png", "menu.png", "namegame.png", "player_crash.png",
               "player_drowned.png", "player_live.png", "raft1.png", "raft2.png",
               "small_bound.png", "stroller.png", "coin.wav", "crash.wav", "drown.wav",
               "level_up.wav", "sound_bg1.wav", "sound_bg2.wav", "walk.wav", "bg.png", "cart.wav", "g1.wav", "g2.wav", "g3.wav",
               "button_pass.wav", "count_down_pok.wav"]}},

    description = "Project Game for 204113",
    executables = exes
    )
