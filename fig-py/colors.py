from matplotlib.colors import LinearSegmentedColormap

red  = (0.86, 0.08, 0.24)
blue = (0.12, 0.56, 1.0)
dblue = (0.10, 0.10, 0.44)
purple = (0.49, 0.32, 0.62)
cyan = (0.0, 0.75, 0.75)
gold = (0.85, 0.65, 0.13)

uBlues = LinearSegmentedColormap.from_list("uBlues", [(1,1,1), blue])
uReds = LinearSegmentedColormap.from_list("uBlues", [(1,1,1), red])