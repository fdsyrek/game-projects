import numpy as np

b = np.arange(1,10)


def one_row():
	a = np.zeros((9,9))
	np.random.shuffle(b)
	np.copyto(a[0,:],b)
	return a

def first_square(a):
	alreadyThere = []
	for x in range(0,3):
		alreadyThere += [a[0,x]]

	exclusion = np.setdiff1d(b, alreadyThere)
	np.random.shuffle(exclusion)
	np.copyto(a[1,:3], exclusion[:3])
	np.copyto(a[2,:3], exclusion[3:])

	return a

def second_square(a):
	alreadyThere = []
	row_one = []
	row_two = []
	for x in range(0,3):
		alreadyThere += [a[0,x+3]]
		row_one += [a[1,x]]
		row_two += [a[2,x]]
	exclusion = np.setdiff1d(b, alreadyThere)
	row_one_needs = np.intersect1d(exclusion, row_two)
	row_one_can = np.setdiff1d(exclusion, row_one)
	no_overlap = np.setdiff1d(row_one_can,row_one_needs)
	np.random.shuffle(no_overlap)
	row_one_list = np.hstack((row_one_needs, no_overlap))
	new_row_one = row_one_list[:3]
	new_row_two = np.setdiff1d(exclusion, new_row_one)
	np.random.shuffle(new_row_one)
	np.random.shuffle(new_row_two)
	np.copyto(a[1,3:6],new_row_one)
	np.copyto(a[2,3:6],new_row_two)
	return a

def third_square(a):
	row_one = []
	row_two = []
	for x in range(0,6):
		row_one += [a[1,x]]
		row_two += [a[2,x]]
	row_one_needs = np.setdiff1d(b,row_one)
	row_two_needs = np.setdiff1d(b,row_two)
	np.random.shuffle(row_one_needs)
	np.random.shuffle(row_two_needs)
	np.copyto(a[1,6:],row_one_needs)
	np.copyto(a[2,6:], row_two_needs)
	return a

def fourth_square(a):
	col_1 = []
	col_2 = []
	col_3 = []
	for x in range(0,3):
		col_1 += [a[x,0]]
		col_2 += [a[x,1]]
		col_3 += [a[x,2]]

	col_one_options = np.setdiff1d(b,col_1)
	np.random.shuffle(col_one_options)
	new_col_one = col_one_options[:3]
	np.copyto(a[3:6,0],new_col_one)
	exclusion = np.setdiff1d(b,new_col_one)
	col_2_need = np.intersect1d(exclusion, col_3)
	col_2_options = np.setdiff1d(exclusion, col_2)
	no_overlap = np.setdiff1d(col_2_options, col_2_need)
	np.random.shuffle(no_overlap)
	long_col_two = np.hstack((col_2_need, no_overlap))
	new_col_two = long_col_two[:3]
	np.random.shuffle(new_col_two)
	np.copyto(a[3:6,1], new_col_two)
	exclusion2 = np.setdiff1d(exclusion, new_col_two)
	np.random.shuffle(exclusion2)
	np.copyto(a[3:6,2],exclusion2)
	return a

def fifth_square(a):
	col_1 = []
	col_2 = []
	col_3 = []
	for x in range(0,6):
		col_1 += [a[x,0]]
		col_2 += [a[x,1]]
		col_3 += [a[x,2]]

	new_col_one = np.setdiff1d(b, col_1)
	new_col_two = np.setdiff1d(b, col_2)
	new_col_three = np.setdiff1d(b, col_3)
	np.random.shuffle(new_col_one)
	np.random.shuffle(new_col_two)
	np.random.shuffle(new_col_three)
	np.copyto(a[6:,0],new_col_one)
	np.copyto(a[6:,1],new_col_two)
	np.copyto(a[6:,2], new_col_three)
	return a

