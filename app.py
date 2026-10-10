from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory storage for orders
orders = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍕 Pizza Machine - Web Kiosk</title>
    <!-- Tailwind CSS for modern styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-slate-100 min-h-screen text-slate-800 font-sans">
    
    <!-- Navbar Header -->
    <header class="bg-red-600 text-white shadow-lg">
        <div class="max-w-5xl mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <span class="text-3xl">🍕</span>
                <div>
                    <h1 class="text-2xl font-black tracking-wide">PIZZA MACHINE</h1>
                    <p class="text-xs text-red-200">Automated Order & Billing Kiosk</p>
                </div>
            </div>
            <div class="bg-red-700 px-3 py-1 rounded-full text-xs font-semibold flex items-center space-x-1">
                <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
                <span>Kiosk Online</span>
            </div>
        </div>
    </header>

    <main class="max-w-5xl mx-auto px-4 py-8 grid grid-cols-1 md:grid-cols-3 gap-8">
        
        <!-- Left 2 Cols: Order Form or Receipt -->
        <div class="md:col-span-2">
            
            {% if latest_order %}
            <!-- Receipt Card (Shown after an order is placed) -->
            <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-200">
                <div class="bg-green-600 p-6 text-white text-center">
                    <div class="inline-flex items-center justify-center w-14 h-14 bg-green-700 rounded-full mb-3 shadow-inner">
                        <i class="fas fa-check text-2xl"></i>
                    </div>
                    <h2 class="text-2xl font-bold">Order Received!</h2>
                    <p class="text-sm text-green-100">Order ID #{{ latest_order.id }} • {{ latest_order.time }}</p>
                </div>

                <div class="p-6">
                    <div class="border-b-2 border-dashed border-slate-300 pb-4 mb-4">
                        <h3 class="text-xs font-bold uppercase text-slate-400 tracking-wider mb-3">Itemized Bill</h3>
                        
                        <div class="flex justify-between py-1 font-medium">
                            <span>🍕 {{ latest_order.size_name }}</span>
                            <span>${{ latest_order.base_price }}</span>
                        </div>

                        {% if latest_order.pepperoni %}
                        <div class="flex justify-between py-1 text-slate-600 text-sm">
                            <span>+ Pepperoni Topping</span>
                            <span>${{ latest_order.pep_cost }}</span>
                        </div>
                        {% endif %}

                        {% if latest_order.extra_cheese %}
                        <div class="flex justify-between py-1 text-slate-600 text-sm">
                            <span>+ Extra Cheese</span>
                            <span>${{ latest_order.cheese_cost }}</span>
                        </div>
                        {% endif %}

                        {% if latest_order.drink_cost > 0 %}
                        <div class="flex justify-between py-1 text-slate-600 text-sm">
                            <span>🥤 {{ latest_order.drink_name }}</span>
                            <span>${{ latest_order.drink_cost }}</span>
                        </div>
                        {% endif %}
                    </div>

                    <div class="flex justify-between items-center text-xl font-black text-slate-900 mb-6">
                        <span>TOTAL AMOUNT:</span>
                        <span class="text-red-600">${{ latest_order.total_bill }}</span>
                    </div>

                    <!-- Next Customer Action Button -->
                    <a href="{{ url_for('index') }}" 
                       class="w-full block text-center bg-red-600 hover:bg-red-700 active:scale-[0.99] transition-all text-white font-bold py-3.5 px-6 rounded-xl shadow-lg shadow-red-200 text-lg">
                        <i class="fas fa-user-plus mr-2"></i> Next Customer / New Order
                    </a>
                </div>
            </div>

            {% else %}
            <!-- Order Form -->
            <div class="bg-white rounded-2xl shadow-xl p-6 md:p-8 border border-slate-200">
                <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center">
                    <i class="fas fa-utensils text-red-500 mr-2.5"></i> Customize Your Order
                </h2>

                <form action="{{ url_for('place_order') }}" method="POST" id="pizzaForm" class="space-y-6">
                    
                    <!-- 1. Size Selection -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">1. Select Pizza Size</label>
                        <div class="grid grid-cols-3 gap-3">
                            <label class="relative flex flex-col items-center justify-center p-4 border-2 rounded-xl cursor-pointer hover:border-red-400 transition-all has-[:checked]:border-red-500 has-[:checked]:bg-red-50">
                                <input type="radio" name="size" value="S" class="sr-only" checked onchange="updateTotal()">
                                <span class="text-2xl mb-1">🍕</span>
                                <span class="font-bold text-slate-800">Small</span>
                                <span class="text-xs text-red-600 font-bold mt-1">$15</span>
                            </label>
                            
                            <label class="relative flex flex-col items-center justify-center p-4 border-2 rounded-xl cursor-pointer hover:border-red-400 transition-all has-[:checked]:border-red-500 has-[:checked]:bg-red-50">
                                <input type="radio" name="size" value="M" class="sr-only" onchange="updateTotal()">
                                <span class="text-3xl mb-1">🍕</span>
                                <span class="font-bold text-slate-800">Medium</span>
                                <span class="text-xs text-red-600 font-bold mt-1">$20</span>
                            </label>

                            <label class="relative flex flex-col items-center justify-center p-4 border-2 rounded-xl cursor-pointer hover:border-red-400 transition-all has-[:checked]:border-red-500 has-[:checked]:bg-red-50">
                                <input type="radio" name="size" value="L" class="sr-only" onchange="updateTotal()">
                                <span class="text-4xl mb-1">🍕</span>
                                <span class="font-bold text-slate-800">Large</span>
                                <span class="text-xs text-red-600 font-bold mt-1">$25</span>
                            </label>
                        </div>
                    </div>

                    <!-- 2. Extra Toppings -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">2. Extra Add-ons</label>
                        <div class="space-y-3">
                            <label class="flex items-center justify-between p-3.5 border rounded-xl cursor-pointer hover:bg-slate-50 transition-all has-[:checked]:bg-amber-50 has-[:checked]:border-amber-400">
                                <div class="flex items-center space-x-3">
                                    <input type="checkbox" name="pepperoni" value="Y" class="w-5 h-5 text-red-600 rounded focus:ring-red-500" onchange="updateTotal()">
                                    <div>
                                        <span class="font-bold text-slate-800 block">Pepperoni Topping</span>
                                        <span class="text-xs text-slate-500" id="pepPriceLabel">+$2 for Small, +$3 for M/L</span>
                                    </div>
                                </div>
                                <span class="text-sm font-bold text-slate-700" id="pepPriceDisplay">+$2</span>
                            </label>

                            <label class="flex items-center justify-between p-3.5 border rounded-xl cursor-pointer hover:bg-slate-50 transition-all has-[:checked]:bg-yellow-50 has-[:checked]:border-yellow-400">
                                <div class="flex items-center space-x-3">
                                    <input type="checkbox" name="extra_cheese" value="Y" class="w-5 h-5 text-red-600 rounded focus:ring-red-500" onchange="updateTotal()">
                                    <div>
                                        <span class="font-bold text-slate-800 block">Extra Cheese</span>
                                        <span class="text-xs text-slate-500">Melted mozzarella layer</span>
                                    </div>
                                </div>
                                <span class="text-sm font-bold text-slate-700">+$1</span>
                            </label>
                        </div>
                    </div>

                    <!-- 3. Drinks Menu -->
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">3. Refreshing Drinks</label>
                        <div class="grid grid-cols-3 gap-3">
                            <label class="relative flex flex-col items-center justify-center p-3 border-2 rounded-xl cursor-pointer hover:border-blue-400 transition-all has-[:checked]:border-blue-500 has-[:checked]:bg-blue-50">
                                <input type="radio" name="drink" value="pepsi" class="sr-only" onchange="updateTotal()">
                                <span class="text-2xl mb-1">🥤</span>
                                <span class="font-bold text-slate-800 text-sm">Pepsi</span>
                                <span class="text-xs text-blue-600 font-bold mt-1">+$3</span>
                            </label>

                            <label class="relative flex flex-col items-center justify-center p-3 border-2 rounded-xl cursor-pointer hover:border-amber-400 transition-all has-[:checked]:border-amber-500 has-[:checked]:bg-amber-50">
                                <input type="radio" name="drink" value="tea" class="sr-only" onchange="updateTotal()">
                                <span class="text-2xl mb-1">🧋</span>
                                <span class="font-bold text-slate-800 text-sm">Iced Tea</span>
                                <span class="text-xs text-amber-600 font-bold mt-1">+$3</span>
                            </label>

                            <label class="relative flex flex-col items-center justify-center p-3 border-2 rounded-xl cursor-pointer hover:border-slate-400 transition-all has-[:checked]:border-slate-500 has-[:checked]:bg-slate-50">
                                <input type="radio" name="drink" value="none" class="sr-only" checked onchange="updateTotal()">
                                <span class="text-2xl mb-1">🚫</span>
                                <span class="font-bold text-slate-800 text-sm">No Drink</span>
                                <span class="text-xs text-slate-400 font-bold mt-1">$0</span>
                            </label>
                        </div>
                    </div>

                    <!-- Live Total & Submit -->
                    <div class="pt-4 border-t flex items-center justify-between">
                        <div>
                            <span class="text-xs font-bold text-slate-400 uppercase tracking-wider block">Estimated Total</span>
                            <span class="text-3xl font-black text-slate-900" id="liveTotalDisplay">$15</span>
                        </div>
                        <button type="submit" class="bg-red-600 hover:bg-red-700 active:scale-[0.98] text-white font-bold px-8 py-3.5 rounded-xl shadow-lg shadow-red-200 transition-all text-base flex items-center">
                            <i class="fas fa-receipt mr-2"></i> Print Bill & Order
                        </button>
                    </div>

                </form>
            </div>
            {% endif %}

        </div>

        <!-- Right 1 Col: Kiosk Order Queue / History -->
        <div>
            <div class="bg-white rounded-2xl shadow-md p-5 border border-slate-200">
                <div class="flex items-center justify-between mb-4 border-b pb-3">
                    <h3 class="font-bold text-slate-800 text-sm flex items-center">
                        <i class="fas fa-history text-slate-400 mr-2"></i> Kiosk Queue
                    </h3>
                    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full font-bold">
                        {{ orders|length }} Orders
                    </span>
                </div>

                {% if orders %}
                <div class="space-y-3 max-h-96 overflow-y-auto pr-1">
                    {% for ord in orders|reverse %}
                    <div class="p-3 bg-slate-50 rounded-lg border border-slate-100 text-xs flex justify-between items-center">
                        <div>
                            <div class="font-bold text-slate-800">#{{ ord.id }} - {{ ord.size_name }}</div>
                            <div class="text-slate-500 text-[11px]">
                                {% if ord.drink_cost > 0 %}+ {{ ord.drink_name }} • {% endif %}
                                {{ ord.time }}
                            </div>
                        </div>
                        <span class="font-black text-slate-900 bg-white px-2 py-1 rounded shadow-sm border border-slate-100">
                            ${{ ord.total_bill }}
                        </span>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <div class="text-center py-8 text-slate-400 text-xs">
                    <i class="fas fa-pizza-slice text-3xl text-slate-200 mb-2 block"></i>
                    No orders placed yet today.
                </div>
                {% endif %}
            </div>
        </div>

    </main>

    <script>
        function updateTotal() {
            const size = document.querySelector('input[name="size"]:checked')?.value || 'S';
            const hasPep = document.querySelector('input[name="pepperoni"]')?.checked;
            const hasCheese = document.querySelector('input[name="extra_cheese"]')?.checked;
            const drink = document.querySelector('input[name="drink"]:checked')?.value || 'none';
            
            let total = 0;
            if (size === 'S') total += 15;
            else if (size === 'M') total += 20;
            else if (size === 'L') total += 25;

            const pepCost = size === 'S' ? 2 : 3;
            document.getElementById('pepPriceDisplay').innerText = '+$' + pepCost;

            if (hasPep) total += pepCost;
            if (hasCheese) total += 1;
            if (drink === 'pepsi' || drink === 'tea') total += 3;

            document.getElementById('liveTotalDisplay').innerText = '$' + total;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, orders=orders, latest_order=None)

