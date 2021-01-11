def sort_quick_sort_method(group):
    if len(group) <= 1:
        return group
    pivot_value = group[len(group)//2]
    left_value = [x for x in group if x < pivot_value]
    middle_value = [x for x in group if x == pivot_value]
    right_value = [x for x in group if x > pivot_value]
    return sort_quick_sort_method(left_value) + middle_value + sort_quick_sort_method(right_value)

print(sort_quick_sort_method([4,9,18,11,3,2,0]))