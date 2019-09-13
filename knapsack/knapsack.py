#!/usr/bin/python

import sys
from collections import namedtuple

# Additional Questions
# 1) Are there item(s) whose value is greater than the total value
# 2) Are there two items whose combined value is
#    less than another item of equal weight?
# 3) Assuming a normalized list sorted by some ideal output,
#    can I reduce my list enough to validate the solution accuracy?
# 4) Given two items with the same ratio, will the optimal solution
#    include both items, what cases will I want val > cost & vice versa


Item = namedtuple('Item', ['index', 'size', 'value'])

# Can I have two ratios that are the same?

# Get the ratio between value/cost
# sort by ratio >> create new sorted list
# loop over sorted ratios, adding to sack if current size + cost < total size
#   if current size + cost > total size, continue


def knapsack_solver(items, capacity):
    ratio_list = []
    max_item = {'index': 0, 'value': 0}
    total_size = 0
    total_value = 0
    leftover_items = []
    for item in items:
        total_size += item.size
        total_value += item.value

        if item.value > max_item['value']:
            max_item['value'] = item.value
            max_item['index'] = item.index

    for item in items:
        index, size, value = [*item]
        ratio = (item.value / item.size) \
            + (item.value / total_value) \
            - (item.size / total_size)

        new_item = {
            'index': index,
            'size': size,
            'value': value,
            'ratio': ratio
        }

        if len(ratio_list) == 0:
            ratio_list.append(new_item)
            continue

        for index, value in enumerate(ratio_list):
            if value['ratio'] <= new_item['ratio']:
                ratio_list.insert(index, new_item)
                break
            elif (index == (len(ratio_list) - 1)):
                ratio_list.append(new_item)
                break

    # {'Value': 197, 'Chosen': [1, 7, 8]}
    current_size = 0
    chosen_items = []
    # value = 0

    for item in ratio_list:
        if (current_size + item['size']) > capacity:
            leftover_items.append(item)
            continue
        chosen_items.append(item)
        # value += item['value']
        current_size += item['size']

        if current_size == capacity:
            break

    # if max_item['value'] > value and max_item['index']
    # is not in solution
    #   remove items from knapsack until max_item fits

    # For each leftover item
    for leftover in leftover_items:
        # print(leftover['index'])
        # loop through selected_items backwards to find two with equal size
        for i in range(len(chosen_items) - 1, -1, -1):
            # check this item against previous items for a match
            for j in range(i - 1, -1, -1):
                # print(chosen_items[i]['index'], chosen_items[j]['index'])
                combined_size = chosen_items[i]['size'] + chosen_items[j]['size']
                combined_value = chosen_items[i]['value'] + chosen_items[j]['value']
                # print(combined_size, leftover['size'])
                # if combined size is equiv to leftover size, combare value
                if combined_size == leftover['size']:
                    if combined_value < leftover['value']:
                        # remove two items, add one item worth more
                        pass

    # chosen_items.sort()
    return {'Value': value, 'Chosen': chosen_items}

if __name__ == '__main__':
  if len(sys.argv) > 1:
    capacity = int(sys.argv[2])
    file_location = sys.argv[1].strip()
    file_contents = open(file_location, 'r')
    items = []

    for line in file_contents.readlines():
      data = line.rstrip().split()
      items.append(Item(int(data[0]), int(data[1]), int(data[2])))

    file_contents.close()
    print(knapsack_solver(items, capacity))
  else:
    print('Usage: knapsack.py [filename] [capacity]')