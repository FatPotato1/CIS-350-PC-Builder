
#return whether selected gpu meets min and/or recommended gpu
def meets_requirements(selected_gpu, min_gpu, rec_gpu, rankings):

    selected = rankings.get(selected_gpu)
    min = rankings.get(min_gpu)
    rec = rankings.get(rec_gpu)

    if selected >= rec:
        return True,True

    if selected >= min:
        return True,False

    return False,False