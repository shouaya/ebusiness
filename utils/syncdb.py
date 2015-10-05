# coding: UTF-8
"""
Created on 2015/09/30

@author: Yang Wanjun
"""
import re
import datetime

from django.db import connection
from django.core.exceptions import ObjectDoesNotExist

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
            try:
                subcontractor = models.Subcontractor()
                subcontractor.name = name[0]
                subcontractor.save()
            except:
                pass

    def sync_section(self):
        # 部署
        self.cursor = connection.cursor()
        self.cursor.execute(u"select distinct DeptName"
                            u"  from t_dept t1"
                            u" where not exists( select 1 from eb_section t2 where t2.name = t1.DeptName);")
        for name, in self.cursor.fetchall():
            try:
                section = models.Section()
                section.name = name
                section.company = section.company
                section.save()
            except:
                pass

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

            try:
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
                member.birthday = self.get_date(birthday)
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
            except:
                pass

    def sync_client(self):
        # 取引先
        self.cursor = connection.cursor()
        self.cursor.execute(u"select CustomerId"
                            u"     , CustomerName"
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
                            u" where not exists(select 1 "
                            u"                    from eb_client t2 "
                            u"				     where t2.saletest_customer_id = t1.CustomerID) "
                            u"   and DeleteFlg = 0;")
        for customer_id, name, japanese_spell, found_date, capital, post_code, address1, address2, tel, fax, \
            president, employee_count, sale_amount, undertaker, undertaker_mail, \
            payment_type, payment_day, remark, comment, salesperson_id in self.cursor.fetchall():
            try:
                client = models.Client()
                client.saletest_customer_id = customer_id
                client.name = name
                client.japanese_spell = japanese_spell if japanese_spell else None
                client.found_date = self.get_date(found_date)
                if capital and capital.strip() and re.match(r"^[0-9.,]+$", capital):
                    capital = capital.strip().replace(",", "")
                    client.capital = long(float(capital))
                client.post_code = post_code.strip().replace("-", "").replace(u"ー", "") if post_code and post_code.strip() else None
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
                if undertaker and undertaker.strip() and undertaker != '0':
                    undertaker = undertaker.strip()
                    lst = models.ClientMember.objects.filter(client=client, name=undertaker)
                    if lst.count() == 0:
                        client_member = models.ClientMember()
                        client_member.name = undertaker
                        client_member.email = undertaker_mail if undertaker_mail and undertaker_mail.strip() else None
                        client_member.client = client
                        client_member.save()
            except:
                pass

    def sync_project(self):
        # 案件
        self.cursor = connection.cursor()
        self.cursor.execute(u"SELECT CustomerID"
                            u"     , ContractName"
                            u"     , min(StartDate) as StartDate"
                            u"     , max(EndDate) as EndDate"
                            u"     , Salesman1ID"
                            u"  FROM t_managementbook t1 "
                            u" where not exists ( select 1"
                            u"                      from eb_project t2"
                            u"                      join eb_client t3 on t3.id = t2.client_id"
                            u"                     where t3.saletest_customer_id = t1.CustomerID)"
                            u"   and trim(ContractName) <> ''"
                            u" group by CustomerID, ContractName;")
        for client_id, name, start_date, end_date, salesperson_id in self.cursor.fetchall():
            project = models.Project()
            project.name = name
            project.start_date = self.get_date(start_date)
            project.end_date = self.get_date(end_date)
            project.status = self.get_project_status(project.start_date, project.end_date)
            if client_id:
                try:
                    client = models.Client.objects.get(saletest_customer_id=client_id)
                    project.client = client
                except ObjectDoesNotExist:
                    pass
            if salesperson_id:
                try:
                    salesperson = models.Salesperson.objects.get(employee_id="%06d" % (salesperson_id,))
                    project.salesperson = salesperson
                except ObjectDoesNotExist:
                    pass
            project.save()

            cursor = connection.cursor()
            cursor.execute(u"select EmployeeID"
                           u"     , min(StartDate)"
                           u"     , max(EndDate)"
                           u"     , Price"
                           u"  from t_managementbook t1"
                           u" where t1.CustomerID = %s"
                           u"   and t1.ContractName = %s"
                           u" group by EmployeeID;", [client_id, name])
            for employee_id, start_date2, end_date2, price in cursor.fetchall():
                try:
                    project_member = models.ProjectMember()
                    project_member.project = project
                    project_member.member = models.Member.objects.get(employee_id="%06d" % (employee_id,))
                    project_member.start_date = self.get_date(start_date2)
                    project_member.end_date = self.get_date(end_date2)
                    project_member.status = self.get_project_member_status(project_member.start_date,
                                                                           project_member.end_date)
                    project_member.price = price
                    project_member.save()
                except ObjectDoesNotExist:
                    pass

    def get_date(self, str_date):
        if str_date and str_date.strip():
            str_date = str_date.strip()
            dt = datetime.datetime.strptime(str_date, "%Y/%m/%d")
            return datetime.date(dt.year, dt.month, dt.day)
        else:
            return None

    def get_project_status(self, start_date, end_date):
        if start_date is None or end_date is None:
            return 1
        else:
            now = datetime.date.today()
            if end_date < now:
                return 5
            elif start_date > now:
                return 1
            else:
                return 4

    def get_project_member_status(self, start_date, end_date):
        if start_date is None or end_date is None:
            return 1
        else:
            now = datetime.date.today()
            if end_date < now:
                return 3
            elif start_date > now:
                return 1
            else:
                return 2
