from typing import KeysView


r = [{"key": "a", "value": 1},  {"key": "b", "value": 2}]
def extractor(item):
  return item.get('value', 0)

r.sort(reverse=True, key=extractor)
print(r)