@app.route("/order", methods=["POST"])
def place_order():
    size = request.form.get("size", "S").upper()
    pepperoni = request.form.get("pepperoni") == "Y"
    extra_cheese = request.form.get("extra_cheese") == "Y"
    drink = request.form.get("drink", "none").lower()

    # Pricing calculation
    bill = 0
    size_name = "Small Pizza"
    base_price = 15

    if size not in ("S", "M", "L"):
        size = "S"  # FIX: unknown size silently billed $0 before

    if size == "S":
        bill += 15
        base_price = 15
        size_name = "Small Pizza"
    elif size == "M":
        bill += 20
        base_price = 20
        size_name = "Medium Pizza"
    elif size == "L":
        bill += 25
        base_price = 25
        size_name = "Large Pizza"

    pep_cost = 0
    if pepperoni:
        pep_cost = 2 if size == "S" else 3
        bill += pep_cost

    cheese_cost = 0
    if extra_cheese:
        cheese_cost = 1
        bill += cheese_cost

    drink_name = "No Drink"
    drink_cost = 0
    if drink == "pepsi":
        drink_name = "Pepsi"
        drink_cost = 3
    elif drink == "tea":
        drink_name = "Iced Tea"
        drink_cost = 3

    bill += drink_cost

    order_record = {
        "id": 1000 + len(orders) + 1,
        "size": size,
        "size_name": size_name,
        "base_price": base_price,
        "pepperoni": pepperoni,
        "pep_cost": pep_cost,
        "extra_cheese": extra_cheese,
        "cheese_cost": cheese_cost,
        "drink_name": drink_name,
        "drink_cost": drink_cost,
        "total_bill": bill,
        "time": datetime.now().strftime("%I:%M:%S %p")
    }

    orders.append(order_record)

    return render_template_string(HTML_TEMPLATE, orders=orders, latest_order=order_record)

if __name__ == "__main__":
    print("\n🍕 Pizza Machine Web App is running!")
    print("👉 Open your browser at: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)

