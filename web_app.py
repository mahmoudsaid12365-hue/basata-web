from flask import Flask, render_template_string
from supabase_client import supabase

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Basata Copy Center</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: Arial; padding:20px;">
    <h2>📋 العملاء</h2>
    <ul>
    {% for customer in customers %}
        <li>
            <b>{{ customer.name }}</b>
            (<a href="/account/{{ customer.id }}">عرض كشف الحساب</a>)
        </li>
    {% endfor %}
    </ul>
</body>
</html>
"""

ACCOUNT_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>كشف حساب</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: Arial; padding:20px;">
    <h2>📄 كشف حساب العميل</h2>

    <table border="1" cellpadding="5">
        <tr>
            <th>الوصف</th>
            <th>ورق</th>
            <th>نسخ</th>
            <th>السعر</th>
            <th>الإجمالي</th>
        </tr>
        {% for op in operations %}
        <tr>
            <td>{{ op.description }}</td>
            <td>{{ op.papers }}</td>
            <td>{{ op.copies }}</td>
            <td>{{ op.price }}</td>
            <td>{{ op.total }}</td>
        </tr>
        {% endfor %}
    </table>

    <br>
    <a href="/">⬅ رجوع</a>
</body>
</html>
"""

@app.route("/")
def home():
    customers = supabase.table("customers").select("*").execute().data
    return render_template_string(HTML_PAGE, customers=customers)

@app.route("/account/<int:customer_id>")
def account(customer_id):
    operations = supabase.table("operations") \
        .select("*") \
        .eq("customer_id", customer_id) \
        .execute().data

    return render_template_string(ACCOUNT_PAGE, operations=operations)

if __name__ == "__main__":
    app.run(debug=True)