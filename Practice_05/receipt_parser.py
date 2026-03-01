import re
import json

def read_receipt(f_p):
    with open(f_p, "r", encoding="utf-8") as f:
        return f.read()



#1
def extract_prices(txt):
    
    prices = re.findall(r'\d[\d ]*,\d{2}', txt)
    
    
    prices = [float(p.replace(" ", "").replace(",", ".")) for p in prices]
    return prices
#2
def extract_products(txt):
    lines = txt.split("\n")
    products = []
    
    for i, line in enumerate(lines):
        
        if re.match(r'^\d+\.$', line.strip()):
            if i + 1 < len(lines):
                product = lines[i + 1].strip()
                products.append(product)
    
    return products
#3
def extract_total(txt):
    match = re.search(r'ИТОГО:\s*\n?\s*([\d ]*,\d{2})', txt)
    if match:
        return float(match.group(1).replace(" ", "").replace(",", "."))
    return None
#4
def extract_datetime(txt):
    match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})', txt)
    if match:
        return {
            "date": match.group(1),
            "time": match.group(2)
        }
    return None
#5
def extract_payment_method(txt):
    if "Банковская карта" in txt:
        return "Bank Card"
    elif "Наличные" in txt:
        return "Cash"
    return "Unknown"

def parse_receipt(f_p):
    txt = read_receipt(f_p)
    
    products = extract_products(txt)
    prices = extract_prices(txt)
    total = extract_total(txt)
    datetime_info = extract_datetime(txt)
    payment = extract_payment_method(txt)
    
    result = {
        "products": products,
        "prices": prices,
        "total": total,
        "date": datetime_info["date"] if datetime_info else None,
        "time": datetime_info["time"] if datetime_info else None,
        "payment_method": payment
    }
    
    return result



if __name__ == "__main__":
    f_p = "raw.txt"
    data = parse_receipt(f_p)
    
    print("Parsed Receipt:\n")
    print(json.dumps(data, indent=4, ensure_ascii=False))