def middle_square(a):
	col_1 = []
	col_2 = []
	col_3 = []
	row_1 = []
	row_2 = []
	row_3 = []
	for x in range(0,3):
		col_1 += [a[x,3]]
		col_2 += [a[x,4]]
		col_3 += [a[x,5]]
		row_1 += [a[3,x]]
		row_2 += [a[4,x]]
		row_3 += [a[5,x]]
	tile_1_no = np.union1d(col_1, row_1)
	tile_1_options = np.setdiff1d(b,tile_1_no)
	np.random.shuffle(tile_1_options)
	a[3,3] = tile_1_options[0]
	exclusion = np.setdiff1d(b,tile_1_options[0])
	tile_2_no = np.union1d(col_2, row_1)
	tile_2_options = np.setdiff1d(exclusion, tile_2_no)
	np.random.shuffle(tile_2_options)
	a[3,4] = tile_2_options[0]
	exclusion = np.setdiff1d(exclusion, tile_2_options[0])
	tile_3_no = np.union1d(col_3,row_1)
	tile_3_options = np.setdiff1d(exclusion, tile_3_no)
	a[3,5] = tile_3_options[0]
	exclusion = np.setdiff1d(exclusion, tile_3_options[0])
	row_2_needs = np.intersect1d(exclusion, row_3)
	row_2_can = np.setdiff1d(exclusion, row_2)
	no_collides = np.setdiff1d(row_2_can, row_2_needs)
	np.random.shuffle(no_collides)
	long_row_2 = np.hstack((row_2_needs,no_collides))
	new_row_two = long_row_2[:3]
	np.random.shuffle(new_row_two)
	count = 0
	while(new_row_two[0] in col_1 or new_row_two[1] in col_2 or new_row_two[2] in col_3):
		np.random.shuffle(new_row_two)
		count +=1
		if count >=10:
			return middle_square(fifth_square(fourth_square(third_square(second_square(first_square(one_row()))))))
	np.copyto(a[4,3:6], new_row_two)
	last_three = np.setdiff1d(exclusion, new_row_two)
	np.random.shuffle(last_three)
	count = 0
	while(last_three[0] in col_1 or last_three[1] in col_2 or last_three[2] in col_3):
		np.random.shuffle(last_three)
		count+=1
		if count >=10:
			return middle_square(fifth_square(fourth_square(third_square(second_square(first_square(one_row()))))))
	np.copyto(a[5,3:6], last_three)
	return a

def seventh_square(a):
	col_1 = []
	col_2 = []
	col_3 = []
	row_1 = []
	row_2 = []
	row_3 = []
	for x in range(0,3):
		col_1 += [a[x,6]]
		col_2 += [a[x,7]]
		col_3 += [a[x,8]]
		row_1 += [a[3,x]]
		row_2 += [a[4,x]]
		row_3 += [a[5,x]]
	for x in range(3,6):
		row_1 += [a[3,x]]
		row_2 += [a[4,x]]
		row_3 += [a[5,x]]
	row_1_needs = np.setdiff1d(b,row_1)
	row_2_needs = np.setdiff1d(b,row_2)
	row_3_needs = np.setdiff1d(b,row_3)
	np.random.shuffle(row_1_needs)
	np.random.shuffle(row_2_needs)
	np.random.shuffle(row_3_needs)
	count = 0
	while(row_1_needs[0] in col_1 or row_1_needs[1] in col_2 or row_1_needs[2] in col_3 ):
		np.random.shuffle(row_1_needs)
		count+=1
		if count >=10:
			return seventh_square(middle_square(fifth_square(fourth_square(third_square(second_square(first_square(one_row())))))))
	np.copyto(a[3,6:],row_1_needs)
	count = 0
	while(row_2_needs[0] in col_1 or row_2_needs[1] in col_2 or row_2_needs[2] in col_3):
		np.random.shuffle(row_2_needs)
		count+=1
		if count >=10:
			return seventh_square(middle_square(fifth_square(fourth_square(third_square(second_square(first_square(one_row())))))))
	np.copyto(a[4,6:],row_2_needs)
	count = 0
	while(row_3_needs[0] in col_1 or row_3_needs[1] in col_2 or row_3_needs[2] in col_3):
		np.random.shuffle(row_3_needs)
		count+=1
		if count >=10:
			return seventh_square(middle_square(fifth_square(fourth_square(third_square(second_square(first_square(one_row())))))))
	np.copyto(a[5,6:],row_3_needs)
	return a



