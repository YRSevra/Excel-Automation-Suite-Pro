def detect_dataset(df):

    columns = [c.lower() for c in df.columns]

    sales_keywords = [
        "product",
        "price",
        "sales",
        "customer",
        "quantity",
        "amount",
        "revenue"
    ]

    hr_keywords = [
        "employee",
        "salary",
        "department",
        "designation"
    ]

    student_keywords = [
        "student",
        "marks",
        "subject",
        "grade",
        "roll"
    ]

    finance_keywords = [
        "income",
        "expense",
        "balance",
        "account",
        "transaction"
    ]

    inventory_keywords = [
        "stock",
        "warehouse",
        "inventory",
        "supplier"
    ]

    if any(word in " ".join(columns) for word in sales_keywords):
        return "📈 Sales Dataset"

    if any(word in " ".join(columns) for word in hr_keywords):
        return "👨‍💼 HR Dataset"

    if any(word in " ".join(columns) for word in student_keywords):
        return "🎓 Student Dataset"

    if any(word in " ".join(columns) for word in finance_keywords):
        return "💰 Finance Dataset"

    if any(word in " ".join(columns) for word in inventory_keywords):
        return "📦 Inventory Dataset"

    return "📂 General Dataset"