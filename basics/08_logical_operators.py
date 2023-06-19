# Say our requirement is to check if the price is between 10 and 30
price = 25
print(price > 10 and price < 30)
# and : If both the boolean expression return true,
# then the result of the entire expression will be true

# Or operator : If at least one of the boolean expressions returns true,
# then the result of the entire expression will be true
price = 5
print(price > 10 or price < 30)
# price > 10 => False, However, price < 30 => True. Therefore, Overall result will be True

# Not Operator : inverses any value you give
price = 5
print(price > 10)  # result will be False
print(not price > 10)
