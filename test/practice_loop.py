cities = ["казань", "Москва", "СПБ"]
for citi in cities:
    print(citi)

ages = [15, 22, 8, 30, 17]
for age in ages:
    if age >= 18: 
      print("совершеннолетний")
    else: 
      print("несоврешеннолетний")  

prices = [50, 120, 30, 200]
total = 0

for price in prices:
    total = total + price   # или короче: total += price

print(total)
 