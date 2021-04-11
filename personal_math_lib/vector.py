'''
v1 = [1,2,3]
v2 = [2,3,4]
v3 = [2,3,0]
v4 = [2,0]
s1 = 3
'''

def scalar_multiplication(vector, scalar) -> list:
	scaled_vector = []
	for i in range(len(vector)):
		scaled_vector.append(scalar * vector[i])
	return scaled_vector

def vector_addition(*args):
	size = len(args[0])
	result = [0 for x in range(size)]
	for i in range(len(args)):
		if size != len(args[i]):
			raise ValueError("Vectors must be same size for addition")
		for j in range(size):
			result[j] += args[i][j]
	return result


