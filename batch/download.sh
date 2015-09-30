#!/bin/bash
# 機能  :  download last hr datatables
# 作成  :  shoushou
source /usr/local/src/ebusiness/batch/config.sh
current_date=$(date "+%Y.%m.%d")
mysqldump -u$HR_DB_USER -p$HR_DB_PASS -h$HR_DB_HOST -P$HR_DB_PORT $HR_DB_NAME>$EB_ROOT/download/$current_date.sql --skip-add-locks --ssl --ssl-cert=$EB_ROOT/database/client-cert.pem --ssl-key=$EB_ROOT/database/client-key.pem --ssl-cipher=AES128-SHA