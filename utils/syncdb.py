# coding: UTF-8
"""
Created on 2015/09/30

@author: Yang Wanjun
"""
import re
import datetime

from django.db import connection

from eb import models


class SyncDb():

    def __init__(self):
        self.cursor = None
        self.company = self.sync_company()

    def sync_company(self):
        lst = models.Company.objects.all()
        if lst.count() == 0:
            company = models.Company()
            company.name = u"株式会社イー・ビジネス"
            company.post_code = "1050014"
            company.address1 = u"東京都港区芝２丁目"
            company.address2 = u"28-8芝2丁目ビル10階"
            company.tel = "03-6809-3235"
            company.save()
            return company
        else:
            return lst[0]

    def sync_subcontractor(self):
        # 協力会社
        self.cursor = connection.cursor()
        self.cursor.execute(u"select distinct Company"
                            u"  from t_employee t1 "
                            u" where not exists( select 1 from eb_subcontractor t2 where t2.name = t1.Company)"
                            u"   and t1.Company is not null"
                            u"   and trim(t1.Company) <> ''"
                            u"   and t1.Company <> '株式会社イー・ビジネス';")
        for name in self.cursor.fetchall():
            subcontractor = models.Subcontractor()
            subcontractor.name = name[0]
            subcontractor.save()

    def sync_section(self):
        # 部署
        self.cursor = connection.cursor()
        self.cursor.execute(u"select distinct DeptName"
                            u"  from t_dept t1"
                            u" where not exists( select 1 from eb_section t2 where t2.name = t1.DeptName);")
        for name, in self.cursor.fetchall():
            section = models.Section()
            section.name = name
            section.company = section.company
            section.save()

    def sync_member(self):
        # 社員
        self.cursor = connection.cursor()
        self.cursor.execute(u"select lpad(EmployeeID, 6, '0') as EmployeeID"
                            u"	   , EmployeeName"
                            u"     , JapaneseSpell"
                            u"     , birthday"
                            u"     , PostCode"
                            u"     , Address1"
                            u"     , Address2"
                            u"     , Tel as phone"
                            u"     , EmployeeType as member_type"
                            u"     , Company as CompanyName"
                            u"     , Certificate"
                            u"     , Note"
                            u"  from t_employee t1"
                            u" where not exists( select 1 "
                            u"                     from eb_member t2 "
                            u"                    where cast(t2.employee_id as unsigned) = t1.EmployeeID)"
                            u"   and not exists( select 1 "
                            u"				       from eb_salesperson t3"
                            u"					  where cast(t3.employee_id as unsigned) = t1.EmployeeID)"
                            u"   and t1.DeleteFlg = 0;")
        for employee_id, \
            full_name, \
            full_name_jp, \
            birthday, \
            post_code, \
            address1, \
            address2, \
            phone, \
            member_type, \
            company_name, \
            certificate, \
            comment in self.cursor.fetchall():

            if member_type == '5':
                member = models.Salesperson()
            else:
                member = models.Member()
            member.employee_id = employee_id
            member.first_name = full_name[0]
            member.last_name = full_name[1:]
            if full_name_jp:
                ja_list = full_name_jp.split(u"　")
                member.first_name_ja = ja_list[0] if ja_list[0] and ja_list[0].strip() else None
                if len(ja_list) > 1:
                    member.last_name_ja = ja_list[1] if ja_list[1] and ja_list[1].strip() else None
            if birthday and birthday.strip():
                birthday = birthday.strip()
                dt = datetime.datetime.strptime(birthday, "%Y/%m/%d")
                member.birthday = datetime.date(dt.year, dt.month, dt.day)
            member.post_code = post_code.strip().replace("-", "") if post_code and post_code.strip() else None
            member.address1 = address1.strip() if address1 and address1.strip() else None
            member.address2 = address2.strip() if address2 and address2.strip() else None
            member.phone = phone.strip() if phone and phone.strip() and len(phone) <= 1 else None
            member.member_type = int(member_type.strip()) if member_type and member_type.strip() else 0
            if company_name and company_name.strip():
                company_name = company_name.strip()
                if company_name == u"株式会社イー・ビジネス":
                    member.company = self.company
                else:
                    subcontractor = models.Subcontractor.objects.get(name=company_name)
                    member.subcontractor = subcontractor
            member.certificate = certificate.strip() if certificate and certificate.strip() else None
            member.comment = comment.strip() if comment and comment.strip() else None
            member.save()

    def sync_client(self):
        # 取引先
        self.cursor = connection.cursor()
        self.cursor.execute(u"select CustomerName"
                            u"     , JapaneseSpell"
                            u"     , FoundDate"
                            u"     , Capital"
                            u"     , PostCode"
                            u"     , Address1"
                            u"     , Address2"
                            u"     , Tel"
                            u"     , Fax"
                            u"     , Representor"
                            u"     , EmployeeCount"
                            u"     , SaleAmount"
                            u"     , Undertaker"
                            u"     , UndertakerMail"
                            u"     , PaymentType"
                            u"     , PaymentDay"
                            u"     , Remark"
                            u"     , Note"
                            u"     , EBSalesID"
                            u"  from t_customer t1"
                            u" where not exists(select 1 from eb_client t2 where t2.name = t1.CustomerName) "
                            u"   and DeleteFlg = 0;")
        for name, japanese_spell, found_date, capital, post_code, address1, address2, tel, fax, \
            president, employee_count, sale_amount, undertaker, undertaker_mail, \
            payment_type, payment_day, remark, comment, salesperson_id in self.cursor.fetchall():
            client = models.Client()
            client.name = name
            client.japanese_spell = japanese_spell if japanese_spell else None
            if found_date and found_date.strip():
                found_date = found_date.strip()
                dt = datetime.datetime.strptime(found_date, "%Y/%m/%d")
                client.found_date = datetime.date(dt.year, dt.month, dt.day)
            if capital and capital.strip() and re.match(r"^[0-9.,]+$", capital):
                capital = capital.strip().replace(",", "")
                client.capital = long(float(capital))
            client.post_code = post_code.strip().replace("-", "") if post_code and post_code.strip() else None
            client.address1 = address1.strip() if address1 and address1.strip() else None
            client.address2 = address2.strip() if address2 and address2.strip() else None
            client.tel = tel if tel else None
            client.fax = fax if fax else None
            client.president = president if president else None
            if employee_count and employee_count.strip():
                employee_count = employee_count.strip().replace(",", "")
                client.employee_count = int(employee_count)
            if sale_amount and sale_amount.strip():
                sale_amount = sale_amount.strip().replace(",", "")
                client.sale_amount = long(sale_amount)
            client.payment_type = payment_type if payment_type else None
            client.payment_day = payment_day if payment_day else None
            client.remark = remark if remark else None
            client.comment = comment if comment else None
            if salesperson_id and salesperson_id.strip():
                salesperson_id = salesperson_id.strip()
                salesperson = models.Salesperson.objects.get(employee_id=salesperson_id)
                client.salesperson = salesperson
            client.save()
            if undertaker and undertaker.strip():
                undertaker = undertaker.strip()
                lst = models.ClientMember.objects.filter(client=client, name=undertaker)
                if lst.count() == 0:
                    client_member = models.ClientMember()
                    client_member.name = undertaker
                    client_member.email = undertaker_mail if undertaker_mail and undertaker_mail.strip() else None
                    client_member.client = client
                    client_member.save()