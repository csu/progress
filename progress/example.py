from progress import Progress

p = Progress("data/", file_ext="md")
p.set_week("Hell World!\nI achieved things this week!")
p.get_week()