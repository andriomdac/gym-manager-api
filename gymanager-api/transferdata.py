import json
from icecream import ic
import requests as rq



with open("data.json", "r") as file:
    data = json.load(file)


students = []


for i in data:
    if i["model"] == "students.student":
        students.append(
            {
                "pk": i["pk"],
                "name": i["fields"]["name"],
                "phone": i["fields"]["phone"],
                "reference": i["fields"]["reference"],
                "payments": [],
            }
        )


for i in data:
    if i["model"] == "payments.payment":
        payment_student_pk = i["fields"]["student"]
        payment_fields = i["fields"]

        for student in students:
            if student["pk"] == payment_student_pk:
                payment = {
                    "pk": i["pk"],
                    "payment_date": payment_fields["payment_date"],
                    "next_payment_date": payment_fields["next_payment_date"],
                    "payment_package": payment_fields["payment_package"],
                    "observations": payment_fields["observations"],
                    "user_signature": payment_fields["user_signature"],
                    "created_at": payment_fields["created_at"],
                    "values": [],
                }
                student["payments"].append(payment)



for i in data:
    if i["model"] == "payments.paymentvalue":
        paymentvalue_payment_id = i["fields"]["payment"]
        for student in students:
            for payment in student["payments"]:
                if payment["pk"] == paymentvalue_payment_id:
                    payment["values"].append(i["fields"])


with open("cleaned_data.json", "w") as cleaned_data:
    json.dump(students, cleaned_data, indent=4, ensure_ascii=False)


for student in students:
    rq.api.post(
        url="http://localhost:8000/api/students/",
        headers={
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxNzk4NTI5LCJpYXQiOjE3NjE3OTEzMjksImp0aSI6IjY2ZWE0Y2M3ZmUzNzQ5YTJiY2JhOWMxYjRkZDVkNGZmIiwidXNlcl9pZCI6IjEiLCJ1c2VyX3Byb2ZpbGVfdXVpZCI6IjZlZTVmMmQ0LTQyZmUtNDhiMC05NTBjLWJhN2M2M2E4YjJiYSJ9.ZzXoOWgNf-7wLcgi43fsSQSzCPAvsOGShDfB-cC7Kbo",
                "Content-Type": "application/json" 
            },
        json={
            "name": f"{student['name']}",
            "reference": f"{student['reference']}",
            "phone": f"{student['phone']}"
        }
    )




