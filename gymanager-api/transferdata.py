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
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMTM5OTEyLCJpYXQiOjE3NjExMzI3MTIsImp0aSI6ImMxNjdjOWI5ZGExNDQ4Yzc5MzRhZjVhNmRlN2E1MWMyIiwidXNlcl9pZCI6IjEiLCJ1c2VyX3Byb2ZpbGVfdXVpZCI6IjU2NGJjNWJmLTE0M2QtNDg1ZC1hYjIyLTFmNTIwOThjMjViMiJ9.TLpDMp_5naAq0H60iqwQOxA3M7w-MdJsaI5jO_xCu9Q",
                "Content-Type": "application/json" 
            },
        json={
            "name": f"{student['name']}",
            "reference": f"{student['reference']}",
            "phone": f"{student['phone']}"
        }
    )




