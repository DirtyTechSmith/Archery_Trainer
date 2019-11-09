import random

random_vals = []
random_weights = []

for x in range(10):
    random_val = random.uniform(0.0, 100.0)
    random_weight = random.random()
    random_vals.append(random_val)
    random_weights.append(random_weight)

print(random_vals)
print(random_weights)

my_choices = random.choices(random_vals,weights=random_weights)
print(my_choices)