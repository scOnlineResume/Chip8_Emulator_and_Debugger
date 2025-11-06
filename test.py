def extract_digits(number):
    # In the form (d1)(d2)(d3)
    d1 = number // 100
    d3 = number % 10
    d2 = (number - (d1*100) - d3) // 10

    return d1,d2,d3

for ii in range(255):
    d1,d2,d3 = extract_digits(ii)
    print(f"ii = {ii}, extracted_digits: {d1} {d2} {d3}")

