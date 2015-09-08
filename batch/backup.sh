#!/bin/bash
# 機能  :  backup eb datatables
# 作成  :  shoushou
source config.sh
current_date=$(date "+%Y.%m.%d")
mysqldump -u$EB_DB_USER -p$EB_DB_PASS -h$EB_DB_HOST $EB_DB_NAME > $EB_ROOT/backup/$current_date.sql --skip-add-locks