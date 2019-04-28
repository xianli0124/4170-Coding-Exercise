#!/usr/bin/env python
# coding: utf-8

# In[1]:


#List of coin denominations
coins = [100, 50, 20, 10, 5, 1]

#Function to recursively find all coin combinations for a given value
def coin_recur(value, coins, cur_ind = 0):
    ways = 0
    if value == 0:
        return 1
    if value < 0:
        return 0
    while cur_ind < len(coins):
        ways = ways + coin_recur(value - coins[cur_ind], coins, cur_ind)
        #Increment index to slowly use less coins
        cur_ind = cur_ind + 1
    
    return ways

coin_recur(500, coins)


# In[2]:


#Number of sides on Gregor's dice
s_G = 5

#Number of sides on Oberyn's dice
s_O = 10

#Number of die Gregor has
n_G = 8

#Number of die Oberyn Has
n_O = 4

#Total number of dice combinations for Gregor
G_coms = s_G**n_G

#Total number of dice combinations for Oberyn
O_coms = s_O**n_O

#Max value possible for each player with their dice
max_val = s_G*n_G

#Probability Gregor wins
G_win_prob = 0.0

#List for storing probabilities of each player's probability of rolling each number
G_prob = []
O_prob = []

#Function for combinations
def C(top, bot):
    val = 1
    den = 1
    a = top - bot
    if a > bot:
        b = a
        a = bot
        bot = b
    for i in range((bot+1), (top+1)):
        val = val * i
    for i in range(1, (a+1)):
        den = den * i
    return val / den

#I looked this up, but this is the formula for calculating the number of combinations for each dice outcome
def dice_coms(s, n, t):
    res = 0
    lim = int(((t - n) / s) + 1) #Lazy floor function for the formula
    for k in range(lim):
        res = res + ((-1)**k)*C(n, k)*C(t - s*k - 1, t - s*k - n)
    return res

#Creating the array for storing each player's probabilities. Didn't want to use any built in packages
#such as numpy so I just appended zeros
for i in range(max_val):
    G_prob.append(0)
for i in range(max_val):
    O_prob.append(0)

#Calculating each player's probabilities for rolling each number
for i in range(n_G, int((max_val + n_G)/2 + 1)):
    G_prob[i-1] = dice_coms(s_G, n_G, i) / G_coms
    G_prob[max_val - (i - n_G) - 1] = G_prob[i-1]
    
for i in range(n_O, int((max_val + n_O)/2 + 1)):
    O_prob[i-1] = dice_coms(s_O, n_O, i) / O_coms
    O_prob[max_val - (i - n_O) - 1] = O_prob[i-1]

#Calculating Gregor's winning probability by summing all his winning probabilities given Oberyn's roll
for i in range(n_O, max_val):
    G_win_prob = G_win_prob + O_prob[i]*sum(G_prob[i+1:len(G_prob)])

G_win_prob


# In[3]:


#Function to make the given matrix with the modifications for the Hungarian Algorithm
def make_Matrix():
    line_1 = '7 53 183 439 863 497 383 563 79 973 287 63 343 169 583'
    line_2 = '627 343 773 959 943 767 473 103 699 303 957 703 583 639 913'
    line_3 = '447 283 463 29 23 487 463 993 119 883 327 493 423 159 743'
    line_4 = '217 623 3 399 853 407 103 983 89 463 290 516 212 462 350'
    line_5 = '960 376 682 962 300 780 486 502 912 800 250 346 172 812 350'
    line_6 = '870 456 192 162 593 473 915 45 989 873 823 965 425 329 803'
    line_7 = '973 965 905 919 133 673 665 235 509 613 673 815 165 992 326'
    line_8 = '322 148 972 962 286 255 941 541 265 323 925 281 601 95 973'
    line_9 = '445 721 11 525 473 65 511 164 138 672 18 428 154 448 848'
    line_10 = '414 456 310 312 798 104 566 520 302 248 694 976 430 392 198'
    line_11 = '184 829 373 181 631 101 969 613 840 740 778 458 284 760 390'
    line_12 = '821 461 843 513 17 901 711 993 293 157 274 94 192 156 574'
    line_13 = '34 124 4 878 450 476 712 914 838 669 875 299 823 329 699'
    line_14 = '815 559 813 459 522 788 168 586 966 232 308 833 251 631 107'
    line_15 = '813 883 451 509 615 77 281 613 459 205 380 274 302 35 805'
    lines = [line_1, line_2, line_3, line_4, line_5, line_6, line_7, line_8, line_9, 
             line_10, line_11, line_12, line_13, line_14, line_15]

    Matrix = []
    for i in lines:
        Matrix.append([int(j) for j in i.split(' ')])
    
    #Since we want the maximum, I thought flipping all the values by subtracting the largest
    #value in the array and taking the absolute value would work, since the Hungarian Algorithm
    #finds the minimums
    max_val = 0
    for i in Matrix:
        max_val_row = max(i)
        if max_val_row > max_val:
            max_val = max_val_row
    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            Matrix[i][j] = abs(Matrix[i][j] - max_val)

    #Subtracting the row and column minima
    for i in range(len(Matrix)):
        min_val = 9999999
        for j in range(len(Matrix)):
            if Matrix[i][j] < min_val:
                min_val = Matrix[i][j]
        for j in range(len(Matrix)):
            Matrix[i][j] = Matrix[i][j] - min_val
            
    for j in range(len(Matrix)):
        min_val = 9999999
        for i in range(len(Matrix)):
            if Matrix[i][j] < min_val:
                min_val = Matrix[i][j]
        for i in range(len(Matrix)):
            Matrix[i][j] = Matrix[i][j] - min_val 
    
    return Matrix


