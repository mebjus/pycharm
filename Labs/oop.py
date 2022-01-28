# class DepartmentReport():
#     def __init__(self, company_name):
#         self.deals = []
#         self.company_name = company_name
#
#     def add_revenue(self, revenues):
#         if not hasattr(self, 'revenues'):
#             self.revenues  = []
#         self.revenues.append(revenues)
#
#     def average_revenue(self):
#         return (f'Average department revenue for {self.company_name}: {round(sum(self.revenues)/len(self.revenues))}')
#
# report = DepartmentReport("Danon")
# report.add_revenue(1_000_000)
# report.add_revenue(400_000)
#
# print(report.average_revenue())


# class SalesReport():
#     def __init__(self, employee_name):
#         self.deals = []
#         self.employee_name = employee_name
#
#     def add_deal(self, company, amount):
#         self.deals.append({'company': company, 'amount': amount})
#
#     def total_amount(self):
#         return sum([deal['amount'] for deal in self.deals])
#
#     def average_deal(self):
#         return self.total_amount()/len(self.deals)
#
#     def all_companies(self):
#         return list(set([deal['company'] for deal in self.deals]))
#
#     def print_report(self):
#         print("Employee: ", self.employee_name)
#         print("Total sales:", self.total_amount())
#         print("Average sales:", self.average_deal())
#         print("Companies:", self.all_companies())
#
#
# report = SalesReport("Ivan Semenov")
# report2 = SalesReport("oleg iii")
#
# report2.add_deal("PepsiCo", 120_000)
# report.add_deal("SkyEng", 250_000)
# report.add_deal("PepsiCo", 20_000)
#
# report.print_report()
# # => Employee:  Ivan


# class User():
#     # Базовые данные
#     def __init__(self, email, password, balance):
#         self.email = email
#         self.password = password
#         self.balance = balance
#
#     def login(self, email, password):
#         return (self.email == email) and (self.password == password)
#
#     def update_balance(self, amount):
#         self.balance +=  amount
#
# user = User("gosha@roskino.org", "qwerty", 20_000)
# user.login("gosha@roskino.org", "qwerty123")
# # => False
# user.login("gosha@roskino.org", "qwerty")
# # => True
# user.update_balance(200)
# user.update_balance(-500)
# print(user.balance)
# # => 19700

import statistics

class IntDataFrame():
    def __init__(self, lst):
        # Инициализируем атрибуты
        self.lst = lst
        self.round_d()

    def round_d(self):
        self.lst = [int(value) for value in self.lst]

    def count(self):
        c=0
        for i in self.lst:
            if i != 0:
                c += 1
        return c

    def unique(self):
        c=[]
        for i in self.lst:
            if i not in c:
                c.append(i)
        return len(set(c))

df = IntDataFrame([4.7, 4, 3, 0, 2.4, 0.3, 4])
print(df.count())
print(df.unique())
