-- MySQL dump 10.13  Distrib 5.6.25, for osx10.10 (x86_64)
--
-- Host: localhost    Database: hr
-- ------------------------------------------------------
-- Server version	5.6.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `T_BankInfo`
--

DROP TABLE IF EXISTS `T_BankInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_BankInfo` (
  `BankInfoId` int(11) NOT NULL AUTO_INCREMENT,
  `CompanyID` int(11) NOT NULL,
  `BankName` varchar(100) NOT NULL,
  `BankCode` varchar(10) NOT NULL,
  `BankBranch` varchar(100) NOT NULL,
  `BankBranchCode` varchar(10) NOT NULL,
  `BankAccountCode` varchar(50) NOT NULL,
  `BankAccountType` varchar(50) NOT NULL,
  `BankAccountHolderName` varchar(100) NOT NULL,
  PRIMARY KEY (`BankInfoId`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_BankInfo`
--

/*!40000 ALTER TABLE `T_BankInfo` DISABLE KEYS */;
INSERT INTO `T_BankInfo` VALUES (1,1,'XXX銀行','0000','XX支店','111','１１１１１１１','普通','カ）イー　ビジネス'),(2,1,'yyyyy','0000','XX支店','111','１１１１１１１','普通','カ）イー　ビジネス');
/*!40000 ALTER TABLE `T_BankInfo` ENABLE KEYS */;

--
-- Table structure for table `T_Bill`
--

DROP TABLE IF EXISTS `T_Bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_Bill` (
  `BillNo` varchar(9) NOT NULL DEFAULT '' COMMENT '請求書番号',
  `BankInfoId` int(11) NOT NULL DEFAULT '1',
  `BillChildNo` varchar(3) DEFAULT '',
  `CustomerID` int(8) DEFAULT NULL COMMENT '顧客ID',
  `BillAmountTotal` decimal(10,0) DEFAULT NULL COMMENT '請求総金額',
  `BillDate` varchar(10) DEFAULT NULL COMMENT '請求日',
  `DeductionItem` varchar(20) DEFAULT NULL COMMENT '控除項目',
  `DeductionCost` decimal(10,0) DEFAULT NULL COMMENT '控除額',
  `DeductionNotes` varchar(20) DEFAULT NULL COMMENT '控除備考',
  `AdditionalItem` varchar(20) DEFAULT NULL COMMENT '追加項目',
  `AdditionalCost` decimal(10,0) DEFAULT NULL COMMENT '追加額',
  `AdditionalNotes` varchar(20) DEFAULT NULL COMMENT '追加備考',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `ReceiptID` int(8) DEFAULT NULL COMMENT '入金ID',
  `ReceiptAmount` decimal(10,0) DEFAULT NULL COMMENT '入金額',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`BillNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_Bill`
--

/*!40000 ALTER TABLE `T_Bill` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_Bill` ENABLE KEYS */;

--
-- Table structure for table `T_CodeMaster`
--

DROP TABLE IF EXISTS `T_CodeMaster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_CodeMaster` (
  `CodeType` varchar(5) NOT NULL DEFAULT '' COMMENT 'コード区分',
  `CodeId` varchar(2) NOT NULL DEFAULT '' COMMENT 'コードID',
  `CodeName` varchar(30) DEFAULT NULL COMMENT 'コード名称',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`CodeType`,`CodeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_CodeMaster`
--

/*!40000 ALTER TABLE `T_CodeMaster` DISABLE KEYS */;
INSERT INTO `T_CodeMaster` VALUES ('00001','1','正社員','0','0000-00-00 00:00:00',NULL,NULL),('00001','2','契約社員','0','0000-00-00 00:00:00',NULL,NULL),('00001','3','個人事業者','0','0000-00-00 00:00:00',NULL,NULL),('00002','1','株式会社イー・ビジネス','0','0000-00-00 00:00:00',NULL,NULL),('CD001','1','正社員','0','0000-00-00 00:00:00',NULL,NULL),('CD001','2','契約社員','0','0000-00-00 00:00:00',NULL,NULL),('CD001','3','個人事業者','0','0000-00-00 00:00:00',NULL,NULL),('CD001','4','他社技術者','0','0000-00-00 00:00:00',NULL,NULL),('CD001','5','営業担当','0','0000-00-00 00:00:00',NULL,NULL),('CD001','6','取締役','0','0000-00-00 00:00:00',NULL,NULL),('CD001','7','代表取締役社長','0','0000-00-00 00:00:00',NULL,NULL),('CD002','0','未処理','0','0000-00-00 00:00:00',NULL,NULL),('CD002','1','処理済','0','0000-00-00 00:00:00',NULL,NULL),('CD003','0','未削除','0','0000-00-00 00:00:00',NULL,NULL),('CD003','1','削除','0','0000-00-00 00:00:00',NULL,NULL),('CD004','0','未発行','0','0000-00-00 00:00:00',NULL,NULL),('CD004','1','発行済','0','0000-00-00 00:00:00',NULL,NULL),('CD005','1','翌月','0','0000-00-00 00:00:00',NULL,NULL),('CD005','2','翌々月','0','0000-00-00 00:00:00',NULL,NULL),('CD005','3','三ヶ月','0','0000-00-00 00:00:00',NULL,NULL),('CD005','4','四ヶ月','0','0000-00-00 00:00:00',NULL,NULL),('CD005','5','五ヶ月','0','0000-00-00 00:00:00',NULL,NULL),('CD005','6','六ヶ月','0','0000-00-00 00:00:00',NULL,NULL),('CD006','01','1日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','02','2日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','03','3日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','04','4日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','05','5日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','06','6日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','07','7日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','08','8日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','09','9日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','10','10日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','11','11日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','12','12日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','13','13日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','14','14日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','15','15日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','16','16日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','17','17日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','18','18日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','19','19日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','20','20日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','21','21日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','22','22日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','23','23日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','24','24日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','25','25日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','26','26日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','27','27日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','28','28日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','29','29日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','30','30日','0','0000-00-00 00:00:00',NULL,NULL),('CD006','99','月末','0','0000-00-00 00:00:00',NULL,NULL),('CD007','1 ','役務請負','0','0000-00-00 00:00:00',NULL,NULL),('CD007','2 ','派遣','0','0000-00-00 00:00:00',NULL,NULL),('CD007','3 ','請負','0','0000-00-00 00:00:00',NULL,NULL),('CD007','4 ','売買','0','0000-00-00 00:00:00',NULL,NULL),('CD008','1 ','月','0','0000-00-00 00:00:00',NULL,NULL),('CD008','2 ','時間','0','0000-00-00 00:00:00',NULL,NULL),('CD008','3 ','一式','0','0000-00-00 00:00:00',NULL,NULL),('CD009','1 ','なし','0','0000-00-00 00:00:00',NULL,NULL),('CD009','2 ','四捨五入','0','0000-00-00 00:00:00',NULL,NULL),('CD009','3 ','小数点以下切り捨て','0','0000-00-00 00:00:00',NULL,NULL),('CD010','0','基本設計','0','0000-00-00 00:00:00',NULL,NULL),('CD010','1','詳細設計','0','0000-00-00 00:00:00',NULL,NULL),('CD010','2','製造','0','0000-00-00 00:00:00',NULL,NULL),('CD011','5','5%','0','2014-02-06 06:35:37','2014-02-06 06:35:37','2014-02-06 06:35:37'),('CD011','8','8%','0','2014-02-06 06:35:37','2014-02-06 06:35:37','2014-02-06 06:35:37'),('CD999','06','仮台帳','0','0000-00-00 00:00:00','2015-05-29 11:38:03',NULL);
/*!40000 ALTER TABLE `T_CodeMaster` ENABLE KEYS */;

--
-- Table structure for table `T_Company`
--

DROP TABLE IF EXISTS `T_Company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_Company` (
  `CompanyID` int(3) NOT NULL AUTO_INCREMENT COMMENT '会社ID',
  `CompanyName` varchar(200) DEFAULT NULL COMMENT '会社名称',
  `PostCode` varchar(10) DEFAULT NULL COMMENT '郵便番号',
  `Address` varchar(200) DEFAULT NULL COMMENT '住所',
  `Representor` varchar(50) DEFAULT NULL COMMENT '代表者',
  `Tel` varchar(20) DEFAULT NULL COMMENT '電話番号',
  `EmployeeID` int(8) DEFAULT NULL COMMENT '営業担当',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`CompanyID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_Company`
--

/*!40000 ALTER TABLE `T_Company` DISABLE KEYS */;
INSERT INTO `T_Company` VALUES (1,'株式会社イー・ビジネス','105-0014','東京都港区芝2-28-8芝2丁目ビル10階','花　   東江','03-6809-3235',245,'0','0000-00-00 00:00:00','2015-04-30 08:02:33',NULL);
/*!40000 ALTER TABLE `T_Company` ENABLE KEYS */;

--
-- Table structure for table `T_Contract`
--

DROP TABLE IF EXISTS `T_Contract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_Contract` (
  `ContractID` int(8) NOT NULL AUTO_INCREMENT COMMENT '契約ID',
  `ContractNo` varchar(50) DEFAULT NULL COMMENT '契約番号',
  `ContractDate` varchar(10) DEFAULT NULL COMMENT '契約日',
  `CustomerID` int(8) DEFAULT NULL COMMENT '顧客ID',
  `OrderNo` varchar(20) DEFAULT NULL COMMENT '注文書番号',
  `EmployType` varchar(1) DEFAULT NULL COMMENT '方式',
  `OrderDate` varchar(10) DEFAULT NULL COMMENT '注文日',
  `ContractName` varchar(50) DEFAULT NULL COMMENT '契約件名',
  `Amount` decimal(10,0) DEFAULT NULL COMMENT '契約金額',
  `Content` varchar(50) DEFAULT NULL COMMENT '内容',
  `Note` varchar(50) DEFAULT NULL COMMENT '備考',
  `StartDate` varchar(10) DEFAULT NULL COMMENT '開始日',
  `EndDate` varchar(10) DEFAULT NULL COMMENT '終了日',
  `Salesman1` int(8) DEFAULT NULL COMMENT '営業担当１',
  `Salesman2` int(8) DEFAULT NULL COMMENT '営業担当２',
  `PaymentType` varchar(10) DEFAULT NULL COMMENT '支払方法',
  `PaymentDay` varchar(10) DEFAULT NULL COMMENT '支払日',
  `FinishFlag` varchar(1) DEFAULT '0' COMMENT '処理済フラグ',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ContractID`)
) ENGINE=InnoDB AUTO_INCREMENT=2226 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_Contract`
--

/*!40000 ALTER TABLE `T_Contract` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_Contract` ENABLE KEYS */;

--
-- Table structure for table `T_ContractDetail`
--

DROP TABLE IF EXISTS `T_ContractDetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_ContractDetail` (
  `ContractID` int(8) NOT NULL COMMENT '契約ID',
  `DetailID` varchar(8) NOT NULL DEFAULT '' COMMENT '契約明細ID',
  `EmployeeID` int(8) DEFAULT NULL COMMENT '技術者ID',
  `Unit` varchar(20) DEFAULT NULL COMMENT '単位',
  `Price` decimal(10,0) DEFAULT NULL COMMENT '単価',
  `Quantity` decimal(10,3) DEFAULT NULL COMMENT '数量',
  `MinHour` decimal(10,2) DEFAULT NULL COMMENT 'Min勤務',
  `MaxHour` decimal(10,2) DEFAULT NULL COMMENT 'Max勤務',
  `MinusUnitPrice` decimal(10,0) DEFAULT NULL COMMENT '減賃金',
  `PlusUnitPrice` decimal(10,0) DEFAULT NULL COMMENT '増賃金',
  `Amount` decimal(10,0) DEFAULT NULL COMMENT '金額',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`DetailID`,`ContractID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_ContractDetail`
--

/*!40000 ALTER TABLE `T_ContractDetail` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_ContractDetail` ENABLE KEYS */;

--
-- Table structure for table `T_Customer`
--

DROP TABLE IF EXISTS `T_Customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_Customer` (
  `CustomerID` int(8) NOT NULL AUTO_INCREMENT COMMENT '顧客ID',
  `CustomerName` varchar(200) DEFAULT NULL COMMENT '顧客名',
  `JapaneseSpell` varchar(200) DEFAULT NULL COMMENT 'フリカナ',
  `Representor` varchar(50) DEFAULT NULL COMMENT '代表者名',
  `FoundDate` varchar(10) DEFAULT NULL COMMENT '設立年月日',
  `Capital` varchar(20) DEFAULT NULL COMMENT '資本金',
  `EmployeeCount` varchar(20) DEFAULT NULL COMMENT '従業員数',
  `SaleAmount` varchar(20) DEFAULT NULL COMMENT '売上高',
  `PostCode` varchar(10) DEFAULT NULL COMMENT '郵便番号',
  `Address1` varchar(200) DEFAULT NULL COMMENT '住所１',
  `Address2` varchar(200) DEFAULT NULL COMMENT '住所２',
  `Tel` varchar(20) DEFAULT NULL COMMENT '電話番号',
  `Fax` varchar(20) DEFAULT NULL COMMENT 'ファックス',
  `Undertaker` varchar(50) DEFAULT NULL COMMENT '担当者',
  `UndertakerMail` varchar(100) DEFAULT NULL COMMENT '担当MAIL',
  `Remark` varchar(2000) DEFAULT NULL COMMENT '評価',
  `Note` varchar(2000) DEFAULT NULL COMMENT '備考',
  `PaymentType` varchar(2) DEFAULT NULL COMMENT '支払方法',
  `PaymentDay` varchar(2) DEFAULT NULL COMMENT '支払日',
  `DataOrder` varchar(8) DEFAULT NULL COMMENT '並び順',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `EBSalesID` int(8) DEFAULT NULL COMMENT 'EB営業担当ID',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=172 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_Customer`
--

/*!40000 ALTER TABLE `T_Customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_Customer` ENABLE KEYS */;

--
-- Table structure for table `T_Dept`
--

DROP TABLE IF EXISTS `T_Dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_Dept` (
  `DeptID` int(8) NOT NULL AUTO_INCREMENT COMMENT '部門ID',
  `DeptName` varchar(200) DEFAULT NULL COMMENT '部門名',
  `LeaderID` int(8) DEFAULT NULL COMMENT 'リーダーID',
  `SubLeaderID` int(8) DEFAULT NULL COMMENT 'サブリーダーID',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`DeptID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_Dept`
--

/*!40000 ALTER TABLE `T_Dept` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_Dept` ENABLE KEYS */;

--
-- Table structure for table `T_Employee`
--

DROP TABLE IF EXISTS `T_Employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_Employee` (
  `EmployeeID` int(8) NOT NULL AUTO_INCREMENT COMMENT '社員ID',
  `EmployeeName` varchar(50) DEFAULT NULL COMMENT '社員名',
  `JapaneseSpell` varchar(50) DEFAULT NULL COMMENT 'フリカナ',
  `Birthday` varchar(10) DEFAULT NULL COMMENT '生年月日',
  `Experience` decimal(10,0) DEFAULT NULL COMMENT '経験年数',
  `Degree` varchar(200) DEFAULT NULL COMMENT '学歴',
  `Certificate` varchar(200) DEFAULT NULL COMMENT '資格',
  `Skill` varchar(1) DEFAULT NULL COMMENT '技術',
  `Language` varchar(200) DEFAULT NULL COMMENT '言語',
  `PostCode` varchar(10) DEFAULT NULL COMMENT '郵便番号',
  `Address1` varchar(200) DEFAULT NULL COMMENT '住所１',
  `Address2` varchar(200) DEFAULT NULL COMMENT '住所２',
  `Tel` varchar(20) DEFAULT NULL COMMENT 'TEL',
  `Company` varchar(200) DEFAULT NULL COMMENT '勤務先',
  `Remark` varchar(2000) DEFAULT NULL COMMENT '評価',
  `Note` varchar(2000) DEFAULT NULL COMMENT '備考',
  `EmployeeType` varchar(1) DEFAULT NULL COMMENT '社員区分',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `DeptID` int(8) DEFAULT NULL,
  `siireID` int(8) DEFAULT NULL,
  `siirePrice` decimal(10,0) DEFAULT NULL,
  `siireSales` varchar(50) DEFAULT NULL,
  `carfare` decimal(10,0) DEFAULT NULL COMMENT '交通費',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`EmployeeID`)
) ENGINE=InnoDB AUTO_INCREMENT=640 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_Employee`
--

/*!40000 ALTER TABLE `T_Employee` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_Employee` ENABLE KEYS */;

--
-- Table structure for table `T_Estimation`
--

DROP TABLE IF EXISTS `T_Estimation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_Estimation` (
  `EstimationID` varchar(8) NOT NULL DEFAULT '' COMMENT '見積ID',
  `EstimationNo` varchar(50) DEFAULT NULL COMMENT '見積番号',
  `EstimationDate` varchar(10) DEFAULT NULL COMMENT '見積日',
  `CustomerID` int(8) DEFAULT NULL COMMENT '顧客ID',
  `RequestNo` varchar(50) DEFAULT NULL COMMENT '依頼番号',
  `RequestDate` varchar(10) DEFAULT NULL COMMENT '依頼日',
  `Title` varchar(100) DEFAULT NULL COMMENT '件名',
  `EmployType` varchar(1) DEFAULT NULL COMMENT '作業形態',
  `Content` varchar(4000) DEFAULT NULL COMMENT '内容',
  `Amount` decimal(10,0) DEFAULT NULL COMMENT '見積金額',
  `Address` varchar(200) DEFAULT NULL COMMENT '場所',
  `Salesman1` varchar(8) DEFAULT NULL COMMENT '営業担当１',
  `Salesman2` varchar(8) DEFAULT NULL COMMENT '営業担当２',
  `Results` varchar(200) DEFAULT NULL COMMENT '成果物',
  `StartDate` varchar(10) DEFAULT NULL COMMENT '開始日',
  `EndDate` varchar(10) DEFAULT NULL COMMENT '終了日',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`EstimationID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_Estimation`
--

/*!40000 ALTER TABLE `T_Estimation` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_Estimation` ENABLE KEYS */;

--
-- Table structure for table `T_EstimationDetail`
--

DROP TABLE IF EXISTS `T_EstimationDetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_EstimationDetail` (
  `EstimationID` varchar(8) NOT NULL DEFAULT '' COMMENT '見積ID',
  `DetailID` varchar(8) DEFAULT NULL COMMENT '見積明細ID',
  `EmployeeID` int(8) DEFAULT NULL COMMENT '技術者ID',
  `Unit` varchar(20) DEFAULT NULL COMMENT '単位',
  `Price` decimal(10,0) DEFAULT NULL COMMENT '単価',
  `Quantity` decimal(10,0) DEFAULT NULL COMMENT '数量',
  `MinHour` decimal(10,0) DEFAULT NULL COMMENT 'Min勤務',
  `MaxHour` decimal(10,0) DEFAULT NULL COMMENT 'Max勤務',
  `MinusUnitPrice` decimal(10,0) DEFAULT NULL COMMENT '減',
  `PlusUnitPrice` decimal(10,0) DEFAULT NULL COMMENT '増',
  `Amount` decimal(10,0) DEFAULT NULL COMMENT '金額',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`EstimationID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_EstimationDetail`
--

/*!40000 ALTER TABLE `T_EstimationDetail` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_EstimationDetail` ENABLE KEYS */;

--
-- Table structure for table `T_ManagementBook`
--

DROP TABLE IF EXISTS `T_ManagementBook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_ManagementBook` (
  `ManagementID` int(8) NOT NULL AUTO_INCREMENT COMMENT '管理ID',
  `EmployeeID` int(8) NOT NULL DEFAULT '0' COMMENT '社員ID',
  `Salesman1ID` int(8) NOT NULL DEFAULT '0' COMMENT '営業担当１ID',
  `Salesman2ID` int(8) DEFAULT NULL COMMENT '営業担当２ID',
  `DeptName` varchar(200) DEFAULT NULL COMMENT '所属部門',
  `siireName` varchar(200) DEFAULT NULL COMMENT '仕入先名',
  `siireSales` varchar(50) DEFAULT NULL COMMENT '仕入先担当',
  `CustomerID` int(8) NOT NULL DEFAULT '0' COMMENT '顧客ID',
  `CustSalesman` varchar(50) NOT NULL DEFAULT '' COMMENT '顧客窓口',
  `ContractName` varchar(50) DEFAULT NULL COMMENT '契約件名',
  `ProjectName` varchar(50) DEFAULT NULL COMMENT '作業工程',
  `WorkAddr` varchar(50) DEFAULT NULL COMMENT '現場',
  `WorkMonth` varchar(7) NOT NULL DEFAULT '' COMMENT '稼働月',
  `StartDate` varchar(10) NOT NULL DEFAULT '' COMMENT '開始日',
  `EndDate` varchar(10) NOT NULL DEFAULT '' COMMENT '終了日',
  `Amount` decimal(10,0) NOT NULL DEFAULT '0' COMMENT '売上',
  `MinHour` decimal(10,2) DEFAULT NULL COMMENT '稼働下限',
  `MaxHour` decimal(10,2) DEFAULT NULL COMMENT '稼働上限',
  `MinusUnitPrice` decimal(10,0) DEFAULT NULL COMMENT '控除単価',
  `PlusUnitPrice` decimal(10,0) DEFAULT NULL COMMENT '超過単価',
  `Quantity` decimal(10,3) NOT NULL DEFAULT '0.000' COMMENT '日割計算',
  `PaymentType` varchar(10) DEFAULT '' COMMENT '支払方法',
  `PaymentDay` varchar(10) DEFAULT '' COMMENT '支払日',
  `TranExpense` decimal(10,0) DEFAULT NULL COMMENT '交通費',
  `Price` decimal(10,0) DEFAULT NULL COMMENT '単価',
  `Unit` varchar(20) DEFAULT NULL COMMENT '単位',
  `Memo` varchar(50) DEFAULT NULL COMMENT '備考',
  `OrderDate` varchar(10) DEFAULT NULL COMMENT '注文書届日',
  `OrderNo` varchar(20) DEFAULT NULL COMMENT '注文書番号',
  `UpdateFlg` varchar(1) NOT NULL DEFAULT '0',
  `DeleteFlg` varchar(1) NOT NULL DEFAULT '0',
  `ContractID` int(8) DEFAULT NULL,
  `DetailID` int(8) DEFAULT NULL,
  `Cost` int(11) NOT NULL,
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ManagementID`)
) ENGINE=InnoDB AUTO_INCREMENT=11673 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_ManagementBook`
--

/*!40000 ALTER TABLE `T_ManagementBook` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_ManagementBook` ENABLE KEYS */;

--
-- Table structure for table `T_OperateLog`
--

DROP TABLE IF EXISTS `T_OperateLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_OperateLog` (
  `OperateLogID` int(11) NOT NULL AUTO_INCREMENT COMMENT '操作ID',
  `TableName` varchar(50) NOT NULL COMMENT 'テーブル名',
  `UserID` varchar(50) NOT NULL,
  `Operate` varchar(200) NOT NULL COMMENT '操作',
  `LogTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '時間',
  PRIMARY KEY (`OperateLogID`)
) ENGINE=MyISAM AUTO_INCREMENT=28549 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_OperateLog`
--

/*!40000 ALTER TABLE `T_OperateLog` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_OperateLog` ENABLE KEYS */;

--
-- Table structure for table `T_PcCodeMaster`
--

DROP TABLE IF EXISTS `T_PcCodeMaster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_PcCodeMaster` (
  `PcCode` varchar(50) NOT NULL,
  `DeleteFlg` varchar(1) NOT NULL DEFAULT '0',
  `PcIP` varchar(64) NOT NULL,
  `PcName` varchar(32) NOT NULL,
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`PcCode`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_PcCodeMaster`
--

/*!40000 ALTER TABLE `T_PcCodeMaster` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_PcCodeMaster` ENABLE KEYS */;

--
-- Table structure for table `T_Receipt`
--

DROP TABLE IF EXISTS `T_Receipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_Receipt` (
  `ReceiptID` int(8) NOT NULL AUTO_INCREMENT COMMENT '入金番号',
  `CustomerID` varchar(50) DEFAULT NULL COMMENT '顧客ID',
  `ReceiptAmount` decimal(10,0) DEFAULT NULL COMMENT '入金額',
  `ReceiptDate` varchar(10) DEFAULT NULL COMMENT '入金日',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ReceiptID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_Receipt`
--

/*!40000 ALTER TABLE `T_Receipt` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_Receipt` ENABLE KEYS */;

--
-- Table structure for table `T_Sale`
--

DROP TABLE IF EXISTS `T_Sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_Sale` (
  `SaleID` int(8) NOT NULL AUTO_INCREMENT COMMENT '売上ID',
  `SaleNo` varchar(50) DEFAULT NULL COMMENT '売上番号',
  `SaleDate` varchar(10) DEFAULT NULL COMMENT '売上日',
  `CustomerID` int(8) DEFAULT NULL COMMENT '顧客ID',
  `ContractID` int(8) NOT NULL DEFAULT '0' COMMENT '契約ID',
  `StartDate` varchar(10) DEFAULT NULL COMMENT '開始日',
  `EndDate` varchar(10) DEFAULT NULL COMMENT '終了日',
  `SaleAmount` decimal(10,0) DEFAULT NULL COMMENT '売上金額',
  `Content` varchar(50) DEFAULT NULL,
  `Note` varchar(50) DEFAULT NULL,
  `Salesman1` int(8) DEFAULT NULL,
  `Salesman2` int(8) DEFAULT NULL,
  `PaymentSite` varchar(10) DEFAULT NULL COMMENT '支払サイト',
  `BillNo` varchar(9) DEFAULT NULL,
  `BillChildNo` varchar(3) DEFAULT NULL,
  `BillFlag` varchar(1) DEFAULT '0' COMMENT '請求書発行済フラグ',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`SaleID`,`ContractID`)
) ENGINE=InnoDB AUTO_INCREMENT=2360 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_Sale`
--

/*!40000 ALTER TABLE `T_Sale` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_Sale` ENABLE KEYS */;

--
-- Table structure for table `T_SaleAttatchment`
--

DROP TABLE IF EXISTS `T_SaleAttatchment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_SaleAttatchment` (
  `AttatchID` int(8) NOT NULL COMMENT '付紙ID',
  `SaleID` int(8) NOT NULL COMMENT '売上ID',
  `MinusItem` varchar(200) DEFAULT NULL COMMENT '控除項目',
  `MinusAmount` decimal(10,0) DEFAULT NULL COMMENT '控除金額',
  `MinusNote` varchar(200) DEFAULT NULL COMMENT '控除備考',
  `PlusItem` varchar(200) DEFAULT NULL COMMENT '追加項目',
  `PlusAmount` decimal(10,0) DEFAULT NULL COMMENT '追加金額',
  `PlusNote` varchar(200) DEFAULT NULL COMMENT '追加備考',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`SaleID`,`AttatchID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_SaleAttatchment`
--

/*!40000 ALTER TABLE `T_SaleAttatchment` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_SaleAttatchment` ENABLE KEYS */;

--
-- Table structure for table `T_SaleDetail`
--

DROP TABLE IF EXISTS `T_SaleDetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_SaleDetail` (
  `SaleID` int(8) NOT NULL COMMENT '売上ID',
  `SaleDetailID` varchar(8) NOT NULL DEFAULT '' COMMENT '売上明細番号',
  `EmployeeID` int(8) DEFAULT NULL COMMENT '技術者ID',
  `Unit` varchar(20) DEFAULT NULL,
  `Price` decimal(10,0) DEFAULT NULL,
  `WorkTime` decimal(10,2) DEFAULT NULL COMMENT '作業時間',
  `Rate` decimal(10,3) DEFAULT NULL COMMENT '率',
  `MinHour` decimal(10,2) DEFAULT NULL,
  `MaxHour` decimal(10,2) DEFAULT NULL,
  `MinusUnitPrice` decimal(10,0) DEFAULT NULL,
  `PlusUnitPrice` decimal(10,0) DEFAULT NULL,
  `Amount` decimal(10,0) DEFAULT NULL COMMENT '金額',
  `OtherAmount` decimal(10,0) DEFAULT NULL COMMENT 'その他',
  `purchase_carfare` decimal(10,0) NOT NULL COMMENT '交通費',
  `purchase_commuting` varchar(200) NOT NULL COMMENT '通勤区間',
  `purchase_price` decimal(10,0) NOT NULL COMMENT '仕入原価',
  `purchase_note` varchar(1000) NOT NULL COMMENT '備考',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`SaleID`,`SaleDetailID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_SaleDetail`
--

/*!40000 ALTER TABLE `T_SaleDetail` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_SaleDetail` ENABLE KEYS */;

--
-- Table structure for table `T_Siire`
--

DROP TABLE IF EXISTS `T_Siire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_Siire` (
  `siireID` int(8) NOT NULL AUTO_INCREMENT COMMENT '仕入先ID',
  `siireName` varchar(200) DEFAULT NULL COMMENT '仕入先名',
  `siireSales` varchar(50) DEFAULT NULL COMMENT '仕入先担当',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`siireID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_Siire`
--

/*!40000 ALTER TABLE `T_Siire` DISABLE KEYS */;
/*!40000 ALTER TABLE `T_Siire` ENABLE KEYS */;

--
-- Table structure for table `T_User`
--

DROP TABLE IF EXISTS `T_User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `T_User` (
  `UserID` varchar(50) NOT NULL COMMENT 'ユーザーID',
  `Passwrod` varchar(100) NOT NULL COMMENT 'パスワード',
  `UserName` varchar(100) DEFAULT NULL COMMENT 'ユーザー名',
  `RegistDate` varchar(10) DEFAULT NULL COMMENT '登録日',
  `DeleteFlg` varchar(1) DEFAULT '0' COMMENT '削除フラグ',
  `InsertTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NULL DEFAULT NULL,
  `DeleteTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `T_User`
--

/*!40000 ALTER TABLE `T_User` DISABLE KEYS */;
INSERT INTO `T_User` VALUES ('admin','E10ADC3949BA59ABBE56E057F20F883E','admin','2014-02-26','0','2014-02-26 08:17:14','2014-02-26 08:17:14','2014-02-26 08:17:14');
/*!40000 ALTER TABLE `T_User` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-09-09  3:58:09
