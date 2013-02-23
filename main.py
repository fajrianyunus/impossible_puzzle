#!/usr/bin/python

#The problem is from http://www.mrbrown.com/blog/2013/02/more-maths-madness.html
#This problem is apparently known as "Impossible Puzzle" ( http://en.wikipedia.org/wiki/Impossible_Puzzle )
#The problem is as following:
#Both x and y are integer which satisfy 1 < x < y < 100
#Sam knows the value of x+y
#Peter knows the value of x*y
#Sam knows that Peter knows the value of x*y
#Peter knows that Sam knows the value of x+y

#They did the following conversation:
#Peter: I cannot determine the 2 numbers
#Sam: I know that (you don't know the 2 numbers)
#Peter: Now I can determine them
#Sam: So can I



#Solution explanation:
#Essentially, every statement in the conversation is new information used to eliminate some of the possibilities
#Let's say, x = 4 and y = 13
#Peter knows x*y=52 and Sam knows x+y=17
#What Peter is knowing now is that, the by now possible answers are [2, 26] and [4, 13]
#What Sam is knowing now is that, the by now possible answers are [2, 15], [3, 14], [4, 13], [5, 12], [6, 11], [7, 10], [8, 9]
#After each statement, both Peter and Sam will examine their possible answers against ALL previously stated statements

unique_xy_product = set([])
non_unique_xy_product = set([])

for x in range(2, 99):
    for y in range(x+1, 100):
        product = x * y
        if product in unique_xy_product:
            unique_xy_product.remove(product)
            non_unique_xy_product.add(product)
        elif product not in non_unique_xy_product:
            unique_xy_product.add(product)

print "the following numbers have only unique x*y factor:"          
print sorted(unique_xy_product)
print ""

def get_xy_possibilities_from_its_sum(summation_result):
    output = []
    for x in range(2, 99):
        y = summation_result - x
        if (y > 2 and y < 100 and y > x):
            output.append([x, y])
        elif (y < 3):
            break
        elif (y <= x):
            continue
    return output

def get_xy_possibilities_from_its_product(product):
    output = []
    for x in range(2, 99):
        if product % x == 0:
            y = product / x
            if x < y and y < 100:
                output.append([x, y])
        elif (x * (x+1) > product):
            break
    return output

def check_xy_validity(x, y, stop_after_certain_statement):
    if stop_after_certain_statement == None:
        stop_after_certain_statement = -1
    product = x * y
    
    #1st statement
    #Peter: I cannot determine the two numbers
    #Thus, given the products, the product must not be factorable into a unique x and y
    #where product = x * y and 1 < x < y < 100 and x is integer and y is integer
    if product in unique_xy_product:
        return False
    
    if stop_after_certain_statement == 1:
        return True
    
    summation =  x + y
    possibilities_from_summation = get_xy_possibilities_from_its_sum(summation)
    satisfies_statement_2 = True
    for el in possibilities_from_summation:
        assert len(el) == 2
        assert 1 < el[0] and el[0] < el[1] and el[1] < 100

        #2nd statement
        #Sam: I know that
        #Thus, given the sum, the sum must not be factorable into x and y which won't make Peter said "I cannot determine the two numbers" (remember the 1st statement)
        #where sum = x + y and 1 < x < y < 100 and x is integer and y is integer                
        satisfies_statement_2 &= check_xy_validity(el[0], el[1], 1)
        
        if not satisfies_statement_2:
            break

    if not satisfies_statement_2:
        return False
        
    if stop_after_certain_statement == 2:
        return True
        
    xy_possibilities_from_product = get_xy_possibilities_from_its_product(product)
    assert len(xy_possibilities_from_product) > 1
    number_of_valids_from_product = 0
    number_of_invalids_from_product = 0
    for xy in xy_possibilities_from_product:
        assert len(xy) == 2
        assert 1 < xy[0] and xy[0] < xy[1] and xy[1] < 100
        result = check_xy_validity(xy[0], xy[1], 2)
        if result:
            number_of_valids_from_product += 1
        else:
            number_of_invalids_from_product += 1
            
    assert len(xy_possibilities_from_product) == number_of_valids_from_product + number_of_invalids_from_product
    assert number_of_valids_from_product > 0
    
    #3rd statement
    #Peter: Now I can determine them
    #Thus, out of all possibilities of x and y Peter can guess, only 1 can make Sam said "I know that" (remember the 2nd statement)
    #where sum = x + y and 1 < x < y < 100 and x is integer and y is integer
    if number_of_valids_from_product != 1:
        return False
    
    if stop_after_certain_statement == 3:
        return True

    number_of_valids_from_summation = 0
    number_of_invalids_from_summation = 0    
    for el in possibilities_from_summation:
        assert len(el) == 2
        assert 1 < el[0] and el[0] < el[1] and el[1] < 100
        result = check_xy_validity(el[0], el[1], 3)
        if result:
            number_of_valids_from_summation += 1
        else:
            number_of_invalids_from_summation += 1
            
    assert len(possibilities_from_summation) == number_of_valids_from_summation + number_of_invalids_from_summation
    
    #4th statement
    #Sam: So can I
    #Thus, of of all possibilities of x and y Sam can guess, only 1 can make peter said "Now I can determine them" (remember the 3rd statement)
    #where sum = x + y and 1 < x < y < 100 and x is integer and y is integer
    if number_of_valids_from_summation == 1:
        return True
    else:
        return False

answers = []
for x in range(2, 99):
    for y in range(x+1, 100):
        is_valid = check_xy_validity(x, y, -1)
        if is_valid:
            answers.append([x, y])

print "the answers are"         
print answers