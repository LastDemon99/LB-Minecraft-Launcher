current_max = 0

def set_status(status):
    print(status)

def set_progress(iteration, total, gui):
    percent = 100 * float(iteration / total)
    gui.updateProgressBar(int(percent), f'Progress: {"{0:.2f}".format(percent)}%')

    if iteration >= total:
        gui.updateProgressBar(100, 'Downloaded!')

def set_max(new_max: int):
    global current_max
    current_max = new_max