from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)
def findprice(user_input):
    numbers=[]
    temp=user_input.split()
    for word in temp:
        if word.isdigit():
            numbers.append(int(word))
    return numbers

def findbrand(user_input):
    unique_brands = ["Infinix", "Realme", "Vivo", "Xiaomi", "Redmi", "Samsung", "Tecno", "Honor", "itel", "Oppo", "A57", "Sparx", "Original", "VGOTEL", "Mobile", "Google", "Imported", "Vgotel", "Zero", "iPhone", "LG", "Nokia", "Combo", "ZTE", "OnePlus", "Sony", "Motorola", "Digit", "Aquos", "Apple"]
    brange = []
    temp = user_input.lower().split()
    for word in temp:
        for brand in unique_brands:
            if word == brand.lower():
                brange.append(brand)
    return brange

def priceandrating(user_input):
    priceflag=False
    ratingflag=False
    temp=user_input.split()
    for word in temp:
        if word.lower() == "rating":
            ratingflag=True
        if word.lower() == "price":
            priceflag=True
    if (priceflag and ratingflag):
        return True
    else:
        return False
    
def findrating(user_input):
    temp=user_input.split()
    for word in temp:
        if word.lower() =="rating":
            return True
    return False
    
def findprodrating(user_input):
    number='3'
    signseq=''
    temp=user_input.split()
    for word in temp:
        if word.isdigit():
            number=word
        if word.lower() =="rating":
            break
        if keyword(word):
            ello=keyword(word)
            if ello == "over":
                signseq='>'
            elif ello == "under":
                signseq='<'
    conn=sqlite3.connect("finalDataBaseProject.db")
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT *
        FROM Products
        WHERE rating {signseq} ?
        AND rating != 'No Score';
    """, (number))
    results = cursor.fetchall()
    if not results:
        return "Chatbot: No products found based on your query."
    else:
        return results
    
    
def priceandratingfind(user_input):
    wordsequence=[]
    signseq=[]
    temp=user_input.split()
    for word in temp:
        if keyword(word):
            ello=keyword(word)
            if ello == "over":
                signseq.append('>')
            elif ello == "under":
                signseq.append('<')
        if ((word.lower() == "price" or word.lower() == "rating") and word.lower != wordsequence):
            wordsequence.append(word)
    
    values=findprice(user_input)
    conn=sqlite3.connect("finalDataBaseProject.db")
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT *
        FROM Products
        WHERE {wordsequence[0]} {signseq[0]} ?
            AND {wordsequence[1]} {signseq[1]} ?;
    """, (values[0], values[1]))
                   
    results = cursor.fetchall()
    if not results:
        return "Chatbot: No products found based on your query."
    else:
        return results

    
    

def findtopword(user_input):
    temp=user_input.split()
    for word in temp:
        if word.lower() == "top":
            return True
    return False

def topphones(user_input,brandnames):
    numberrange=5
    temp=user_input.split()
    for i in range(len(temp)):
        if temp[i].lower() == "top":
            numberrange=int(temp[i+1])
            break
    conn = sqlite3.connect("finalDataBaseProject.db")
    cursor = conn.cursor()
    

    cursor.execute("""
            SELECT *
            FROM Products 
            WHERE brand LIKE ? 
            AND rating != 'No Score'
            ORDER BY rating DESC
            LIMIT ?;
        """, ('%' + brandnames[0] + '%', numberrange))

    results = cursor.fetchall()
    if not results:
        return "Chatbot: No products found based on your query."
    else:
        return results


def keyword(user_input):
    synonyms_dict = {
    "over": ["above", "more than", "higher than","over"],
    "under": ["below", "less than", "lower than","under"],
    "between": ["in between", "range", "from", "to","between"],
    }
    temp = user_input.lower().split()

    for token in temp:
        for keyword, synonyms in synonyms_dict.items():
            if token.lower() in synonyms:
                return keyword

    return None 
    