def ocho(a):
	col_1 = []
	col_2 = []
	col_3 = []
	for x in range(0,6):
		col_1 += [a[x,3]]
		col_2 += [a[x,4]]
		col_3 += [a[x,5]]
	row_1 = []
	row_2 = []
	row_3 = []
	for x in range(0,3):
		row_1 += [a[6,x]]
		row_2 += [a[7,x]]
		row_3 += [a[8,x]]

	new_col_1 = np.setdiff1d(b,col_1)
	new_col_2 = np.setdiff1d(b, col_2)
	new_col_3 = np.setdiff1d(b, col_3)

	np.random.shuffle(new_col_1)
	np.random.shuffle(new_col_2)
	np.random.shuffle(new_col_3)
	count = 0
	while(new_col_1[0] in row_1 or new_col_1[1] in row_2 or new_col_1[2] in row_3):
		np.random.shuffle(new_col_1)
		count+= 1
		if count >= 10:
			return ocho(seventh_square(middle_square(fifth_square(fourth_square(third_square(second_square(first_square(one_row()))))))))
	np.copyto(a[6:,3],new_col_1)
	count = 0
	while(new_col_2[0] in row_1 or new_col_2[1] in row_2 or new_col_2[2] in row_3):
		np.random.shuffle(new_col_2)
		count+= 1
		if count >= 10:
			return ocho(seventh_square(middle_square(fifth_square(fourth_square(third_square(second_square(first_square(one_row()))))))))
	np.copyto(a[6:,4],new_col_2)
	count = 0
	while(new_col_3[0] in row_1 or new_col_3[1] in row_2 or new_col_3[2] in row_3):
		np.random.shuffle(new_col_3)
		count+= 1
		if count >= 10:
			return ocho(seventh_square(middle_square(fifth_square(fourth_square(third_square(second_square(first_square(one_row()))))))))
	np.copyto(a[6:,5],new_col_3)
	return a

def final_square(a):
	col_1 = []
	col_2 = []
	col_3 = []
	row_1 = []
	row_2 = []
	row_3 = []
	for x in range(0,6):
		col_1 += [a[x,6]]
		col_2 += [a[x,7]]
		col_3 += [a[x,8]]
		row_1 += [a[6,x]]
		row_2 += [a[7,x]]
		row_3 += [a[8,x]]


	new_col_1 = np.setdiff1d(b,col_1)
	new_col_2 = np.setdiff1d(b, col_2)
	new_col_3 = np.setdiff1d(b, col_3)

	np.random.shuffle(new_col_1)
	np.random.shuffle(new_col_2)
	np.random.shuffle(new_col_3)
	count = 0
	while(new_col_1[0] in row_1 or new_col_1[1] in row_2 or new_col_1[2] in row_3):
		np.random.shuffle(new_col_1)
		count+= 1
		if count >= 10:
			return final_square(ocho(seventh_square(middle_square(fifth_square(fourth_square(third_square(second_square(first_square(one_row())))))))))
	np.copyto(a[6:,6],new_col_1)
	count = 0
	while(new_col_2[0] in row_1 or new_col_2[1] in row_2 or new_col_2[2] in row_3):
		np.random.shuffle(new_col_2)
		count+= 1
		if count >= 10:
			return final_square(ocho(seventh_square(middle_square(fifth_square(fourth_square(third_square(second_square(first_square(one_row())))))))))
	np.copyto(a[6:,7],new_col_2)
	count = 0
	while(new_col_3[0] in row_1 or new_col_3[1] in row_2 or new_col_3[2] in row_3):
		np.random.shuffle(new_col_3)
		count+= 1
		if count >= 10:
			return final_square(ocho(seventh_square(middle_square(fifth_square(fourth_square(third_square(second_square(first_square(one_row())))))))))
	np.copyto(a[6:,8],new_col_3)
	return a

def create_solved_puzzle():
	a = fifth_square(fourth_square(third_square(second_square(first_square(one_row())))))
	return final_square(ocho(seventh_square(middle_square(a))))


print(create_solved_puzzle())