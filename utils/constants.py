# coding: UTF-8
"""
Created on 2015/09/28

@author: Yang Wanjun
"""
from decimal import Decimal

EXCEL_APPLICATION = "Excel.Application"
EXCEL_FORMAT_EXCEL2003 = 56

REG_DATE_STR = ur"\d{4}([-/.年])\d{1,2}([-/.月])\d{1,2}([日]?)"
REG_DATE_STR2 = ur"\d{4}([-/.年])\d{1,2}([-/.月]?)"
REG_EXCEL_REPLACEMENT = ur"\{\$([A-Z0-9_]+)\$\}"

NAME_BUSINESS_PLAN = u"%02d月営業企画"
NAME_MEMBER_LIST = u"最新要員一覧"
NAME_RESUME = u"EB履歴書_%s_%s"

MARK_POST_CODE = u"〒"

DOWNLOAD_REQUEST = "request"
DOWNLOAD_BUSINESS_PLAN = "business_plan"
DOWNLOAD_MEMBER_LIST = "member_list"
DOWNLOAD_RESUME = "resume"
DOWNLOAD_QUOTATION = "quotation"
DOWNLOAD_ORDER = "order"

ERROR_TEMPLATE_NOT_EXISTS = u"テンプレートファイルが存在しません。"
ERROR_REQUEST_FILE_NOT_EXISTS = u"作成された請求書は存在しません、" \
                                u"サーバーに該当する請求書が存在するのかを確認してください。"
ERROR_CANNOT_GENERATE_2MONTH_BEFORE = u"２ヶ月前の請求書は作成できない"

PROJECT_STAGE = (u"要件定義", u"調査分析",
                 u"基本設計", u"詳細設計",
                 u"開発製造", u"単体試験",
                 u"結合試験", u"総合試験",
                 u"保守運用", u"サポート")

CHOICE_PROJECT_MEMBER_STATUS = ((1, u"提案中"),
                                (2, u"作業確定"))
CHOICE_PROJECT_STATUS = ((1, u"提案"), (2, u"予算審査"), (3, u"予算確定"), (4, u"実施中"), (5, u"完了"))
CHOICE_SKILL_TIME = ((0, u"未経験者可"),
                     (1, u"１年以上"),
                     (2, u"２年以上"),
                     (3, u"３年以上"),
                     (5, u"５年以上"),
                     (10, u"１０年以上"))
CHOICE_DEGREE_TYPE = ((1, u"小・中学校"),
                      (2, u"高等学校"),
                      (3, u"専門学校"),
                      (4, u"高等専門学校"),
                      (5, u"短期大学"),
                      (6, u"大学学部"),
                      (7, u"大学大学院"))
CHOICE_SALESPERSON_TYPE = ((0, u"営業部長"),
                           (5, u"営業担当"),
                           (6, u"取締役"),
                           (7, u"代表取締役社長"))
CHOICE_MEMBER_TYPE = ((1, u"正社員"),
                      (2, u"契約社員"),
                      (3, u"個人事業者"),
                      (4, u"他社技術者"))
CHOICE_PROJECT_ROLE = (("OP", u"OP：ｵﾍﾟﾚｰﾀｰ"),
                       ("PG", u"PG：ﾌﾟﾛｸﾞﾗﾏｰ"),
                       ("SP", u"SP：ｼｽﾃﾑﾌﾟﾛｸﾞﾗﾏｰ"),
                       ("SE", u"SE：ｼｽﾃﾑｴﾝｼﾞﾆｱ"),
                       ("SL", u"SL：ｻﾌﾞﾘｰﾀﾞｰ"),
                       ("L", u"L：ﾘｰﾀﾞｰ"),
                       ("M", u"M：ﾏﾈｰｼﾞｬｰ"))
CHOICE_POSITION = ((4, u"部長"), (5, u"担当部長"),
                   (6, u"課長"), (7, u"担当課長"), (8, u"PM"), (9, u"リーダー"), (10, u"サブリーダー"))
