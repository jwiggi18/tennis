import pandas as pd

#create a dataframe that mimics the data in the google sheet
data = pd.DataFrame({'Name': ['John', 'Paul', 'George', 'Ringo']})

# test the elements of the function
#make the winner's index lower than the loser's index
won = 'George'
lost = 'John'

#does the find index link work?
loser_index = data[data['Name'] == lost].index[0] #potential name to move
print(loser_index)
winner_index = data[data['Name'] == won].index[0] #potential target location
print(winner_index)

#check if the winner index is larger (lower in the rankings) than the loser index
if loser_index < winner_index:
    #reindex the DataFrame
    new_order = list(range(len(data)))
    #remove the loser from the list
    new_order.pop(loser_index)
    #insert the loser at the winner's index
    new_order.insert(winner_index, loser_index)
    #reindex the DataFrame
    data = data.reindex(new_order).reset_index(drop=True)
        
    print('The winner has been moved up in the rankings.')
    print(data)
else:
        #if the winner is ranked higher than the loser, do nothing
    print('The winner is ranked higher than the loser. No changes made.')

#not quite working yet, but close

# Example usage, this works?
name_to_move = 'George'
target_name = 'John'
data = move_element(data, name_to_move, target_name)

print(data)