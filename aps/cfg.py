from staticfg import CFGBuilder

cfg = CFGBuilder().build_from_file("example", "src/main.py")
cfg.build_visual("cfg_output", "png")