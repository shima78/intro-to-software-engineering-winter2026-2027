def sum_values(numbers):
	total = sum(numbers)
	return total


def sum_and_append(numbers):
	total = sum(numbers)
	numbers.append(total)
	return total

my_numbers = [1, 2, 3, 4, 5]
result = sum_values(my_numbers)
print("Sum of 'sum_values':", result)  # Output: Sum of numbers: 15
print("Original list:", my_numbers)  # Output: Original list: [1, 2, 3, 4, 5]	

result = sum_and_append(my_numbers)
print("Sum of 'sum_and_append':", result)  # Output: Sum of numbers: 15
print("Modified list:", my_numbers)  # Output: Modified list: [1, 2, 3, 4, 5, 15]