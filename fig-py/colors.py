from matplotlib.colors import LinearSegmentedColormap

white  = (1.00, 1.00, 1.00)
red    = (0.86, 0.08, 0.24)
blue   = (0.12, 0.56, 1.0)
dblue  = (0.10, 0.10, 0.44)
purple = (0.49, 0.32, 0.62)
cyan   = (0.00, 0.75, 0.75)
gold   = (0.85, 0.65, 0.13)

uBlues = LinearSegmentedColormap.from_list("uBlues", [white, blue])
uReds = LinearSegmentedColormap.from_list("uBlues", [white, red])
bwr = LinearSegmentedColormap.from_list("ubwr", [(0.0, blue), (0.5, (1, 1, 1)), (1.0, red)])
wbr = LinearSegmentedColormap.from_list("uwbr", [(0.0, white), (0.5, blue), (1, red)])
wbrg = LinearSegmentedColormap.from_list("wbrg", [(0.0, white), (0.33, blue), (0.66, red), (1.0, gold)])
