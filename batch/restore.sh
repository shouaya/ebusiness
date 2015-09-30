#!/bin/bash
# 機能  :  restore eb inside hr datatables
# 作成  :  shoushou
source /usr/local/src/ebusiness/batch/config.sh
current_date=$(date "+%Y.%m.%d")
mysql -u$EB_DB_USER -p$EB_DB_PASS $EB_DB_NAME < $EB_ROOT/download/$current_date.sql