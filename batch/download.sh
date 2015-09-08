#!/bin/bash
# 機能  :  download last hr datatables
# 作成  :  shoushou
source config.sh
current_date=$(date "+%Y.%m.%d")
mysqldump -u$HR_DB_USER -p$HR_DB_PASS -h$HR_DB_HOST $HR_DB_NAME> $EB_ROOT/download/$current_date.sql --skip-add-locks