def find(brandname, pricerange, sign,user_input):
    conn = sqlite3.connect("finalDataBaseProject.db")
    cursor = conn.cursor()

    query_base = """
    SELECT *
    FROM Products P
    WHERE 1=1
    """

    conditions = []
    parameters = []
    temp=""
    for i in range(len(sign)):
        if pricerange is not None:
            conditions.append(f"P.price {sign[i]} ?")
            parameters.append(pricerange[i])
    temp=""
    for i in range(len(brandname)):
        
        if brandname is not None:
            if i==0:
                if len(brandname)>1:
                    temp+="(P.brand LIKE ?"
                else:
                    temp+="P.brand LIKE ?"
                    conditions.append(temp)
#                     parameters.append(f"%{brandname[i]}%")

            elif i >0 and i<len(brandname)-1:
            
                temp+=" OR P.brand LIKE ?"

            elif i==len(brandname)-1:
                temp =temp + " OR P.brand LIKE ?)"
                conditions.append(temp)
            parameters.append(f"%{brandname[i]}%")
                       
    query=query_base
    for i in range(len(conditions)):
        query = query + " AND "+conditions[i]
    cursor.execute(query, (parameters))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if not results:
        return "Chatbot: No products found based on your query."
    else:
        return results

# def display(final):
#     for i in range(len(final)):
#         print(f"Product : {i+1}")
#         print(final[i][0])
#         print(f"Name : {final[i][1]}")
#         print(f"Price : {final[i][2]}")
#         print(f"Brand : {final[i][3]}")
#         print(f"Rating : {final[i][4]}")
#         print(f"URL : {final[i][6]}")
#         print(" ")
#user_input = input("You: ")    
def process_user_input(user_input):
    print("Chatbot: Hello! Type 'bye' to exit.")
    # print("eelo")

    # if user_input.lower() == 'bye':
    #     print("Chatbot: Goodbye!")
    #     break
    brandname=findbrand(user_input)
    pricerange=[]
    comparison=None
    sign=[]
    signs=None
    # fardeen = []
    if(priceandrating(user_input)):
        ello1=priceandratingfind(user_input)
        # continue
        # fardeen+=ello1
        return ello1

    if (findtopword(user_input)):
        ello=topphones(user_input,brandname)
        # fardeen+=ello
        return ello
        # continue

    if (findrating(user_input)):
        ello2 = findprodrating(user_input)
        return ello2
        # continue

    if(findprice(user_input)):
        pricerange=findprice(user_input)
        pricerange=sorted(pricerange, reverse=True)
        comparison=keyword(user_input)
        if comparison == "over":
            sign=['>']
        elif comparison == "under":
            sign=['<']
        elif comparison == "between":
            sign=['<','>']
    return find(brandname,pricerange,sign,user_input)


def calculate_dashboard_metrics():
    conn = sqlite3.connect("finalDataBaseProject.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Products;")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(price) FROM Products;")
    average_price = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(rating) FROM Products WHERE rating != 'No Score';")
    average_ratings = cursor.fetchone()[0]

    conn.close()

    return {
        'total_products': total_products,
        'average_price': average_price,
        'average_ratings': average_ratings,
    }

@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/', methods=['POST'])
def get_user_input():
    user_input = request.form['user_input']
    response = process_user_input(user_input)
    fardeen = ""
    counter = 1
    for i in response:
        fardeen += "Product " + str(counter) + "\n"
        fardeen += "Name: " + str(i[1]) + "\n"
        fardeen += "Price: " + str(i[2]) + "\n"  
        fardeen += "Rating: " + str(i[4]) + "\n"  
        fardeen += "URL: <a href='" + str(i[6]) + "' target='_blank'>" + str(i[6]) + "</a>\n" 
        counter += 1

    print(fardeen)
    print(" ")
    return render_template('index3.html', user_input=user_input, response=fardeen)

@app.route('/dashboard')
def dashboard():
    metrics = calculate_dashboard_metrics()
    return render_template('dashboard.html', metrics=metrics)

if __name__ == '__main__':
    app.run(debug=True)