CHOICE_SEX = (('1', u"男"), ('2', u"女"))
CHOICE_MARRIED = (('', u"------"), ('0', u"未婚"), ('1', u"既婚"))
CHOICE_PAYMENT_MONTH = (('1', u"翌月"),
                        ('2', u"翌々月"),
                        ('3', u"３月"),
                        ('4', u"４月"),
                        ('5', u"５月"),
                        ('6', u"６月"))
CHOICE_PAYMENT_DAY = (('01', u'1日'),
                      ('02', u'2日'),
                      ('03', u'3日'),
                      ('04', u'4日'),
                      ('05', u'5日'),
                      ('06', u'6日'),
                      ('07', u'7日'),
                      ('08', u'8日'),
                      ('09', u'9日'),
                      ('10', u'10日'),
                      ('11', u'11日'),
                      ('12', u'12日'),
                      ('13', u'13日'),
                      ('14', u'14日'),
                      ('15', u'15日'),
                      ('16', u'16日'),
                      ('17', u'17日'),
                      ('18', u'18日'),
                      ('19', u'19日'),
                      ('20', u'20日'),
                      ('21', u'21日'),
                      ('22', u'22日'),
                      ('23', u'23日'),
                      ('24', u'24日'),
                      ('25', u'25日'),
                      ('26', u'26日'),
                      ('27', u'27日'),
                      ('28', u'28日'),
                      ('29', u'29日'),
                      ('30', u'30日'),
                      ('99', u'月末'))
CHOICE_ATTENDANCE_YEAR = (('2014', u"2014年"),
                          ('2015', u"2015年"),
                          ('2016', u"2016年"),
                          ('2017', u"2017年"),
                          ('2018', u"2018年"),
                          ('2019', u"2019年"),
                          ('2020', u"2020年"))
CHOICE_ATTENDANCE_MONTH = (('01', u'1月'),
                           ('02', u'2月'),
                           ('03', u'3月'),
                           ('04', u'4月'),
                           ('05', u'5月'),
                           ('06', u'6月'),
                           ('07', u'7月'),
                           ('08', u'8月'),
                           ('09', u'9月'),
                           ('10', u'10月'),
                           ('11', u'11月'),
                           ('12', u'12月'))
CHOICE_ACCOUNT_TYPE = (("1", u"普通預金"),
                       ("2", u"定期預金"),
                       ("3", u"総合口座"),
                       ("4", u"当座預金"),
                       ("5", u"貯蓄預金"),
                       ("6", u"大口定期預金"),
                       ("7", u"積立定期預金"))
CHOICE_ATTENDANCE_TYPE = (('1', u"１５分ごと"),
                          ('2', u"３０分ごと"),
                          ('3', u"１時間ごと"))
CHOICE_TAX_RATE = ((Decimal('0.00'), u"税なし"),
                   (Decimal('0.05'), u"5％"),
                   (Decimal('0.08'), u"8％"))
CHOICE_DECIMAL_TYPE = (('0', u"四捨五入"),
                       ('1', u"切り捨て"))
CHOICE_DEV_LOCATION = (('01', u"東大島"),
                       ('02', u"田町"),
                       ('03', u"府中"),
                       ('04', u"西葛西"))
CHOICE_NOTIFY_TYPE = ((1, u"EBのメールアドレス"),
                      (2, u"個人メールアドレス"),
                      (3, u"EBと個人両方のメールアドレス"))
CHOICE_ISSUE_STATUS = (('1', u"提出中"),
                       ('2', u"対応中"),
                       ('3', u"対応完了"),
                       ('4', u"クローズ"))

xlPart = 2
xlByRows = 1
xlFormulas = -4123
xlNext = 1
xlDown = -4121

URL_SYNC_MEMBERS = u"http://service.e-business.co.jp:8080/EmployeeManagement/api/employeelist?type=json"
URL_CONTRACT = u"http://service.e-business.co.jp:8080/ContractManagement/api/newContract?uid=%s"