# In[4]:


#Example given in the pdf. I used this to test my algorithm
def simple_case():
    line_1 = '7 53 183 439 863'
    line_2 = '497 383 563 79 973'
    line_3 = '287 63 343 169 583'
    line_4 = '627 343 773 959 943'
    line_5 = '767 473 103 699 303'
    lines = [line_1, line_2, line_3, line_4, line_5]   

    Matrix = []
    for i in lines:
        Matrix.append([int(j) for j in i.split(' ')])
    
    max_val = 0
    for i in Matrix:
        max_val_row = max(i)
        if max_val_row > max_val:
            max_val = max_val_row
    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            Matrix[i][j] = abs(Matrix[i][j] - max_val)

    for i in range(len(Matrix)):
        min_val = 9999999
        for j in range(len(Matrix)):
            if Matrix[i][j] < min_val:
                min_val = Matrix[i][j]
        for j in range(len(Matrix)):
            Matrix[i][j] = Matrix[i][j] - min_val
           
    for j in range(len(Matrix)):
        min_val = 9999999
        for i in range(len(Matrix)):
            if Matrix[i][j] < min_val:
                min_val = Matrix[i][j]
        for i in range(len(Matrix)):
            Matrix[i][j] = Matrix[i][j] - min_val 
    
    return Matrix


# In[5]:


#Function to assign zeros and find rows to mark
def assign_zeros(Matrix):
    assigned_rows = []
    assigned_cols = []
    conflicting_rows = []
    assigned_zeros = []
    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            if (Matrix[i][j] == 0) & (j not in assigned_cols) & (i not in assigned_rows):
                assigned_rows.append(i)
                assigned_cols.append(j)
                assigned_zeros.append([i, j])
    for i in range(len(Matrix)):
        if i not in assigned_rows:
            conflicting_rows.append(i)
    return assigned_zeros, conflicting_rows

#Function to mark the columns of the rows with conflicting zeros
def mark_cols(Matrix, new_rows, marked_cols):
    new_cols = []
    for i in new_rows:
        for j in range(len(Matrix)):
            if (Matrix[i][j] == 0) & (j not in marked_cols):
                marked_cols.append(j)
                new_cols.append(j)
    return marked_cols, new_cols

#Function to mark the rows given the column with conflicts
def mark_rows(Matrix, assigned_zeros, new_cols, conflicting_rows):
    new_rows = []
    for i in range(len(assigned_zeros)):
        if (assigned_zeros[i][1] in new_cols) & (assigned_zeros[i][0] not in conflicting_rows):
            conflicting_rows.append(assigned_zeros[i][0])
            new_rows.append(assigned_zeros[i][0])
    return conflicting_rows, new_rows

#Function to determine which rows and columns to mark to draw the minimum number of lines needed
#to cover all the zeros
def mark_rows_and_cols(Matrix, assigned_zeros, conflicting_rows):
    marked_cols = []
    row_line = []
    marked_cols, new_cols = mark_cols(Matrix, conflicting_rows, marked_cols)
    conflicting_rows, new_rows = mark_rows(Matrix, assigned_zeros, new_cols, conflicting_rows)
    while len(new_rows) > 0:
        marked_cols, new_cols = mark_cols(Matrix, new_rows, marked_cols)
        conflicting_rows, new_rows = mark_rows(Matrix, assigned_zeros, new_cols, conflicting_rows)
    for i in range(len(Matrix)):
        if i not in conflicting_rows:
            row_line.append(i)
    return row_line, marked_cols

#Function to subtract the minimum of all unmarked spaces and to add the minimum to 
#spaces covered twice
def subtract_min_from_remainder(Matrix, row_line, marked_cols):
    min_val = 99999
    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            if (Matrix[i][j] < min_val) & (i not in row_line) & (j not in marked_cols):
                min_val = Matrix[i][j]
    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            if (i not in row_line) & (j not in marked_cols):
                Matrix[i][j] = Matrix[i][j] - min_val
            if (i in row_line) & (j in marked_cols):
                Matrix[i][j] = Matrix[i][j] + min_val
    return Matrix

#Hungarian Algorithm. Keeps modifying the matrix until it can assign a minimum to all rows without conflicts
def Hungarian_Algorithm(Matrix):
    while(1):
        assigned_zeros, conflicting_rows = assign_zeros(Matrix)
        print(assigned_zeros)
        if len(assigned_zeros) == len(Matrix):
            break
        row_line, marked_cols = mark_rows_and_cols(Matrix, assigned_zeros, conflicting_rows)
        Matrix = subtract_min_from_remainder(Matrix, row_line, marked_cols)
    return assigned_zeros


# In[6]:


Matrix = simple_case()
#Matrix = make_Matrix()
Hungarian_Algorithm(Matrix)

