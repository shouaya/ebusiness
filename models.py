# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class ActEvtLog(models.Model):
    log_nr_field = models.BigIntegerField(db_column='LOG_NR_', primary_key=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    type_field = models.CharField(db_column='TYPE_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_def_id_field = models.CharField(db_column='PROC_DEF_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    execution_id_field = models.CharField(db_column='EXECUTION_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    time_stamp_field = models.DateTimeField(db_column='TIME_STAMP_')  # Field name made lowercase. Field renamed because it ended with '_'.
    user_id_field = models.CharField(db_column='USER_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    data_field = models.TextField(db_column='DATA_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    lock_owner_field = models.CharField(db_column='LOCK_OWNER_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    lock_time_field = models.DateTimeField(db_column='LOCK_TIME_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    is_processed_field = models.IntegerField(db_column='IS_PROCESSED_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_EVT_LOG'


class ActGeBytearray(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    deployment_id_field = models.ForeignKey('ActReDeployment', db_column='DEPLOYMENT_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    bytes_field = models.TextField(db_column='BYTES_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    generated_field = models.IntegerField(db_column='GENERATED_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_GE_BYTEARRAY'


class ActGeProperty(models.Model):
    name_field = models.CharField(db_column='NAME_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    value_field = models.CharField(db_column='VALUE_', max_length=300, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_GE_PROPERTY'


class ActHiActinst(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_def_id_field = models.CharField(db_column='PROC_DEF_ID_', max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.BigIntegerField(db_column='PROC_INST_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    execution_id_field = models.BigIntegerField(db_column='EXECUTION_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    act_id_field = models.CharField(db_column='ACT_ID_', max_length=255)  # Field name made lowercase. Field renamed because it ended with '_'.
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    call_proc_inst_id_field = models.CharField(db_column='CALL_PROC_INST_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    act_name_field = models.CharField(db_column='ACT_NAME_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    act_type_field = models.CharField(db_column='ACT_TYPE_', max_length=255)  # Field name made lowercase. Field renamed because it ended with '_'.
    assignee_field = models.BigIntegerField(db_column='ASSIGNEE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    start_time_field = models.DateTimeField(db_column='START_TIME_')  # Field name made lowercase. Field renamed because it ended with '_'.
    end_time_field = models.DateTimeField(db_column='END_TIME_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    isstart = models.IntegerField(db_column='ISSTART', blank=True, null=True)  # Field name made lowercase.
    duration_field = models.BigIntegerField(db_column='DURATION_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_HI_ACTINST'


class ActHiAttachment(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    user_id_field = models.CharField(db_column='USER_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    description_field = models.CharField(db_column='DESCRIPTION_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    type_field = models.CharField(db_column='TYPE_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    url_field = models.CharField(db_column='URL_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    content_id_field = models.CharField(db_column='CONTENT_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_HI_ATTACHMENT'


class ActHiComment(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    type_field = models.CharField(db_column='TYPE_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    time_field = models.DateTimeField(db_column='TIME_')  # Field name made lowercase. Field renamed because it ended with '_'.
    user_id_field = models.CharField(db_column='USER_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    action_field = models.CharField(db_column='ACTION_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    message_field = models.CharField(db_column='MESSAGE_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    full_msg_field = models.TextField(db_column='FULL_MSG_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_HI_COMMENT'


class ActHiDetail(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    type_field = models.CharField(db_column='TYPE_', max_length=255)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    execution_id_field = models.CharField(db_column='EXECUTION_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    act_inst_id_field = models.CharField(db_column='ACT_INST_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=255)  # Field name made lowercase. Field renamed because it ended with '_'.
    var_type_field = models.CharField(db_column='VAR_TYPE_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    time_field = models.DateTimeField(db_column='TIME_')  # Field name made lowercase. Field renamed because it ended with '_'.
    bytearray_id_field = models.CharField(db_column='BYTEARRAY_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    double_field = models.FloatField(db_column='DOUBLE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    long_field = models.BigIntegerField(db_column='LONG_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    text_field = models.CharField(db_column='TEXT_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    text2_field = models.CharField(db_column='TEXT2_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_HI_DETAIL'


class ActHiIdentitylink(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    group_id_field = models.CharField(db_column='GROUP_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    type_field = models.CharField(db_column='TYPE_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    user_id_field = models.CharField(db_column='USER_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_HI_IDENTITYLINK'


class ActHiProcinst(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.BigIntegerField(db_column='PROC_INST_ID_', unique=True, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    business_key_field = models.CharField(db_column='BUSINESS_KEY_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_def_id_field = models.CharField(db_column='PROC_DEF_ID_', max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    start_time_field = models.DateTimeField(db_column='START_TIME_')  # Field name made lowercase. Field renamed because it ended with '_'.
    end_time_field = models.DateTimeField(db_column='END_TIME_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    duration_field = models.BigIntegerField(db_column='DURATION_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    start_user_id_field = models.BigIntegerField(db_column='START_USER_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    start_act_id_field = models.CharField(db_column='START_ACT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    end_act_id_field = models.CharField(db_column='END_ACT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    super_process_instance_id_field = models.BigIntegerField(db_column='SUPER_PROCESS_INSTANCE_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    delete_reason_field = models.CharField(db_column='DELETE_REASON_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_HI_PROCINST'


class ActHiTaskinst(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_def_id_field = models.CharField(db_column='PROC_DEF_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    task_def_key_field = models.CharField(db_column='TASK_DEF_KEY_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.BigIntegerField(db_column='PROC_INST_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    execution_id_field = models.BigIntegerField(db_column='EXECUTION_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    parent_task_id_field = models.BigIntegerField(db_column='PARENT_TASK_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    description_field = models.CharField(db_column='DESCRIPTION_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    owner_field = models.BigIntegerField(db_column='OWNER_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    assignee_field = models.BigIntegerField(db_column='ASSIGNEE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    start_time_field = models.DateTimeField(db_column='START_TIME_')  # Field name made lowercase. Field renamed because it ended with '_'.
    claim_time_field = models.DateTimeField(db_column='CLAIM_TIME_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    end_time_field = models.DateTimeField(db_column='END_TIME_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    duration_field = models.BigIntegerField(db_column='DURATION_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    delete_reason_field = models.CharField(db_column='DELETE_REASON_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    priority_field = models.IntegerField(db_column='PRIORITY_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    due_date_field = models.DateTimeField(db_column='DUE_DATE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    form_key_field = models.CharField(db_column='FORM_KEY_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    category_field = models.CharField(db_column='CATEGORY_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_HI_TASKINST'


class ActHiVarinst(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    execution_id_field = models.CharField(db_column='EXECUTION_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=255)  # Field name made lowercase. Field renamed because it ended with '_'.
    var_type_field = models.CharField(db_column='VAR_TYPE_', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    bytearray_id_field = models.CharField(db_column='BYTEARRAY_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    double_field = models.FloatField(db_column='DOUBLE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    long_field = models.BigIntegerField(db_column='LONG_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    text_field = models.CharField(db_column='TEXT_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    text2_field = models.CharField(db_column='TEXT2_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    create_time_field = models.DateTimeField(db_column='CREATE_TIME_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    last_updated_time_field = models.DateTimeField(db_column='LAST_UPDATED_TIME_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_HI_VARINST'


class ActIdGroup(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    type_field = models.CharField(db_column='TYPE_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_ID_GROUP'


class ActIdInfo(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    user_id_field = models.CharField(db_column='USER_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    type_field = models.CharField(db_column='TYPE_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    key_field = models.CharField(db_column='KEY_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    value_field = models.CharField(db_column='VALUE_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    password_field = models.TextField(db_column='PASSWORD_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    parent_id_field = models.CharField(db_column='PARENT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_ID_INFO'


class ActIdMembership(models.Model):
    user_id_field = models.ForeignKey('ActIdUser', db_column='USER_ID_')  # Field name made lowercase. Field renamed because it ended with '_'.
    group_id_field = models.ForeignKey(ActIdGroup, db_column='GROUP_ID_')  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_ID_MEMBERSHIP'
        unique_together = (('USER_ID_', 'GROUP_ID_'),)


class ActIdUser(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    first_field = models.CharField(db_column='FIRST_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    last_field = models.CharField(db_column='LAST_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    email_field = models.CharField(db_column='EMAIL_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    pwd_field = models.CharField(db_column='PWD_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    picture_id_field = models.CharField(db_column='PICTURE_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_ID_USER'


class ActReDeployment(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    category_field = models.CharField(db_column='CATEGORY_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    deploy_time_field = models.DateTimeField(db_column='DEPLOY_TIME_')  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_RE_DEPLOYMENT'


class ActReModel(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    key_field = models.CharField(db_column='KEY_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    category_field = models.CharField(db_column='CATEGORY_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    create_time_field = models.DateTimeField(db_column='CREATE_TIME_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    last_update_time_field = models.DateTimeField(db_column='LAST_UPDATE_TIME_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    version_field = models.IntegerField(db_column='VERSION_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    meta_info_field = models.CharField(db_column='META_INFO_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    deployment_id_field = models.ForeignKey(ActReDeployment, db_column='DEPLOYMENT_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    editor_source_value_id_field = models.CharField(db_column='EDITOR_SOURCE_VALUE_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    editor_source_extra_value_id_field = models.CharField(db_column='EDITOR_SOURCE_EXTRA_VALUE_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_RE_MODEL'


class ActReProcdef(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    category_field = models.CharField(db_column='CATEGORY_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    key_field = models.CharField(db_column='KEY_', max_length=255)  # Field name made lowercase. Field renamed because it ended with '_'.
    version_field = models.IntegerField(db_column='VERSION_')  # Field name made lowercase. Field renamed because it ended with '_'.
    deployment_id_field = models.BigIntegerField(db_column='DEPLOYMENT_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    resource_name_field = models.CharField(db_column='RESOURCE_NAME_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    dgrm_resource_name_field = models.CharField(db_column='DGRM_RESOURCE_NAME_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    description_field = models.CharField(db_column='DESCRIPTION_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    has_start_form_key_field = models.IntegerField(db_column='HAS_START_FORM_KEY_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    suspension_state_field = models.IntegerField(db_column='SUSPENSION_STATE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_RE_PROCDEF'
        unique_together = (('KEY_', 'VERSION_', 'TENANT_ID_'),)


class ActRuEventSubscr(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    event_type_field = models.CharField(db_column='EVENT_TYPE_', max_length=255)  # Field name made lowercase. Field renamed because it ended with '_'.
    event_name_field = models.CharField(db_column='EVENT_NAME_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    execution_id_field = models.ForeignKey('ActRuExecution', db_column='EXECUTION_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    activity_id_field = models.CharField(db_column='ACTIVITY_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    configuration_field = models.CharField(db_column='CONFIGURATION_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    created_field = models.DateTimeField(db_column='CREATED_')  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_def_id_field = models.CharField(db_column='PROC_DEF_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_RU_EVENT_SUBSCR'


class ActRuExecution(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.ForeignKey('self', db_column='PROC_INST_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    business_key_field = models.CharField(db_column='BUSINESS_KEY_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    parent_id_field = models.ForeignKey('self', db_column='PARENT_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_def_id_field = models.ForeignKey(ActReProcdef, db_column='PROC_DEF_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    super_exec_field = models.ForeignKey('self', db_column='SUPER_EXEC_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    act_id_field = models.CharField(db_column='ACT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    is_active_field = models.IntegerField(db_column='IS_ACTIVE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    is_concurrent_field = models.IntegerField(db_column='IS_CONCURRENT_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    is_scope_field = models.IntegerField(db_column='IS_SCOPE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    is_event_scope_field = models.IntegerField(db_column='IS_EVENT_SCOPE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    suspension_state_field = models.IntegerField(db_column='SUSPENSION_STATE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    cached_ent_state_field = models.IntegerField(db_column='CACHED_ENT_STATE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_RU_EXECUTION'


class ActRuIdentitylink(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    group_id_field = models.BigIntegerField(db_column='GROUP_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    type_field = models.CharField(db_column='TYPE_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    user_id_field = models.BigIntegerField(db_column='USER_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    task_id_field = models.ForeignKey('ActRuTask', db_column='TASK_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_def_id_field = models.ForeignKey(ActReProcdef, db_column='PROC_DEF_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_RU_IDENTITYLINK'


class ActRuJob(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    type_field = models.CharField(db_column='TYPE_', max_length=255)  # Field name made lowercase. Field renamed because it ended with '_'.
    lock_exp_time_field = models.DateTimeField(db_column='LOCK_EXP_TIME_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    lock_owner_field = models.CharField(db_column='LOCK_OWNER_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    exclusive_field = models.IntegerField(db_column='EXCLUSIVE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    execution_id_field = models.CharField(db_column='EXECUTION_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    process_instance_id_field = models.CharField(db_column='PROCESS_INSTANCE_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_def_id_field = models.CharField(db_column='PROC_DEF_ID_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    retries_field = models.IntegerField(db_column='RETRIES_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    exception_stack_id_field = models.ForeignKey(ActGeBytearray, db_column='EXCEPTION_STACK_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    exception_msg_field = models.CharField(db_column='EXCEPTION_MSG_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    duedate_field = models.DateTimeField(db_column='DUEDATE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    repeat_field = models.CharField(db_column='REPEAT_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    handler_type_field = models.CharField(db_column='HANDLER_TYPE_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    handler_cfg_field = models.CharField(db_column='HANDLER_CFG_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_RU_JOB'


class ActRuTask(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    execution_id_field = models.ForeignKey(ActRuExecution, db_column='EXECUTION_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.ForeignKey(ActRuExecution, db_column='PROC_INST_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_def_id_field = models.ForeignKey(ActReProcdef, db_column='PROC_DEF_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    parent_task_id_field = models.BigIntegerField(db_column='PARENT_TASK_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    description_field = models.CharField(db_column='DESCRIPTION_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    task_def_key_field = models.CharField(db_column='TASK_DEF_KEY_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    owner_field = models.BigIntegerField(db_column='OWNER_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    assignee_field = models.BigIntegerField(db_column='ASSIGNEE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    delegation_field = models.CharField(db_column='DELEGATION_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    priority_field = models.IntegerField(db_column='PRIORITY_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    create_time_field = models.DateTimeField(db_column='CREATE_TIME_')  # Field name made lowercase. Field renamed because it ended with '_'.
    due_date_field = models.DateTimeField(db_column='DUE_DATE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    category_field = models.CharField(db_column='CATEGORY_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    suspension_state_field = models.IntegerField(db_column='SUSPENSION_STATE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_RU_TASK'


class ActRuVariable(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    type_field = models.CharField(db_column='TYPE_', max_length=255)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=255)  # Field name made lowercase. Field renamed because it ended with '_'.
    execution_id_field = models.ForeignKey(ActRuExecution, db_column='EXECUTION_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    proc_inst_id_field = models.ForeignKey(ActRuExecution, db_column='PROC_INST_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    task_id_field = models.BigIntegerField(db_column='TASK_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    bytearray_id_field = models.ForeignKey(ActGeBytearray, db_column='BYTEARRAY_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    double_field = models.FloatField(db_column='DOUBLE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    long_field = models.BigIntegerField(db_column='LONG_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    text_field = models.CharField(db_column='TEXT_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    text2_field = models.CharField(db_column='TEXT2_', max_length=4000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ACT_RU_VARIABLE'


class BpmAgentCondition(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    settingid = models.BigIntegerField(db_column='SETTINGID', blank=True, null=True)  # Field name made lowercase.
    con = models.CharField(db_column='CON', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  # Field name made lowercase.
    agentid = models.BigIntegerField(db_column='AGENTID', blank=True, null=True)  # Field name made lowercase.
    agent = models.CharField(db_column='AGENT', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_AGENT_CONDITION'


class BpmAgentDef(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    settingid = models.BigIntegerField(db_column='SETTINGID', blank=True, null=True)  # Field name made lowercase.
    flowkey = models.CharField(db_column='FLOWKEY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flowname = models.CharField(db_column='FLOWNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_AGENT_DEF'


class BpmAgentSetting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    authid = models.BigIntegerField(db_column='AUTHID', blank=True, null=True)  # Field name made lowercase.
    authname = models.CharField(db_column='AUTHNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='STARTDATE')  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='ENDDATE', blank=True, null=True)  # Field name made lowercase.
    enabled = models.SmallIntegerField(db_column='ENABLED', blank=True, null=True)  # Field name made lowercase.
    authtype = models.SmallIntegerField(db_column='AUTHTYPE', blank=True, null=True)  # Field name made lowercase.
    agentid = models.BigIntegerField(db_column='AGENTID', blank=True, null=True)  # Field name made lowercase.
    agent = models.CharField(db_column='AGENT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    flowkey = models.CharField(db_column='FLOWKEY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    flowname = models.CharField(db_column='FLOWNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_AGENT_SETTING'


class BpmApprovalItem(models.Model):
    itemid = models.BigIntegerField(db_column='ITEMID', primary_key=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    defkey = models.CharField(db_column='DEFKEY', max_length=128, blank=True, null=True)  # Field name made lowercase.
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  # Field name made lowercase.
    type = models.SmallIntegerField(db_column='TYPE', blank=True, null=True)  # Field name made lowercase.
    expression = models.CharField(db_column='EXPRESSION', max_length=3000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_APPROVAL_ITEM'


class BpmBusLink(models.Model):
    bus_id = models.BigIntegerField(db_column='BUS_ID')  # Field name made lowercase.
    bus_form_table = models.CharField(db_column='BUS_FORM_TABLE', max_length=255)  # Field name made lowercase.
    bus_pk = models.BigIntegerField(db_column='BUS_PK', blank=True, null=True)  # Field name made lowercase.
    bus_pkstr = models.CharField(db_column='BUS_PKSTR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bus_def_id = models.BigIntegerField(db_column='BUS_DEF_ID', blank=True, null=True)  # Field name made lowercase.
    bus_flow_runid = models.BigIntegerField(db_column='BUS_FLOW_RUNID', blank=True, null=True)  # Field name made lowercase.
    bus_creator_id = models.BigIntegerField(db_column='BUS_CREATOR_ID', blank=True, null=True)  # Field name made lowercase.
    bus_creator = models.CharField(db_column='BUS_CREATOR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bus_org_id = models.BigIntegerField(db_column='BUS_ORG_ID', blank=True, null=True)  # Field name made lowercase.
    bus_org_name = models.CharField(db_column='BUS_ORG_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bus_createtime = models.DateTimeField(db_column='BUS_CREATETIME')  # Field name made lowercase.
    bus_updid = models.BigIntegerField(db_column='BUS_UPDID', blank=True, null=True)  # Field name made lowercase.
    bus_upd = models.CharField(db_column='BUS_UPD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bus_updtime = models.DateTimeField(db_column='BUS_UPDTIME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_BUS_LINK'
        unique_together = (('BUS_ID', 'BUS_FORM_TABLE'),)


class BpmCommonWsParams(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    setid = models.BigIntegerField(db_column='SETID')  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    param_type = models.IntegerField(db_column='PARAM_TYPE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=400, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_COMMON_WS_PARAMS'


class BpmCommonWsSet(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=200)  # Field name made lowercase.
    wsdl_url = models.CharField(db_column='WSDL_URL', max_length=400, blank=True, null=True)  # Field name made lowercase.
    document = models.TextField(db_column='DOCUMENT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_COMMON_WS_SET'


class BpmCommuReceiver(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    opinionid = models.BigIntegerField(db_column='OPINIONID', blank=True, null=True)  # Field name made lowercase.
    recevierid = models.BigIntegerField(db_column='RECEVIERID', blank=True, null=True)  # Field name made lowercase.
    receivername = models.CharField(db_column='RECEIVERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    receivetime = models.DateTimeField(db_column='RECEIVETIME')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.
    feedbacktime = models.DateTimeField(db_column='FEEDBACKTIME')  # Field name made lowercase.
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_COMMU_RECEIVER'


class BpmDataTemplate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tableid = models.BigIntegerField(db_column='TABLEID', blank=True, null=True)  # Field name made lowercase.
    formkey = models.BigIntegerField(db_column='FORMKEY', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=300, blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    style = models.SmallIntegerField(db_column='STYLE', blank=True, null=True)  # Field name made lowercase.
    needpage = models.SmallIntegerField(db_column='NEEDPAGE', blank=True, null=True)  # Field name made lowercase.
    pagesize = models.SmallIntegerField(db_column='PAGESIZE', blank=True, null=True)  # Field name made lowercase.
    templatealias = models.CharField(db_column='TEMPLATEALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    templatehtml = models.TextField(db_column='TEMPLATEHTML', blank=True, null=True)  # Field name made lowercase.
    displayfield = models.TextField(db_column='DISPLAYFIELD', blank=True, null=True)  # Field name made lowercase.
    sortfield = models.CharField(db_column='SORTFIELD', max_length=200, blank=True, null=True)  # Field name made lowercase.
    conditionfield = models.TextField(db_column='CONDITIONFIELD', blank=True, null=True)  # Field name made lowercase.
    managefield = models.CharField(db_column='MANAGEFIELD', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    filterfield = models.TextField(db_column='FILTERFIELD', blank=True, null=True)  # Field name made lowercase.
    varfield = models.CharField(db_column='VARFIELD', max_length=200, blank=True, null=True)  # Field name made lowercase.
    filtertype = models.SmallIntegerField(db_column='FILTERTYPE', blank=True, null=True)  # Field name made lowercase.
    source = models.SmallIntegerField(db_column='SOURCE', blank=True, null=True)  # Field name made lowercase.
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  # Field name made lowercase.
    isquery = models.SmallIntegerField(db_column='ISQUERY', blank=True, null=True)  # Field name made lowercase.
    isfilter = models.IntegerField(db_column='ISFILTER', blank=True, null=True)  # Field name made lowercase.
    printfield = models.TextField(db_column='PRINTFIELD', blank=True, null=True)  # Field name made lowercase.
    exportfield = models.TextField(db_column='EXPORTFIELD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_DATA_TEMPLATE'


class BpmDefinition(models.Model):
    defid = models.BigIntegerField(db_column='DEFID', primary_key=True)  # Field name made lowercase.
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=256)  # Field name made lowercase.
    defkey = models.CharField(db_column='DEFKEY', max_length=128)  # Field name made lowercase.
    tasknamerule = models.CharField(db_column='TASKNAMERULE', max_length=512, blank=True, null=True)  # Field name made lowercase.
    descp = models.CharField(db_column='DESCP', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    defxml = models.TextField(db_column='DEFXML', blank=True, null=True)  # Field name made lowercase.
    actdeployid = models.BigIntegerField(db_column='ACTDEPLOYID', blank=True, null=True)  # Field name made lowercase.
    actdefkey = models.CharField(db_column='ACTDEFKEY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UPDATETIME', blank=True, null=True)  # Field name made lowercase.
    createby = models.BigIntegerField(db_column='CREATEBY', blank=True, null=True)  # Field name made lowercase.
    updateby = models.BigIntegerField(db_column='UPDATEBY', blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='REASON', max_length=512, blank=True, null=True)  # Field name made lowercase.
    versionno = models.BigIntegerField(db_column='VERSIONNO', blank=True, null=True)  # Field name made lowercase.
    parentdefid = models.BigIntegerField(db_column='PARENTDEFID', blank=True, null=True)  # Field name made lowercase.
    ismain = models.SmallIntegerField(db_column='ISMAIN', blank=True, null=True)  # Field name made lowercase.
    tofirstnode = models.BigIntegerField(db_column='TOFIRSTNODE', blank=True, null=True)  # Field name made lowercase.
    showfirstassignee = models.SmallIntegerField(db_column='SHOWFIRSTASSIGNEE', blank=True, null=True)  # Field name made lowercase.
    canchoicepath = models.CharField(db_column='CANCHOICEPATH', max_length=500, blank=True, null=True)  # Field name made lowercase.
    isuseoutform = models.SmallIntegerField(db_column='ISUSEOUTFORM', blank=True, null=True)  # Field name made lowercase.
    formdetailurl = models.CharField(db_column='FORMDETAILURL', max_length=200, blank=True, null=True)  # Field name made lowercase.
    allowfinishedcc = models.SmallIntegerField(db_column='ALLOWFINISHEDCC', blank=True, null=True)  # Field name made lowercase.
    submitconfirm = models.SmallIntegerField(db_column='SUBMITCONFIRM', blank=True, null=True)  # Field name made lowercase.
    allowdivert = models.SmallIntegerField(db_column='ALLOWDIVERT', blank=True, null=True)  # Field name made lowercase.
    informstart = models.CharField(db_column='INFORMSTART', max_length=20, blank=True, null=True)  # Field name made lowercase.
    informtype = models.CharField(db_column='INFORMTYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    attachment = models.CharField(db_column='ATTACHMENT', max_length=80, blank=True, null=True)  # Field name made lowercase.
    sameexecutorjump = models.SmallIntegerField(db_column='SAMEEXECUTORJUMP', blank=True, null=True)  # Field name made lowercase.
    allowrefer = models.SmallIntegerField(db_column='ALLOWREFER', blank=True, null=True)  # Field name made lowercase.
    instanceamount = models.SmallIntegerField(db_column='INSTANCEAMOUNT', blank=True, null=True)  # Field name made lowercase.
    allowfinisheddivert = models.SmallIntegerField(db_column='ALLOWFINISHEDDIVERT', blank=True, null=True)  # Field name made lowercase.
    isprintform = models.SmallIntegerField(db_column='ISPRINTFORM', blank=True, null=True)  # Field name made lowercase.
    directstart = models.SmallIntegerField(db_column='DIRECTSTART', blank=True, null=True)  # Field name made lowercase.
    ccmessagetype = models.CharField(db_column='CCMESSAGETYPE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    allowdeldraf = models.SmallIntegerField(db_column='ALLOWDELDRAF', blank=True, null=True)  # Field name made lowercase.
    teststatustag = models.CharField(db_column='TESTSTATUSTAG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    allowmobile = models.IntegerField(db_column='ALLOWMOBILE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_DEFINITION'


class BpmDefAct(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    authorize_id = models.BigIntegerField(db_column='AUTHORIZE_ID')  # Field name made lowercase.
    def_key = models.CharField(db_column='DEF_KEY', max_length=100)  # Field name made lowercase.
    def_name = models.CharField(db_column='DEF_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    right_content = models.CharField(db_column='RIGHT_CONTENT', max_length=400, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_DEF_ACT'


class BpmDefAuthorize(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    authorize_desc = models.CharField(db_column='AUTHORIZE_DESC', max_length=512, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_DEF_AUTHORIZE'


class BpmDefAuthType(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    authorize_id = models.BigIntegerField(db_column='AUTHORIZE_ID')  # Field name made lowercase.
    authorize_type = models.CharField(db_column='AUTHORIZE_TYPE', max_length=64)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_DEF_AUTH_TYPE'


class BpmDefRights(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    flowtypeid = models.BigIntegerField(db_column='FLOWTYPEID', blank=True, null=True)  # Field name made lowercase.
    righttype = models.BigIntegerField(db_column='RIGHTTYPE', blank=True, null=True)  # Field name made lowercase.
    ownerid = models.BigIntegerField(db_column='OWNERID', blank=True, null=True)  # Field name made lowercase.
    ownername = models.CharField(db_column='OWNERNAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    searchtype = models.BigIntegerField(db_column='SEARCHTYPE', blank=True, null=True)  # Field name made lowercase.
    defkey = models.CharField(db_column='DEFKEY', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_DEF_RIGHTS'


class BpmDefUser(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    authorize_id = models.BigIntegerField(db_column='AUTHORIZE_ID')  # Field name made lowercase.
    owner_id = models.BigIntegerField(db_column='OWNER_ID')  # Field name made lowercase.
    owner_name = models.CharField(db_column='OWNER_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    right_type = models.CharField(db_column='RIGHT_TYPE', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_DEF_USER'


class BpmDefVars(models.Model):
    varid = models.BigIntegerField(db_column='VARID', primary_key=True)  # Field name made lowercase.
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  # Field name made lowercase.
    varname = models.CharField(db_column='VARNAME', max_length=128)  # Field name made lowercase.
    varkey = models.CharField(db_column='VARKEY', max_length=128, blank=True, null=True)  # Field name made lowercase.
    vardatatype = models.CharField(db_column='VARDATATYPE', max_length=64, blank=True, null=True)  # Field name made lowercase.
    defvalue = models.CharField(db_column='DEFVALUE', max_length=256, blank=True, null=True)  # Field name made lowercase.
    nodename = models.CharField(db_column='NODENAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=256, blank=True, null=True)  # Field name made lowercase.
    actdeployid = models.BigIntegerField(db_column='ACTDEPLOYID', blank=True, null=True)  # Field name made lowercase.
    varscope = models.CharField(db_column='VARSCOPE', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_DEF_VARS'


class BpmExeStack(models.Model):
    stackid = models.BigIntegerField(db_column='STACKID', primary_key=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=64, blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=128)  # Field name made lowercase.
    nodename = models.CharField(db_column='NODENAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='STARTTIME', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  # Field name made lowercase.
    assignees = models.CharField(db_column='ASSIGNEES', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    ismultitask = models.SmallIntegerField(db_column='ISMULTITASK', blank=True, null=True)  # Field name made lowercase.
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  # Field name made lowercase.
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  # Field name made lowercase.
    taskids = models.CharField(db_column='TASKIDS', max_length=512, blank=True, null=True)  # Field name made lowercase.
    nodepath = models.CharField(db_column='NODEPATH', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    depth = models.BigIntegerField(db_column='DEPTH', blank=True, null=True)  # Field name made lowercase.
    tasktoken = models.CharField(db_column='TASKTOKEN', max_length=128, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_EXE_STACK'


class BpmFormDef(models.Model):
    formdefid = models.BigIntegerField(db_column='FORMDEFID', primary_key=True)  # Field name made lowercase.
    categoryid = models.BigIntegerField(db_column='CATEGORYID', blank=True, null=True)  # Field name made lowercase.
    formkey = models.CharField(db_column='FORMKEY', max_length=128, blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=128, blank=True, null=True)  # Field name made lowercase.
    formdesc = models.CharField(db_column='FORMDESC', max_length=200, blank=True, null=True)  # Field name made lowercase.
    html = models.TextField(db_column='HTML', blank=True, null=True)  # Field name made lowercase.
    template = models.TextField(db_column='TEMPLATE', blank=True, null=True)  # Field name made lowercase.
    isdefault = models.SmallIntegerField(db_column='ISDEFAULT', blank=True, null=True)  # Field name made lowercase.
    versionno = models.BigIntegerField(db_column='VERSIONNO', blank=True, null=True)  # Field name made lowercase.
    tableid = models.BigIntegerField(db_column='TABLEID', blank=True, null=True)  # Field name made lowercase.
    ispublished = models.SmallIntegerField(db_column='ISPUBLISHED', blank=True, null=True)  # Field name made lowercase.
    publishedby = models.CharField(db_column='PUBLISHEDBY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    publishtime = models.DateTimeField(db_column='PUBLISHTIME', blank=True, null=True)  # Field name made lowercase.
    tabtitle = models.CharField(db_column='TABTITLE', max_length=500, blank=True, null=True)  # Field name made lowercase.
    designtype = models.SmallIntegerField(db_column='DESIGNTYPE', blank=True, null=True)  # Field name made lowercase.
    templatesid = models.CharField(db_column='TEMPLATESID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    createby = models.BigIntegerField(db_column='CREATEBY', blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_FORM_DEF'


class BpmFormDefHi(models.Model):
    hisid = models.BigIntegerField(db_column='HISID', primary_key=True)  # Field name made lowercase.
    formdefid = models.BigIntegerField(db_column='FORMDEFID')  # Field name made lowercase.
    categoryid = models.BigIntegerField(db_column='CATEGORYID', blank=True, null=True)  # Field name made lowercase.
    formkey = models.CharField(db_column='FORMKEY', max_length=200, blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=128, blank=True, null=True)  # Field name made lowercase.
    formdesc = models.CharField(db_column='FORMDESC', max_length=200, blank=True, null=True)  # Field name made lowercase.
    html = models.TextField(db_column='HTML', blank=True, null=True)  # Field name made lowercase.
    template = models.TextField(db_column='TEMPLATE', blank=True, null=True)  # Field name made lowercase.
    isdefault = models.SmallIntegerField(db_column='ISDEFAULT', blank=True, null=True)  # Field name made lowercase.
    versionno = models.BigIntegerField(db_column='VERSIONNO', blank=True, null=True)  # Field name made lowercase.
    tableid = models.BigIntegerField(db_column='TABLEID', blank=True, null=True)  # Field name made lowercase.
    ispublished = models.SmallIntegerField(db_column='ISPUBLISHED', blank=True, null=True)  # Field name made lowercase.
    publishedby = models.CharField(db_column='PUBLISHEDBY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    publishtime = models.DateTimeField(db_column='PUBLISHTIME', blank=True, null=True)  # Field name made lowercase.
    tabtitle = models.CharField(db_column='TABTITLE', max_length=500, blank=True, null=True)  # Field name made lowercase.
    designtype = models.SmallIntegerField(db_column='DESIGNTYPE', blank=True, null=True)  # Field name made lowercase.
    templatesid = models.CharField(db_column='TEMPLATESID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    createby = models.BigIntegerField(db_column='CREATEBY', blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_FORM_DEF_HI'


class BpmFormDialog(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    style = models.SmallIntegerField(db_column='STYLE', blank=True, null=True)  # Field name made lowercase.
    width = models.BigIntegerField(db_column='WIDTH', blank=True, null=True)  # Field name made lowercase.
    height = models.BigIntegerField(db_column='HEIGHT', blank=True, null=True)  # Field name made lowercase.
    issingle = models.SmallIntegerField(db_column='ISSINGLE', blank=True, null=True)  # Field name made lowercase.
    needpage = models.SmallIntegerField(db_column='NEEDPAGE', blank=True, null=True)  # Field name made lowercase.
    istable = models.SmallIntegerField(db_column='ISTABLE', blank=True, null=True)  # Field name made lowercase.
    objname = models.CharField(db_column='OBJNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    displayfield = models.CharField(db_column='DISPLAYFIELD', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    conditionfield = models.CharField(db_column='CONDITIONFIELD', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    resultfield = models.CharField(db_column='RESULTFIELD', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    dsname = models.CharField(db_column='DSNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dsalias = models.CharField(db_column='DSALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pagesize = models.SmallIntegerField(db_column='PAGESIZE', blank=True, null=True)  # Field name made lowercase.
    sortfield = models.CharField(db_column='SORTFIELD', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_FORM_DIALOG'


class BpmFormField(models.Model):
    fieldid = models.BigIntegerField(db_column='FIELDID', primary_key=True)  # Field name made lowercase.
    tableid = models.BigIntegerField(db_column='TABLEID', blank=True, null=True)  # Field name made lowercase.
    fieldname = models.CharField(db_column='FIELDNAME', max_length=128)  # Field name made lowercase.
    fieldtype = models.CharField(db_column='FIELDTYPE', max_length=128)  # Field name made lowercase.
    isrequired = models.SmallIntegerField(db_column='ISREQUIRED', blank=True, null=True)  # Field name made lowercase.
    islist = models.SmallIntegerField(db_column='ISLIST', blank=True, null=True)  # Field name made lowercase.
    isquery = models.SmallIntegerField(db_column='ISQUERY', blank=True, null=True)  # Field name made lowercase.
    fielddesc = models.CharField(db_column='FIELDDESC', max_length=128, blank=True, null=True)  # Field name made lowercase.
    charlen = models.BigIntegerField(db_column='CHARLEN', blank=True, null=True)  # Field name made lowercase.
    intlen = models.BigIntegerField(db_column='INTLEN', blank=True, null=True)  # Field name made lowercase.
    decimallen = models.BigIntegerField(db_column='DECIMALLEN', blank=True, null=True)  # Field name made lowercase.
    dicttype = models.CharField(db_column='DICTTYPE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.SmallIntegerField(db_column='ISDELETED', blank=True, null=True)  # Field name made lowercase.
    validrule = models.CharField(db_column='VALIDRULE', max_length=64, blank=True, null=True)  # Field name made lowercase.
    originalname = models.CharField(db_column='ORIGINALNAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  # Field name made lowercase.
    valuefrom = models.SmallIntegerField(db_column='VALUEFROM', blank=True, null=True)  # Field name made lowercase.
    script = models.CharField(db_column='SCRIPT', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    controltype = models.SmallIntegerField(db_column='CONTROLTYPE', blank=True, null=True)  # Field name made lowercase.
    ishidden = models.SmallIntegerField(db_column='ISHIDDEN', blank=True, null=True)  # Field name made lowercase.
    isflowvar = models.SmallIntegerField(db_column='ISFLOWVAR', blank=True, null=True)  # Field name made lowercase.
    serialnum = models.CharField(db_column='SERIALNUM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    options = models.CharField(db_column='OPTIONS', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    ctlproperty = models.CharField(db_column='CTLPROPERTY', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    isallowmobile = models.SmallIntegerField(db_column='ISALLOWMOBILE', blank=True, null=True)  # Field name made lowercase.
    iswebsign = models.SmallIntegerField(db_column='ISWEBSIGN', blank=True, null=True)  # Field name made lowercase.
    isreference = models.SmallIntegerField(db_column='ISREFERENCE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_FORM_FIELD'


class BpmFormQuery(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    obj_name = models.CharField(db_column='OBJ_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    needpage = models.BigIntegerField(db_column='NEEDPAGE', blank=True, null=True)  # Field name made lowercase.
    conditionfield = models.CharField(db_column='CONDITIONFIELD', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    resultfield = models.CharField(db_column='RESULTFIELD', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    dsname = models.CharField(db_column='DSNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dsalias = models.CharField(db_column='DSALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pagesize = models.BigIntegerField(db_column='PAGESIZE', blank=True, null=True)  # Field name made lowercase.
    istable = models.BigIntegerField(db_column='ISTABLE', blank=True, null=True)  # Field name made lowercase.
    sortfield = models.CharField(db_column='SORTFIELD', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_FORM_QUERY'


class BpmFormRights(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    formdefid = models.BigIntegerField(db_column='FORMDEFID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    permission = models.CharField(db_column='PERMISSION', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    type = models.SmallIntegerField(db_column='TYPE', blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=60, blank=True, null=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=60, blank=True, null=True)  # Field name made lowercase.
    parentactdefid = models.CharField(db_column='PARENTACTDEFID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    platform = models.IntegerField(db_column='PLATFORM', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_FORM_RIGHTS'


class BpmFormRule(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    regulation = models.CharField(db_column='REGULATION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tipinfo = models.CharField(db_column='TIPINFO', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_FORM_RULE'


class BpmFormRun(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    formdefid = models.BigIntegerField(db_column='FORMDEFID', blank=True, null=True)  # Field name made lowercase.
    formdefkey = models.BigIntegerField(db_column='FORMDEFKEY', blank=True, null=True)  # Field name made lowercase.
    actinstanceid = models.CharField(db_column='ACTINSTANCEID', max_length=64, blank=True, null=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=64, blank=True, null=True)  # Field name made lowercase.
    actnodeid = models.CharField(db_column='ACTNODEID', max_length=64, blank=True, null=True)  # Field name made lowercase.
    runid = models.BigIntegerField(db_column='RUNID', blank=True, null=True)  # Field name made lowercase.
    settype = models.SmallIntegerField(db_column='SETTYPE', blank=True, null=True)  # Field name made lowercase.
    formtype = models.SmallIntegerField(db_column='FORMTYPE', blank=True, null=True)  # Field name made lowercase.
    formurl = models.CharField(db_column='FORMURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mobileformid = models.BigIntegerField(db_column='MOBILEFORMID', blank=True, null=True)  # Field name made lowercase.
    mobileformkey = models.BigIntegerField(db_column='MOBILEFORMKEY', blank=True, null=True)  # Field name made lowercase.
    mobileformurl = models.CharField(db_column='MOBILEFORMURL', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_FORM_RUN'


class BpmFormTable(models.Model):
    tableid = models.BigIntegerField(db_column='TABLEID', primary_key=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TABLENAME', max_length=128)  # Field name made lowercase.
    tabledesc = models.CharField(db_column='TABLEDESC', max_length=128, blank=True, null=True)  # Field name made lowercase.
    ismain = models.SmallIntegerField(db_column='ISMAIN', blank=True, null=True)  # Field name made lowercase.
    maintableid = models.BigIntegerField(db_column='MAINTABLEID', blank=True, null=True)  # Field name made lowercase.
    ispublished = models.SmallIntegerField(db_column='ISPUBLISHED', blank=True, null=True)  # Field name made lowercase.
    publishedby = models.CharField(db_column='PUBLISHEDBY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    publishtime = models.DateTimeField(db_column='PUBLISHTIME', blank=True, null=True)  # Field name made lowercase.
    isexternal = models.SmallIntegerField(db_column='ISEXTERNAL', blank=True, null=True)  # Field name made lowercase.
    dsalias = models.CharField(db_column='DSALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dsname = models.CharField(db_column='DSNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    relation = models.CharField(db_column='RELATION', max_length=500, blank=True, null=True)  # Field name made lowercase.
    keytype = models.SmallIntegerField(db_column='KEYTYPE', blank=True, null=True)  # Field name made lowercase.
    keyvalue = models.CharField(db_column='KEYVALUE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pkfield = models.CharField(db_column='PKFIELD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    listtemplate = models.TextField(db_column='LISTTEMPLATE', blank=True, null=True)  # Field name made lowercase.
    detailtemplate = models.TextField(db_column='DETAILTEMPLATE', blank=True, null=True)  # Field name made lowercase.
    genbyform = models.SmallIntegerField(db_column='GENBYFORM', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.BigIntegerField(db_column='CREATEBY', blank=True, null=True)  # Field name made lowercase.
    keydatatype = models.SmallIntegerField(db_column='KEYDATATYPE', blank=True, null=True)  # Field name made lowercase.
    team = models.TextField(db_column='TEAM', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_FORM_TABLE'


class BpmFormTemplate(models.Model):
    templateid = models.BigIntegerField(db_column='TEMPLATEID', primary_key=True)  # Field name made lowercase.
    templatename = models.CharField(db_column='TEMPLATENAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    templatetype = models.CharField(db_column='TEMPLATETYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    macrotemplatealias = models.CharField(db_column='MACROTEMPLATEALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    html = models.TextField(db_column='HTML', blank=True, null=True)  # Field name made lowercase.
    templatedesc = models.CharField(db_column='TEMPLATEDESC', max_length=400, blank=True, null=True)  # Field name made lowercase.
    canedit = models.SmallIntegerField(db_column='CANEDIT', blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_FORM_TEMPLATE'


class BpmGangedSet(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nodename = models.CharField(db_column='NODENAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    choisefield = models.TextField(db_column='CHOISEFIELD', blank=True, null=True)  # Field name made lowercase.
    changefield = models.TextField(db_column='CHANGEFIELD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_GANGED_SET'


class BpmMobileForm(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    formid = models.BigIntegerField(db_column='FORMID', blank=True, null=True)  # Field name made lowercase.
    formkey = models.BigIntegerField(db_column='FORMKEY', blank=True, null=True)  # Field name made lowercase.
    html = models.TextField(db_column='HTML', blank=True, null=True)  # Field name made lowercase.
    template = models.TextField(db_column='TEMPLATE', blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='GUID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    isdefault = models.IntegerField(db_column='ISDEFAULT', blank=True, null=True)  # Field name made lowercase.
    formjson = models.TextField(db_column='FORMJSON', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_MOBILE_FORM'


class BpmMonGroup(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    grade = models.SmallIntegerField(db_column='GRADE', blank=True, null=True)  # Field name made lowercase.
    enabled = models.SmallIntegerField(db_column='ENABLED', blank=True, null=True)  # Field name made lowercase.
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_MON_GROUP'


class BpmMonGroupitem(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    groupid = models.BigIntegerField(db_column='GROUPID', blank=True, null=True)  # Field name made lowercase.
    flowkey = models.CharField(db_column='FLOWKEY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_MON_GROUPITEM'


class BpmMonOrgrole(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    groupid = models.BigIntegerField(db_column='GROUPID', blank=True, null=True)  # Field name made lowercase.
    roleid = models.BigIntegerField(db_column='ROLEID', blank=True, null=True)  # Field name made lowercase.
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_MON_ORGROLE'


class BpmNodeBtn(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=64, blank=True, null=True)  # Field name made lowercase.
    isstartform = models.SmallIntegerField(db_column='ISSTARTFORM', blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    btnname = models.CharField(db_column='BTNNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    iconclsname = models.CharField(db_column='ICONCLSNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    operatortype = models.SmallIntegerField(db_column='OPERATORTYPE', blank=True, null=True)  # Field name made lowercase.
    prevscript = models.CharField(db_column='PREVSCRIPT', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    afterscript = models.CharField(db_column='AFTERSCRIPT', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    nodetype = models.SmallIntegerField(db_column='NODETYPE', blank=True, null=True)  # Field name made lowercase.
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  # Field name made lowercase.
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_NODE_BTN'


class BpmNodeMessage(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=64, blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    messagetype = models.SmallIntegerField(db_column='MESSAGETYPE', blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=200, blank=True, null=True)  # Field name made lowercase.
    template = models.TextField(db_column='TEMPLATE', blank=True, null=True)  # Field name made lowercase.
    issend = models.SmallIntegerField(db_column='ISSEND', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_NODE_MESSAGE'


class BpmNodePrivilege(models.Model):
    privilegeid = models.BigIntegerField(db_column='PRIVILEGEID', primary_key=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    privilegemode = models.SmallIntegerField(db_column='PRIVILEGEMODE', blank=True, null=True)  # Field name made lowercase.
    usertype = models.SmallIntegerField(db_column='USERTYPE', blank=True, null=True)  # Field name made lowercase.
    cmpnames = models.TextField(db_column='CMPNAMES', blank=True, null=True)  # Field name made lowercase.
    cmpids = models.TextField(db_column='CMPIDS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_NODE_PRIVILEGE'


class BpmNodeRule(models.Model):
    ruleid = models.BigIntegerField(db_column='RULEID', primary_key=True)  # Field name made lowercase.
    rulename = models.CharField(db_column='RULENAME', max_length=128)  # Field name made lowercase.
    conditioncode = models.TextField(db_column='CONDITIONCODE', blank=True, null=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    priority = models.BigIntegerField(db_column='PRIORITY', blank=True, null=True)  # Field name made lowercase.
    targetnode = models.CharField(db_column='TARGETNODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    targetnodename = models.CharField(db_column='TARGETNODENAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_NODE_RULE'


class BpmNodeScript(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=64, blank=True, null=True)  # Field name made lowercase.
    script = models.TextField(db_column='SCRIPT', blank=True, null=True)  # Field name made lowercase.
    scripttype = models.BigIntegerField(db_column='SCRIPTTYPE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_NODE_SCRIPT'


class BpmNodeSet(models.Model):
    setid = models.BigIntegerField(db_column='SETID', primary_key=True)  # Field name made lowercase.
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  # Field name made lowercase.
    nodename = models.CharField(db_column='NODENAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    nodeorder = models.SmallIntegerField(db_column='NODEORDER', blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    formtype = models.SmallIntegerField(db_column='FORMTYPE', blank=True, null=True)  # Field name made lowercase.
    formurl = models.CharField(db_column='FORMURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    formkey = models.BigIntegerField(db_column='FORMKEY', blank=True, null=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  # Field name made lowercase.
    formdefname = models.CharField(db_column='FORMDEFNAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nodetype = models.SmallIntegerField(db_column='NODETYPE', blank=True, null=True)  # Field name made lowercase.
    jointaskkey = models.CharField(db_column='JOINTASKKEY', max_length=128, blank=True, null=True)  # Field name made lowercase.
    jointaskname = models.CharField(db_column='JOINTASKNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    beforehandler = models.CharField(db_column='BEFOREHANDLER', max_length=100, blank=True, null=True)  # Field name made lowercase.
    afterhandler = models.CharField(db_column='AFTERHANDLER', max_length=100, blank=True, null=True)  # Field name made lowercase.
    jumptype = models.CharField(db_column='JUMPTYPE', max_length=32, blank=True, null=True)  # Field name made lowercase.
    settype = models.SmallIntegerField(db_column='SETTYPE', blank=True, null=True)  # Field name made lowercase.
    isjumpfordef = models.SmallIntegerField(db_column='ISJUMPFORDEF', blank=True, null=True)  # Field name made lowercase.
    ishideoption = models.SmallIntegerField(db_column='ISHIDEOPTION', blank=True, null=True)  # Field name made lowercase.
    ishidepath = models.SmallIntegerField(db_column='ISHIDEPATH', blank=True, null=True)  # Field name made lowercase.
    detailurl = models.CharField(db_column='DETAILURL', max_length=256, blank=True, null=True)  # Field name made lowercase.
    isallowmobile = models.SmallIntegerField(db_column='ISALLOWMOBILE', blank=True, null=True)  # Field name made lowercase.
    informtype = models.CharField(db_column='INFORMTYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    parentactdefid = models.CharField(db_column='PARENTACTDEFID', max_length=127, blank=True, null=True)  # Field name made lowercase.
    mobileformkey = models.BigIntegerField(db_column='MOBILEFORMKEY', blank=True, null=True)  # Field name made lowercase.
    mobileformurl = models.CharField(db_column='MOBILEFORMURL', max_length=256, blank=True, null=True)  # Field name made lowercase.
    mobiledetailurl = models.CharField(db_column='MOBILEDETAILURL', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_NODE_SET'


class BpmNodeSign(models.Model):
    signid = models.BigIntegerField(db_column='SIGNID', primary_key=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    voteamount = models.BigIntegerField(db_column='VOTEAMOUNT', blank=True, null=True)  # Field name made lowercase.
    decidetype = models.SmallIntegerField(db_column='DECIDETYPE')  # Field name made lowercase.
    votetype = models.SmallIntegerField(db_column='VOTETYPE', blank=True, null=True)  # Field name made lowercase.
    flowmode = models.SmallIntegerField(db_column='FLOWMODE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_NODE_SIGN'


class BpmNodeUser(models.Model):
    nodeuserid = models.BigIntegerField(db_column='NODEUSERID', primary_key=True)  # Field name made lowercase.
    cmpids = models.TextField(db_column='CMPIDS', blank=True, null=True)  # Field name made lowercase.
    cmpnames = models.TextField(db_column='CMPNAMES', blank=True, null=True)  # Field name made lowercase.
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  # Field name made lowercase.
    assigntype = models.CharField(db_column='ASSIGNTYPE', max_length=20)  # Field name made lowercase.
    comptype = models.SmallIntegerField(db_column='COMPTYPE', blank=True, null=True)  # Field name made lowercase.
    conditionid = models.BigIntegerField(db_column='CONDITIONID', blank=True, null=True)  # Field name made lowercase.
    extractuser = models.SmallIntegerField(db_column='EXTRACTUSER', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_NODE_USER'


class BpmNodeWebservice(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    document = models.TextField(db_column='DOCUMENT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_NODE_WEBSERVICE'


class BpmNodeWsParams(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    webserviceid = models.BigIntegerField(db_column='WEBSERVICEID', blank=True, null=True)  # Field name made lowercase.
    paratype = models.BigIntegerField(db_column='PARATYPE', blank=True, null=True)  # Field name made lowercase.
    varid = models.BigIntegerField(db_column='VARID', blank=True, null=True)  # Field name made lowercase.
    wsname = models.CharField(db_column='WSNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=128, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_NODE_WS_PARAMS'


class BpmPrintTemplate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    form_key = models.BigIntegerField(db_column='FORM_KEY', blank=True, null=True)  # Field name made lowercase.
    temapalte_name = models.CharField(db_column='TEMAPALTE_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    is_default = models.SmallIntegerField(db_column='IS_DEFAULT', blank=True, null=True)  # Field name made lowercase.
    tableid = models.BigIntegerField(db_column='TABLEID', blank=True, null=True)  # Field name made lowercase.
    html = models.TextField(db_column='HTML', blank=True, null=True)  # Field name made lowercase.
    template = models.TextField(db_column='TEMPLATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_PRINT_TEMPLATE'


class BpmProCpto(models.Model):
    copy_id = models.BigIntegerField(db_column='COPY_ID', primary_key=True)  # Field name made lowercase.
    acact_inst_id = models.BigIntegerField(db_column='ACACT_INST_ID')  # Field name made lowercase.
    run_id = models.BigIntegerField(db_column='RUN_ID')  # Field name made lowercase.
    node_key = models.CharField(db_column='NODE_KEY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    node_name = models.CharField(db_column='NODE_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cc_uid = models.BigIntegerField(db_column='CC_UID', blank=True, null=True)  # Field name made lowercase.
    cc_uname = models.CharField(db_column='CC_UNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cc_time = models.DateTimeField(db_column='CC_TIME')  # Field name made lowercase.
    is_readed = models.SmallIntegerField(db_column='IS_READED', blank=True, null=True)  # Field name made lowercase.
    fill_opinion = models.CharField(db_column='FILL_OPINION', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=300, blank=True, null=True)  # Field name made lowercase.
    read_time = models.DateTimeField(db_column='READ_TIME')  # Field name made lowercase.
    cp_type = models.SmallIntegerField(db_column='CP_TYPE', blank=True, null=True)  # Field name made lowercase.
    create_id = models.BigIntegerField(db_column='CREATE_ID', blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    def_typeid = models.BigIntegerField(db_column='DEF_TYPEID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_PRO_CPTO'


class BpmProRun(models.Model):
    runid = models.BigIntegerField(db_column='RUNID', primary_key=True)  # Field name made lowercase.
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  # Field name made lowercase.
    processname = models.CharField(db_column='PROCESSNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=600, blank=True, null=True)  # Field name made lowercase.
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=128, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  # Field name made lowercase.
    busdescp = models.CharField(db_column='BUSDESCP', max_length=3000, blank=True, null=True)  # Field name made lowercase.
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=256, blank=True, null=True)  # Field name made lowercase.
    businesskey = models.CharField(db_column='BUSINESSKEY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    businessurl = models.CharField(db_column='BUSINESSURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  # Field name made lowercase.
    duration = models.BigIntegerField(db_column='DURATION', blank=True, null=True)  # Field name made lowercase.
    pkname = models.CharField(db_column='PKNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TABLENAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  # Field name made lowercase.
    startorgid = models.BigIntegerField(db_column='STARTORGID', blank=True, null=True)  # Field name made lowercase.
    startorgname = models.CharField(db_column='STARTORGNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    formdefid = models.BigIntegerField(db_column='FORMDEFID', blank=True, null=True)  # Field name made lowercase.
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  # Field name made lowercase.
    dsalias = models.CharField(db_column='DSALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flowkey = models.CharField(db_column='FLOWKEY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    formtype = models.SmallIntegerField(db_column='FORMTYPE', blank=True, null=True)  # Field name made lowercase.
    formkeyurl = models.CharField(db_column='FORMKEYURL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastsubmitduration = models.BigIntegerField(db_column='LASTSUBMITDURATION', blank=True, null=True)  # Field name made lowercase.
    isformal = models.SmallIntegerField(db_column='ISFORMAL', blank=True, null=True)  # Field name made lowercase.
    startnode = models.CharField(db_column='STARTNODE', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_PRO_RUN'


class BpmProRunHis(models.Model):
    runid = models.BigIntegerField(db_column='RUNID', primary_key=True)  # Field name made lowercase.
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  # Field name made lowercase.
    processname = models.CharField(db_column='PROCESSNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=600, blank=True, null=True)  # Field name made lowercase.
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=128, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  # Field name made lowercase.
    busdescp = models.CharField(db_column='BUSDESCP', max_length=3000, blank=True, null=True)  # Field name made lowercase.
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=256, blank=True, null=True)  # Field name made lowercase.
    businesskey = models.CharField(db_column='BUSINESSKEY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    businessurl = models.CharField(db_column='BUSINESSURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  # Field name made lowercase.
    duration = models.BigIntegerField(db_column='DURATION', blank=True, null=True)  # Field name made lowercase.
    pkname = models.CharField(db_column='PKNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TABLENAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  # Field name made lowercase.
    startorgid = models.BigIntegerField(db_column='STARTORGID', blank=True, null=True)  # Field name made lowercase.
    startorgname = models.CharField(db_column='STARTORGNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    formdefid = models.BigIntegerField(db_column='FORMDEFID', blank=True, null=True)  # Field name made lowercase.
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  # Field name made lowercase.
    dsalias = models.CharField(db_column='DSALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flowkey = models.CharField(db_column='FLOWKEY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    formtype = models.SmallIntegerField(db_column='FORMTYPE', blank=True, null=True)  # Field name made lowercase.
    formkeyurl = models.CharField(db_column='FORMKEYURL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastsubmitduration = models.BigIntegerField(db_column='LASTSUBMITDURATION', blank=True, null=True)  # Field name made lowercase.
    isformal = models.SmallIntegerField(db_column='ISFORMAL', blank=True, null=True)  # Field name made lowercase.
    startnode = models.CharField(db_column='STARTNODE', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_PRO_RUN_HIS'


class BpmProStatus(models.Model):
    id = models.BigIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=64, blank=True, null=True)  # Field name made lowercase.
    nodename = models.CharField(db_column='NODENAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    lastupdatetime = models.DateTimeField(db_column='LASTUPDATETIME', blank=True, null=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=64, blank=True, null=True)  # Field name made lowercase.
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_PRO_STATUS'


class BpmProTransto(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  # Field name made lowercase.
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  # Field name made lowercase.
    transtype = models.SmallIntegerField(db_column='TRANSTYPE', blank=True, null=True)  # Field name made lowercase.
    action = models.SmallIntegerField(db_column='ACTION', blank=True, null=True)  # Field name made lowercase.
    createuserid = models.BigIntegerField(db_column='CREATEUSERID', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.
    transresult = models.SmallIntegerField(db_column='TRANSRESULT', blank=True, null=True)  # Field name made lowercase.
    assignee = models.CharField(db_column='ASSIGNEE', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_PRO_TRANSTO'


class BpmReferDefinition(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    defid = models.CharField(db_column='DEFID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    refer_defkey = models.CharField(db_column='REFER_DEFKEY', max_length=128, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.
    createid = models.BigIntegerField(db_column='CREATEID', blank=True, null=True)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UPDATETIME')  # Field name made lowercase.
    state = models.SmallIntegerField(db_column='STATE', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=400, blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=200, blank=True, null=True)  # Field name made lowercase.
    updateid = models.BigIntegerField(db_column='UPDATEID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_REFER_DEFINITION'


class BpmRunLog(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  # Field name made lowercase.
    operatortype = models.SmallIntegerField(db_column='OPERATORTYPE', blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=300, blank=True, null=True)  # Field name made lowercase.
    runid = models.BigIntegerField(db_column='RUNID', blank=True, null=True)  # Field name made lowercase.
    processsubject = models.CharField(db_column='PROCESSSUBJECT', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_RUN_LOG'


class BpmSubtableRights(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tableid = models.BigIntegerField(db_column='TABLEID', blank=True, null=True)  # Field name made lowercase.
    permissiontype = models.SmallIntegerField(db_column='PERMISSIONTYPE', blank=True, null=True)  # Field name made lowercase.
    permissionseting = models.CharField(db_column='PERMISSIONSETING', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    parentactdefid = models.CharField(db_column='PARENTACTDEFID', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_SUBTABLE_RIGHTS'


class BpmTaskDue(models.Model):
    taskdueid = models.BigIntegerField(db_column='TASKDUEID', primary_key=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    reminderstart = models.BigIntegerField(db_column='REMINDERSTART')  # Field name made lowercase.
    reminderend = models.BigIntegerField(db_column='REMINDEREND', blank=True, null=True)  # Field name made lowercase.
    times = models.BigIntegerField(db_column='TIMES', blank=True, null=True)  # Field name made lowercase.
    mailcontent = models.TextField(db_column='MAILCONTENT', blank=True, null=True)  # Field name made lowercase.
    msgcontent = models.TextField(db_column='MSGCONTENT', blank=True, null=True)  # Field name made lowercase.
    smscontent = models.TextField(db_column='SMSCONTENT', blank=True, null=True)  # Field name made lowercase.
    action = models.BigIntegerField(db_column='ACTION', blank=True, null=True)  # Field name made lowercase.
    script = models.CharField(db_column='SCRIPT', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    completetime = models.BigIntegerField(db_column='COMPLETETIME', blank=True, null=True)  # Field name made lowercase.
    condexp = models.TextField(db_column='CONDEXP', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    relativenodeid = models.CharField(db_column='RELATIVENODEID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    relativenodetype = models.BigIntegerField(db_column='RELATIVENODETYPE', blank=True, null=True)  # Field name made lowercase.
    relativetimetype = models.BigIntegerField(db_column='RELATIVETIMETYPE', blank=True, null=True)  # Field name made lowercase.
    assignerid = models.BigIntegerField(db_column='ASSIGNERID', blank=True, null=True)  # Field name made lowercase.
    assignername = models.CharField(db_column='ASSIGNERNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_TASK_DUE'


class BpmTaskExe(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  # Field name made lowercase.
    assignee_id = models.BigIntegerField(db_column='ASSIGNEE_ID', blank=True, null=True)  # Field name made lowercase.
    assignee_name = models.CharField(db_column='ASSIGNEE_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    owner_id = models.BigIntegerField(db_column='OWNER_ID', blank=True, null=True)  # Field name made lowercase.
    owner_name = models.CharField(db_column='OWNER_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=400, blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    cratetime = models.DateTimeField(db_column='CRATETIME', blank=True, null=True)  # Field name made lowercase.
    act_inst_id = models.BigIntegerField(db_column='ACT_INST_ID', blank=True, null=True)  # Field name made lowercase.
    task_name = models.CharField(db_column='TASK_NAME', max_length=400, blank=True, null=True)  # Field name made lowercase.
    task_def_key = models.CharField(db_column='TASK_DEF_KEY', max_length=64, blank=True, null=True)  # Field name made lowercase.
    exe_time = models.DateTimeField(db_column='EXE_TIME', blank=True, null=True)  # Field name made lowercase.
    exe_user_id = models.BigIntegerField(db_column='EXE_USER_ID', blank=True, null=True)  # Field name made lowercase.
    exe_user_name = models.CharField(db_column='EXE_USER_NAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    assign_type = models.SmallIntegerField(db_column='ASSIGN_TYPE', blank=True, null=True)  # Field name made lowercase.
    runid = models.BigIntegerField(db_column='RUNID', blank=True, null=True)  # Field name made lowercase.
    type_id = models.BigIntegerField(db_column='TYPE_ID', blank=True, null=True)  # Field name made lowercase.
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_TASK_EXE'


class BpmTaskFork(models.Model):
    taskforkid = models.BigIntegerField(db_column='TASKFORKID', primary_key=True)  # Field name made lowercase.
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  # Field name made lowercase.
    forktaskname = models.CharField(db_column='FORKTASKNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    forktaskkey = models.CharField(db_column='FORKTASKKEY', max_length=256, blank=True, null=True)  # Field name made lowercase.
    forksn = models.BigIntegerField(db_column='FORKSN', blank=True, null=True)  # Field name made lowercase.
    forkcount = models.BigIntegerField(db_column='FORKCOUNT', blank=True, null=True)  # Field name made lowercase.
    fininshcount = models.BigIntegerField(db_column='FININSHCOUNT', blank=True, null=True)  # Field name made lowercase.
    forktime = models.DateTimeField(db_column='FORKTIME', blank=True, null=True)  # Field name made lowercase.
    jointaskname = models.CharField(db_column='JOINTASKNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    jointaskkey = models.CharField(db_column='JOINTASKKEY', max_length=256, blank=True, null=True)  # Field name made lowercase.
    forktokens = models.CharField(db_column='FORKTOKENS', max_length=512, blank=True, null=True)  # Field name made lowercase.
    forktokenpre = models.CharField(db_column='FORKTOKENPRE', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_TASK_FORK'


class BpmTaskOpinion(models.Model):
    opinionid = models.BigIntegerField(db_column='OPINIONID', primary_key=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  # Field name made lowercase.
    taskname = models.CharField(db_column='TASKNAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    taskkey = models.CharField(db_column='TASKKEY', max_length=64, blank=True, null=True)  # Field name made lowercase.
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  # Field name made lowercase.
    tasktoken = models.CharField(db_column='TASKTOKEN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='STARTTIME')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  # Field name made lowercase.
    durtime = models.BigIntegerField(db_column='DURTIME', blank=True, null=True)  # Field name made lowercase.
    exeuserid = models.BigIntegerField(db_column='EXEUSERID', blank=True, null=True)  # Field name made lowercase.
    exefullname = models.CharField(db_column='EXEFULLNAME', max_length=127, blank=True, null=True)  # Field name made lowercase.
    opinion = models.TextField(db_column='OPINION', blank=True, null=True)  # Field name made lowercase.
    checkstatus = models.SmallIntegerField(db_column='CHECKSTATUS', blank=True, null=True)  # Field name made lowercase.
    formdefid = models.BigIntegerField(db_column='FORMDEFID', blank=True, null=True)  # Field name made lowercase.
    fieldname = models.CharField(db_column='FIELDNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    superexecution = models.BigIntegerField(db_column='SUPEREXECUTION', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_TASK_OPINION'


class BpmTaskRead(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  # Field name made lowercase.
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_TASK_READ'


class BpmTaskReminderstate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  # Field name made lowercase.
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  # Field name made lowercase.
    remindertime = models.DateTimeField(db_column='REMINDERTIME', blank=True, null=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    actinstanceid = models.BigIntegerField(db_column='ACTINSTANCEID', blank=True, null=True)  # Field name made lowercase.
    remindtype = models.SmallIntegerField(db_column='REMINDTYPE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_TASK_REMINDERSTATE'


class BpmTksignData(models.Model):
    dataid = models.BigIntegerField(db_column='DATAID', primary_key=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  # Field name made lowercase.
    actinstid = models.BigIntegerField(db_column='ACTINSTID')  # Field name made lowercase.
    nodename = models.CharField(db_column='NODENAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=127)  # Field name made lowercase.
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  # Field name made lowercase.
    voteuserid = models.CharField(db_column='VOTEUSERID', max_length=1000)  # Field name made lowercase.
    voteusername = models.CharField(db_column='VOTEUSERNAME', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    votetime = models.DateTimeField(db_column='VOTETIME', blank=True, null=True)  # Field name made lowercase.
    isagree = models.SmallIntegerField(db_column='ISAGREE', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='CONTENT', max_length=200, blank=True, null=True)  # Field name made lowercase.
    signnums = models.BigIntegerField(db_column='SIGNNUMS', blank=True, null=True)  # Field name made lowercase.
    iscompleted = models.SmallIntegerField(db_column='ISCOMPLETED', blank=True, null=True)  # Field name made lowercase.
    batch = models.SmallIntegerField(db_column='BATCH', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_TKSIGN_DATA'


class BpmUserCondition(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    setid = models.BigIntegerField(db_column='SETID', blank=True, null=True)  # Field name made lowercase.
    conditionname = models.CharField(db_column='CONDITIONNAME', max_length=127, blank=True, null=True)  # Field name made lowercase.
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  # Field name made lowercase.
    nodeid = models.CharField(db_column='NODEID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    conditioncode = models.TextField(db_column='CONDITIONCODE', blank=True, null=True)  # Field name made lowercase.
    sn = models.DecimalField(db_column='SN', max_digits=38, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    conditionshow = models.TextField(db_column='CONDITIONSHOW', blank=True, null=True)  # Field name made lowercase.
    conditiontype = models.SmallIntegerField(db_column='CONDITIONTYPE', blank=True, null=True)  # Field name made lowercase.
    groupno = models.SmallIntegerField(db_column='GROUPNO', blank=True, null=True)  # Field name made lowercase.
    formidentity = models.CharField(db_column='FORMIDENTITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    parentactdefid = models.CharField(db_column='PARENTACTDEFID', max_length=128, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BPM_USER_CONDITION'


class BusQueryFilter(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ruleid = models.BigIntegerField(db_column='RULEID', blank=True, null=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TABLENAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    filtername = models.CharField(db_column='FILTERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    filterdesc = models.TextField(db_column='FILTERDESC', blank=True, null=True)  # Field name made lowercase.
    filterkey = models.CharField(db_column='FILTERKEY', max_length=256, blank=True, null=True)  # Field name made lowercase.
    queryparameter = models.TextField(db_column='QUERYPARAMETER', blank=True, null=True)  # Field name made lowercase.
    sortparameter = models.TextField(db_column='SORTPARAMETER', blank=True, null=True)  # Field name made lowercase.
    isshare = models.SmallIntegerField(db_column='ISSHARE', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.
    createby = models.BigIntegerField(db_column='CREATEBY', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BUS_QUERY_FILTER'


class BusQueryRule(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TABLENAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    needpage = models.SmallIntegerField(db_column='NEEDPAGE', blank=True, null=True)  # Field name made lowercase.
    pagesize = models.BigIntegerField(db_column='PAGESIZE', blank=True, null=True)  # Field name made lowercase.
    isquery = models.SmallIntegerField(db_column='ISQUERY', blank=True, null=True)  # Field name made lowercase.
    isfilter = models.SmallIntegerField(db_column='ISFILTER', blank=True, null=True)  # Field name made lowercase.
    displayfield = models.TextField(db_column='DISPLAYFIELD', blank=True, null=True)  # Field name made lowercase.
    filterfield = models.TextField(db_column='FILTERFIELD', blank=True, null=True)  # Field name made lowercase.
    sortfield = models.TextField(db_column='SORTFIELD', blank=True, null=True)  # Field name made lowercase.
    exportfield = models.TextField(db_column='EXPORTFIELD', blank=True, null=True)  # Field name made lowercase.
    printfield = models.TextField(db_column='PRINTFIELD', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.
    createby = models.BigIntegerField(db_column='CREATEBY', blank=True, null=True)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UPDATETIME')  # Field name made lowercase.
    updateby = models.BigIntegerField(db_column='UPDATEBY', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BUS_QUERY_RULE'


class BusQuerySetting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TABLENAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    displayfield = models.TextField(db_column='DISPLAYFIELD', blank=True, null=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BUS_QUERY_SETTING'


class BusQueryShare(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    filterid = models.BigIntegerField(db_column='FILTERID', blank=True, null=True)  # Field name made lowercase.
    shareright = models.TextField(db_column='SHARERIGHT', blank=True, null=True)  # Field name made lowercase.
    sharerid = models.BigIntegerField(db_column='SHARERID', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BUS_QUERY_SHARE'


class MailCodeMap(models.Model):
    mail = models.CharField(max_length=2000)
    code = models.IntegerField()
    sex = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MAIL_CODE_MAP'


class MobileUserInfo(models.Model):
    userid = models.BigIntegerField(db_column='USERID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=127, blank=True, null=True)  # Field name made lowercase.
    idcard = models.CharField(db_column='IDCARD', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MOBILE_USER_INFO'


class OutMail(models.Model):
    mailid = models.BigIntegerField(db_column='MAILID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=512, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='CONTENT', blank=True, null=True)  # Field name made lowercase.
    senderaddresses = models.CharField(db_column='SENDERADDRESSES', max_length=128, blank=True, null=True)  # Field name made lowercase.
    sendername = models.CharField(db_column='SENDERNAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    receiveraddresses = models.TextField(db_column='RECEIVERADDRESSES', blank=True, null=True)  # Field name made lowercase.
    receivernames = models.TextField(db_column='RECEIVERNAMES', blank=True, null=True)  # Field name made lowercase.
    ccaddresses = models.TextField(db_column='CCADDRESSES', blank=True, null=True)  # Field name made lowercase.
    bccanames = models.TextField(db_column='BCCANAMES', blank=True, null=True)  # Field name made lowercase.
    bccaddresses = models.TextField(db_column='BCCADDRESSES', blank=True, null=True)  # Field name made lowercase.
    ccnames = models.TextField(db_column='CCNAMES', blank=True, null=True)  # Field name made lowercase.
    emailid = models.CharField(db_column='EMAILID', max_length=128, blank=True, null=True)  # Field name made lowercase.
    types = models.BigIntegerField(db_column='TYPES', blank=True, null=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    isreply = models.BigIntegerField(db_column='ISREPLY', blank=True, null=True)  # Field name made lowercase.
    maildate = models.DateTimeField(db_column='MAILDATE', blank=True, null=True)  # Field name made lowercase.
    fileids = models.CharField(db_column='FILEIDS', max_length=512, blank=True, null=True)  # Field name made lowercase.
    isread = models.BigIntegerField(db_column='ISREAD', blank=True, null=True)  # Field name made lowercase.
    setid = models.BigIntegerField(db_column='SETID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OUT_MAIL'


class OutMailAttachment(models.Model):
    fileid = models.BigIntegerField(db_column='FILEID', primary_key=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FILENAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    filepath = models.CharField(db_column='FILEPATH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mailid = models.BigIntegerField(db_column='MAILID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OUT_MAIL_ATTACHMENT'


class OutMailLinkman(models.Model):
    linkid = models.BigIntegerField(db_column='LINKID', primary_key=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    mailid = models.BigIntegerField(db_column='MAILID', blank=True, null=True)  # Field name made lowercase.
    sendtime = models.DateTimeField(db_column='SENDTIME', blank=True, null=True)  # Field name made lowercase.
    linkname = models.CharField(db_column='LINKNAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    linkaddress = models.CharField(db_column='LINKADDRESS', max_length=2000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OUT_MAIL_LINKMAN'


class OutMailUserSeting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    mailaddress = models.CharField(db_column='MAILADDRESS', max_length=128, blank=True, null=True)  # Field name made lowercase.
    mailpass = models.CharField(db_column='MAILPASS', max_length=128, blank=True, null=True)  # Field name made lowercase.
    smtphost = models.CharField(db_column='SMTPHOST', max_length=128, blank=True, null=True)  # Field name made lowercase.
    smtpport = models.CharField(db_column='SMTPPORT', max_length=64, blank=True, null=True)  # Field name made lowercase.
    pophost = models.CharField(db_column='POPHOST', max_length=128, blank=True, null=True)  # Field name made lowercase.
    popport = models.CharField(db_column='POPPORT', max_length=64, blank=True, null=True)  # Field name made lowercase.
    imaphost = models.CharField(db_column='IMAPHOST', max_length=128, blank=True, null=True)  # Field name made lowercase.
    imapport = models.CharField(db_column='IMAPPORT', max_length=128, blank=True, null=True)  # Field name made lowercase.
    isdefault = models.SmallIntegerField(db_column='ISDEFAULT', blank=True, null=True)  # Field name made lowercase.
    mailtype = models.CharField(db_column='MAILTYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    usessl = models.SmallIntegerField(db_column='USESSL', blank=True, null=True)  # Field name made lowercase.
    isdeleteremote = models.SmallIntegerField(db_column='ISDELETEREMOTE', blank=True, null=True)  # Field name made lowercase.
    isvalidate = models.SmallIntegerField(db_column='ISVALIDATE', blank=True, null=True)  # Field name made lowercase.
    ishandleattach = models.SmallIntegerField(db_column='ISHANDLEATTACH', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OUT_MAIL_USER_SETING'


class QrtzBlobTriggers(models.Model):
    sched_name = models.ForeignKey('QrtzTriggers', db_column='SCHED_NAME')  # Field name made lowercase.
    trigger_name = models.ForeignKey('QrtzTriggers', db_column='TRIGGER_NAME')  # Field name made lowercase.
    trigger_group = models.ForeignKey('QrtzTriggers', db_column='TRIGGER_GROUP')  # Field name made lowercase.
    blob_data = models.TextField(db_column='BLOB_DATA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QRTZ_BLOB_TRIGGERS'
        unique_together = (('SCHED_NAME', 'TRIGGER_NAME', 'TRIGGER_GROUP'),)


class QrtzCalendars(models.Model):
    sched_name = models.CharField(db_column='SCHED_NAME', max_length=120)  # Field name made lowercase.
    calendar_name = models.CharField(db_column='CALENDAR_NAME', max_length=200)  # Field name made lowercase.
    calendar = models.TextField(db_column='CALENDAR')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QRTZ_CALENDARS'
        unique_together = (('SCHED_NAME', 'CALENDAR_NAME'),)


class QrtzCronTriggers(models.Model):
    sched_name = models.ForeignKey('QrtzTriggers', db_column='SCHED_NAME')  # Field name made lowercase.
    trigger_name = models.ForeignKey('QrtzTriggers', db_column='TRIGGER_NAME')  # Field name made lowercase.
    trigger_group = models.ForeignKey('QrtzTriggers', db_column='TRIGGER_GROUP')  # Field name made lowercase.
    cron_expression = models.CharField(db_column='CRON_EXPRESSION', max_length=120)  # Field name made lowercase.
    time_zone_id = models.CharField(db_column='TIME_ZONE_ID', max_length=80, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QRTZ_CRON_TRIGGERS'
        unique_together = (('SCHED_NAME', 'TRIGGER_NAME', 'TRIGGER_GROUP'),)


class QrtzFiredTriggers(models.Model):
    sched_name = models.CharField(db_column='SCHED_NAME', max_length=120)  # Field name made lowercase.
    entry_id = models.CharField(db_column='ENTRY_ID', max_length=95)  # Field name made lowercase.
    trigger_name = models.CharField(db_column='TRIGGER_NAME', max_length=140)  # Field name made lowercase.
    trigger_group = models.CharField(db_column='TRIGGER_GROUP', max_length=50)  # Field name made lowercase.
    instance_name = models.CharField(db_column='INSTANCE_NAME', max_length=200)  # Field name made lowercase.
    fired_time = models.BigIntegerField(db_column='FIRED_TIME')  # Field name made lowercase.
    priority = models.BigIntegerField(db_column='PRIORITY')  # Field name made lowercase.
    state = models.CharField(db_column='STATE', max_length=16)  # Field name made lowercase.
    job_name = models.CharField(db_column='JOB_NAME', max_length=150, blank=True, null=True)  # Field name made lowercase.
    job_group = models.CharField(db_column='JOB_GROUP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    is_nonconcurrent = models.CharField(db_column='IS_NONCONCURRENT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    requests_recovery = models.CharField(db_column='REQUESTS_RECOVERY', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QRTZ_FIRED_TRIGGERS'
        unique_together = (('SCHED_NAME', 'ENTRY_ID'),)


class QrtzJobDetails(models.Model):
    sched_name = models.CharField(db_column='SCHED_NAME', max_length=120)  # Field name made lowercase.
    job_name = models.CharField(db_column='JOB_NAME', max_length=150)  # Field name made lowercase.
    job_group = models.CharField(db_column='JOB_GROUP', max_length=50)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=250, blank=True, null=True)  # Field name made lowercase.
    job_class_name = models.CharField(db_column='JOB_CLASS_NAME', max_length=250)  # Field name made lowercase.
    is_durable = models.CharField(db_column='IS_DURABLE', max_length=1)  # Field name made lowercase.
    is_nonconcurrent = models.CharField(db_column='IS_NONCONCURRENT', max_length=1)  # Field name made lowercase.
    is_update_data = models.CharField(db_column='IS_UPDATE_DATA', max_length=1)  # Field name made lowercase.
    requests_recovery = models.CharField(db_column='REQUESTS_RECOVERY', max_length=1)  # Field name made lowercase.
    job_data = models.TextField(db_column='JOB_DATA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QRTZ_JOB_DETAILS'
        unique_together = (('SCHED_NAME', 'JOB_NAME', 'JOB_GROUP'),)


class QrtzLocks(models.Model):
    sched_name = models.CharField(db_column='SCHED_NAME', max_length=120)  # Field name made lowercase.
    lock_name = models.CharField(db_column='LOCK_NAME', max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QRTZ_LOCKS'
        unique_together = (('SCHED_NAME', 'LOCK_NAME'),)


class QrtzPausedTriggerGrps(models.Model):
    sched_name = models.CharField(db_column='SCHED_NAME', max_length=120)  # Field name made lowercase.
    trigger_group = models.CharField(db_column='TRIGGER_GROUP', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QRTZ_PAUSED_TRIGGER_GRPS'
        unique_together = (('SCHED_NAME', 'TRIGGER_GROUP'),)


class QrtzSchedulerState(models.Model):
    sched_name = models.CharField(db_column='SCHED_NAME', max_length=120)  # Field name made lowercase.
    instance_name = models.CharField(db_column='INSTANCE_NAME', max_length=200)  # Field name made lowercase.
    last_checkin_time = models.BigIntegerField(db_column='LAST_CHECKIN_TIME')  # Field name made lowercase.
    checkin_interval = models.BigIntegerField(db_column='CHECKIN_INTERVAL')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QRTZ_SCHEDULER_STATE'
        unique_together = (('SCHED_NAME', 'INSTANCE_NAME'),)


class QrtzSimpleTriggers(models.Model):
    sched_name = models.ForeignKey('QrtzTriggers', db_column='SCHED_NAME')  # Field name made lowercase.
    trigger_name = models.ForeignKey('QrtzTriggers', db_column='TRIGGER_NAME')  # Field name made lowercase.
    trigger_group = models.ForeignKey('QrtzTriggers', db_column='TRIGGER_GROUP')  # Field name made lowercase.
    repeat_count = models.BigIntegerField(db_column='REPEAT_COUNT')  # Field name made lowercase.
    repeat_interval = models.BigIntegerField(db_column='REPEAT_INTERVAL')  # Field name made lowercase.
    times_triggered = models.BigIntegerField(db_column='TIMES_TRIGGERED')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QRTZ_SIMPLE_TRIGGERS'
        unique_together = (('SCHED_NAME', 'TRIGGER_NAME', 'TRIGGER_GROUP'),)


class QrtzSimpropTriggers(models.Model):
    sched_name = models.ForeignKey('QrtzTriggers', db_column='SCHED_NAME')  # Field name made lowercase.
    trigger_name = models.ForeignKey('QrtzTriggers', db_column='TRIGGER_NAME')  # Field name made lowercase.
    trigger_group = models.ForeignKey('QrtzTriggers', db_column='TRIGGER_GROUP')  # Field name made lowercase.
    str_prop_1 = models.CharField(db_column='STR_PROP_1', max_length=512, blank=True, null=True)  # Field name made lowercase.
    str_prop_2 = models.CharField(db_column='STR_PROP_2', max_length=512, blank=True, null=True)  # Field name made lowercase.
    str_prop_3 = models.CharField(db_column='STR_PROP_3', max_length=512, blank=True, null=True)  # Field name made lowercase.
    int_prop_1 = models.BigIntegerField(db_column='INT_PROP_1', blank=True, null=True)  # Field name made lowercase.
    int_prop_2 = models.BigIntegerField(db_column='INT_PROP_2', blank=True, null=True)  # Field name made lowercase.
    long_prop_1 = models.BigIntegerField(db_column='LONG_PROP_1', blank=True, null=True)  # Field name made lowercase.
    long_prop_2 = models.BigIntegerField(db_column='LONG_PROP_2', blank=True, null=True)  # Field name made lowercase.
    dec_prop_1 = models.DecimalField(db_column='DEC_PROP_1', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    dec_prop_2 = models.DecimalField(db_column='DEC_PROP_2', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    bool_prop_1 = models.CharField(db_column='BOOL_PROP_1', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bool_prop_2 = models.CharField(db_column='BOOL_PROP_2', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QRTZ_SIMPROP_TRIGGERS'
        unique_together = (('SCHED_NAME', 'TRIGGER_NAME', 'TRIGGER_GROUP'),)


class QrtzTriggers(models.Model):
    sched_name = models.ForeignKey(QrtzJobDetails, db_column='SCHED_NAME')  # Field name made lowercase.
    trigger_name = models.CharField(db_column='TRIGGER_NAME', max_length=140)  # Field name made lowercase.
    trigger_group = models.CharField(db_column='TRIGGER_GROUP', max_length=50)  # Field name made lowercase.
    job_name = models.ForeignKey(QrtzJobDetails, db_column='JOB_NAME')  # Field name made lowercase.
    job_group = models.ForeignKey(QrtzJobDetails, db_column='JOB_GROUP')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=250, blank=True, null=True)  # Field name made lowercase.
    next_fire_time = models.BigIntegerField(db_column='NEXT_FIRE_TIME', blank=True, null=True)  # Field name made lowercase.
    prev_fire_time = models.BigIntegerField(db_column='PREV_FIRE_TIME', blank=True, null=True)  # Field name made lowercase.
    priority = models.BigIntegerField(db_column='PRIORITY', blank=True, null=True)  # Field name made lowercase.
    trigger_state = models.CharField(db_column='TRIGGER_STATE', max_length=16)  # Field name made lowercase.
    trigger_type = models.CharField(db_column='TRIGGER_TYPE', max_length=8)  # Field name made lowercase.
    start_time = models.BigIntegerField(db_column='START_TIME')  # Field name made lowercase.
    end_time = models.BigIntegerField(db_column='END_TIME', blank=True, null=True)  # Field name made lowercase.
    calendar_name = models.CharField(db_column='CALENDAR_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    misfire_instr = models.SmallIntegerField(db_column='MISFIRE_INSTR', blank=True, null=True)  # Field name made lowercase.
    job_data = models.TextField(db_column='JOB_DATA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QRTZ_TRIGGERS'
        unique_together = (('SCHED_NAME', 'TRIGGER_NAME', 'TRIGGER_GROUP'),)


class RepLabel(models.Model):
    lbl_id = models.BigIntegerField(db_column='LBL_ID', primary_key=True)  # Field name made lowercase.
    lbl_code = models.CharField(db_column='LBL_CODE', max_length=100)  # Field name made lowercase.
    lbl_label = models.CharField(db_column='LBL_LABEL', max_length=100)  # Field name made lowercase.
    lbl_module = models.CharField(db_column='LBL_MODULE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lbl_category = models.CharField(db_column='LBL_CATEGORY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lbl_comments = models.CharField(db_column='LBL_COMMENTS', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lbl_page = models.CharField(db_column='LBL_PAGE', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REP_LABEL'


class RepLabelLocale(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    lbl_code = models.CharField(db_column='LBL_CODE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lal_value = models.CharField(db_column='LAL_VALUE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lal_locale = models.CharField(db_column='LAL_LOCALE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lal_updated = models.DateTimeField(db_column='LAL_UPDATED', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REP_LABEL_LOCALE'


class RepLocale(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=20)  # Field name made lowercase.
    locale = models.CharField(db_column='LOCALE', max_length=20)  # Field name made lowercase.
    active = models.SmallIntegerField(db_column='ACTIVE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REP_LOCALE'


class RepMsg(models.Model):
    msg_id = models.BigIntegerField(db_column='MSG_ID', primary_key=True)  # Field name made lowercase.
    msg_code = models.CharField(db_column='MSG_CODE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    msg_desc = models.CharField(db_column='MSG_DESC', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    msg_category = models.CharField(db_column='MSG_CATEGORY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    msg_page = models.CharField(db_column='MSG_PAGE', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REP_MSG'


class RepMsgLocale(models.Model):
    msl_id = models.BigIntegerField(db_column='MSL_ID', primary_key=True)  # Field name made lowercase.
    msl_value = models.CharField(db_column='MSL_VALUE', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    msl_locale = models.CharField(db_column='MSL_LOCALE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    msg_code = models.CharField(db_column='MSG_CODE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    msl_updated = models.DateTimeField(db_column='MSL_UPDATED', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REP_MSG_LOCALE'


class SysAcceptIp(models.Model):
    acceptid = models.BigIntegerField(db_column='ACCEPTID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=128, blank=True, null=True)  # Field name made lowercase.
    startip = models.CharField(db_column='STARTIP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    endip = models.CharField(db_column='ENDIP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_ACCEPT_IP'


class SysAliasScript(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    alias_name = models.CharField(db_column='ALIAS_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    alias_desc = models.CharField(db_column='ALIAS_DESC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    class_name = models.CharField(db_column='CLASS_NAME', max_length=400, blank=True, null=True)  # Field name made lowercase.
    class_ins_name = models.CharField(db_column='CLASS_INS_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    method_name = models.CharField(db_column='METHOD_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    method_desc = models.CharField(db_column='METHOD_DESC', max_length=400, blank=True, null=True)  # Field name made lowercase.
    script_comten = models.TextField(db_column='SCRIPT_COMTEN', blank=True, null=True)  # Field name made lowercase.
    return_type = models.CharField(db_column='RETURN_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    script_type = models.CharField(db_column='SCRIPT_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    argument = models.TextField(db_column='ARGUMENT', blank=True, null=True)  # Field name made lowercase.
    enable = models.DecimalField(db_column='ENABLE', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_ALIAS_SCRIPT'


class SysAudit(models.Model):
    auditid = models.BigIntegerField(db_column='AUDITID', primary_key=True)  # Field name made lowercase.
    opname = models.CharField(db_column='OPNAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    exetime = models.DateTimeField(db_column='EXETIME', blank=True, null=True)  # Field name made lowercase.
    executorid = models.BigIntegerField(db_column='EXECUTORID', blank=True, null=True)  # Field name made lowercase.
    executor = models.CharField(db_column='EXECUTOR', max_length=64, blank=True, null=True)  # Field name made lowercase.
    fromip = models.CharField(db_column='FROMIP', max_length=64, blank=True, null=True)  # Field name made lowercase.
    exemethod = models.CharField(db_column='EXEMETHOD', max_length=128, blank=True, null=True)  # Field name made lowercase.
    requesturi = models.CharField(db_column='REQUESTURI', max_length=256, blank=True, null=True)  # Field name made lowercase.
    reqparams = models.TextField(db_column='REQPARAMS', blank=True, null=True)  # Field name made lowercase.
    ownermodel = models.CharField(db_column='OWNERMODEL', max_length=200, blank=True, null=True)  # Field name made lowercase.
    exectype = models.CharField(db_column='EXECTYPE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  # Field name made lowercase.
    detail = models.TextField(db_column='DETAIL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_AUDIT'


class SysAuthRole(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    auth_id = models.BigIntegerField(db_column='AUTH_ID', blank=True, null=True)  # Field name made lowercase.
    role_id = models.BigIntegerField(db_column='ROLE_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_AUTH_ROLE'


class SysCalendar(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=400, blank=True, null=True)  # Field name made lowercase.
    isdefault = models.BigIntegerField(db_column='ISDEFAULT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_CALENDAR'


class SysCalendarAssign(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    canlendarid = models.BigIntegerField(db_column='CANLENDARID', blank=True, null=True)  # Field name made lowercase.
    assigntype = models.SmallIntegerField(db_column='ASSIGNTYPE', blank=True, null=True)  # Field name made lowercase.
    assignid = models.BigIntegerField(db_column='ASSIGNID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_CALENDAR_ASSIGN'


class SysCalendarSetting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    calendarid = models.BigIntegerField(db_column='CALENDARID', blank=True, null=True)  # Field name made lowercase.
    years = models.SmallIntegerField(db_column='YEARS', blank=True, null=True)  # Field name made lowercase.
    months = models.SmallIntegerField(db_column='MONTHS', blank=True, null=True)  # Field name made lowercase.
    days = models.SmallIntegerField(db_column='DAYS', blank=True, null=True)  # Field name made lowercase.
    type = models.SmallIntegerField(db_column='TYPE', blank=True, null=True)  # Field name made lowercase.
    worktimeid = models.BigIntegerField(db_column='WORKTIMEID')  # Field name made lowercase.
    calday = models.CharField(db_column='CALDAY', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_CALENDAR_SETTING'


class SysCodeTemplate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='TEMPLATE_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    html = models.TextField(db_column='HTML', blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  # Field name made lowercase.
    template_alias = models.CharField(db_column='TEMPLATE_ALIAS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    template_type = models.SmallIntegerField(db_column='TEMPLATE_TYPE', blank=True, null=True)  # Field name made lowercase.
    issubneed = models.SmallIntegerField(db_column='ISSUBNEED', blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FILENAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    filedir = models.CharField(db_column='FILEDIR', max_length=200, blank=True, null=True)  # Field name made lowercase.
    formedit = models.SmallIntegerField(db_column='FORMEDIT', blank=True, null=True)  # Field name made lowercase.
    formdetail = models.SmallIntegerField(db_column='FORMDETAIL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_CODE_TEMPLATE'


class SysConditionScript(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    class_name = models.CharField(db_column='CLASS_NAME', max_length=400, blank=True, null=True)  # Field name made lowercase.
    class_ins_name = models.CharField(db_column='CLASS_INS_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    method_name = models.CharField(db_column='METHOD_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    method_desc = models.CharField(db_column='METHOD_DESC', max_length=400, blank=True, null=True)  # Field name made lowercase.
    return_type = models.CharField(db_column='RETURN_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    argument = models.TextField(db_column='ARGUMENT', blank=True, null=True)  # Field name made lowercase.
    enable = models.SmallIntegerField(db_column='ENABLE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_CONDITION_SCRIPT'


class SysDatasource(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    drivername = models.CharField(db_column='DRIVERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dbtype = models.CharField(db_column='DBTYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_DATASOURCE'


class SysDataSource(models.Model):
    id_field = models.DecimalField(db_column='ID_', primary_key=True, max_digits=18, decimal_places=0)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    alias_field = models.CharField(db_column='ALIAS_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    db_type_field = models.CharField(db_column='DB_TYPE_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    setting_json_field = models.TextField(db_column='SETTING_JSON_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    init_on_start_field = models.SmallIntegerField(db_column='INIT_ON_START_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    enabled_field = models.SmallIntegerField(db_column='ENABLED_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    class_path_field = models.CharField(db_column='CLASS_PATH_', max_length=128, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    init_method_field = models.CharField(db_column='INIT_METHOD_', max_length=128, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    close_method_field = models.CharField(db_column='CLOSE_METHOD_', max_length=128, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'SYS_DATA_SOURCE'
        unique_together = (('NAME_', 'ALIAS_'),)


class SysDataSourceDef(models.Model):
    id_field = models.DecimalField(db_column='ID_', primary_key=True, max_digits=18, decimal_places=0)  # Field name made lowercase. Field renamed because it ended with '_'.
    name_field = models.CharField(db_column='NAME_', max_length=64)  # Field name made lowercase. Field renamed because it ended with '_'.
    class_path_field = models.CharField(db_column='CLASS_PATH_', max_length=128)  # Field name made lowercase. Field renamed because it ended with '_'.
    setting_json_field = models.TextField(db_column='SETTING_JSON_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    init_method_field = models.CharField(db_column='INIT_METHOD_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    is_system_field = models.SmallIntegerField(db_column='IS_SYSTEM_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    close_method_field = models.CharField(db_column='CLOSE_METHOD_', max_length=64, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'SYS_DATA_SOURCE_DEF'
        unique_together = (('CLASS_PATH_', 'NAME_'),)


class SysDbId(models.Model):
    id = models.SmallIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    incremental = models.BigIntegerField(db_column='INCREMENTAL', blank=True, null=True)  # Field name made lowercase.
    bound = models.BigIntegerField(db_column='BOUND', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_DB_ID'


class SysDemension(models.Model):
    demid = models.BigIntegerField(db_column='DEMID', primary_key=True)  # Field name made lowercase.
    demname = models.CharField(db_column='DEMNAME', max_length=128)  # Field name made lowercase.
    demdesc = models.CharField(db_column='DEMDESC', max_length=1024, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_DEMENSION'


class SysDesktopColumn(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    servicemethod = models.CharField(db_column='SERVICEMETHOD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    templatename = models.CharField(db_column='TEMPLATENAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    templateid = models.CharField(db_column='TEMPLATEID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    templatepath = models.CharField(db_column='TEMPLATEPATH', max_length=200, blank=True, null=True)  # Field name made lowercase.
    columnurl = models.CharField(db_column='COLUMNURL', max_length=200, blank=True, null=True)  # Field name made lowercase.
    html = models.TextField(db_column='HTML', blank=True, null=True)  # Field name made lowercase.
    issys = models.SmallIntegerField(db_column='ISSYS', blank=True, null=True)  # Field name made lowercase.
    methodtype = models.SmallIntegerField(db_column='METHODTYPE', blank=True, null=True)  # Field name made lowercase.
    queryalias = models.CharField(db_column='QUERYALIAS', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_DESKTOP_COLUMN'


class SysDesktopLayout(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cols = models.SmallIntegerField(db_column='COLS', blank=True, null=True)  # Field name made lowercase.
    width = models.CharField(db_column='WIDTH', max_length=50, blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    isdefault = models.BigIntegerField(db_column='ISDEFAULT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_DESKTOP_LAYOUT'


class SysDesktopLayoutcol(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    layoutid = models.BigIntegerField(db_column='LAYOUTID', blank=True, null=True)  # Field name made lowercase.
    columnid = models.BigIntegerField(db_column='COLUMNID', blank=True, null=True)  # Field name made lowercase.
    col = models.BigIntegerField(db_column='COL', blank=True, null=True)  # Field name made lowercase.
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_DESKTOP_LAYOUTCOL'


class SysDesktopMycolumn(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    layoutid = models.BigIntegerField(db_column='LAYOUTID', blank=True, null=True)  # Field name made lowercase.
    columnid = models.BigIntegerField(db_column='COLUMNID', blank=True, null=True)  # Field name made lowercase.
    col = models.SmallIntegerField(db_column='COL', blank=True, null=True)  # Field name made lowercase.
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  # Field name made lowercase.
    columnname = models.CharField(db_column='COLUMNNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    servicemethod = models.CharField(db_column='SERVICEMETHOD', max_length=400, blank=True, null=True)  # Field name made lowercase.
    columnhtml = models.CharField(db_column='COLUMNHTML', max_length=200, blank=True, null=True)  # Field name made lowercase.
    columnurl = models.CharField(db_column='COLUMNURL', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_DESKTOP_MYCOLUMN'


class SysDic(models.Model):
    dicid = models.BigIntegerField(db_column='DICID', primary_key=True)  # Field name made lowercase.
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  # Field name made lowercase.
    itemkey = models.CharField(db_column='ITEMKEY', max_length=64, blank=True, null=True)  # Field name made lowercase.
    itemname = models.CharField(db_column='ITEMNAME', max_length=64)  # Field name made lowercase.
    itemvalue = models.CharField(db_column='ITEMVALUE', max_length=128)  # Field name made lowercase.
    descp = models.CharField(db_column='DESCP', max_length=256, blank=True, null=True)  # Field name made lowercase.
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  # Field name made lowercase.
    nodepath = models.CharField(db_column='NODEPATH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_DIC'


class SysErrorLog(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    hashcode = models.CharField(db_column='HASHCODE', max_length=40, blank=True, null=True)  # Field name made lowercase.
    account = models.CharField(db_column='ACCOUNT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=30, blank=True, null=True)  # Field name made lowercase.
    errorurl = models.CharField(db_column='ERRORURL', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    error = models.TextField(db_column='ERROR', blank=True, null=True)  # Field name made lowercase.
    errordate = models.DateTimeField(db_column='ERRORDATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_ERROR_LOG'


class SysExcelImprule(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    table_name = models.CharField(db_column='TABLE_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    column_str = models.CharField(db_column='COLUMN_STR', max_length=200, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=200, blank=True, null=True)  # Field name made lowercase.
    imp_type = models.SmallIntegerField(db_column='IMP_TYPE', blank=True, null=True)  # Field name made lowercase.
    busi_date = models.DateTimeField(db_column='BUSI_DATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_EXCEL_IMPRULE'


class SysFile(models.Model):
    fileid = models.CharField(db_column='FILEID', primary_key=True, max_length=80)  # Field name made lowercase.
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FILENAME', max_length=128)  # Field name made lowercase.
    filepath = models.CharField(db_column='FILEPATH', max_length=128)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.
    ext = models.CharField(db_column='EXT', max_length=32, blank=True, null=True)  # Field name made lowercase.
    filetype = models.CharField(db_column='FILETYPE', max_length=32)  # Field name made lowercase.
    note = models.CharField(db_column='NOTE', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=32)  # Field name made lowercase.
    totalbytes = models.BigIntegerField(db_column='TOTALBYTES', blank=True, null=True)  # Field name made lowercase.
    delflag = models.SmallIntegerField(db_column='DELFLAG', blank=True, null=True)  # Field name made lowercase.
    fileblob = models.TextField(db_column='FILEBLOB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_FILE'


class SysGlType(models.Model):
    typeid = models.BigIntegerField(db_column='TYPEID', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='TYPENAME', max_length=128)  # Field name made lowercase.
    nodepath = models.CharField(db_column='NODEPATH', max_length=200, blank=True, null=True)  # Field name made lowercase.
    depth = models.BigIntegerField(db_column='DEPTH')  # Field name made lowercase.
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  # Field name made lowercase.
    catkey = models.CharField(db_column='CATKEY', max_length=64, blank=True, null=True)  # Field name made lowercase.
    nodekey = models.CharField(db_column='NODEKEY', max_length=64)  # Field name made lowercase.
    sn = models.BigIntegerField(db_column='SN')  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    depid = models.BigIntegerField(db_column='DEPID', blank=True, null=True)  # Field name made lowercase.
    type = models.BigIntegerField(db_column='TYPE', blank=True, null=True)  # Field name made lowercase.
    isleaf = models.SmallIntegerField(db_column='ISLEAF', blank=True, null=True)  # Field name made lowercase.
    nodecode = models.CharField(db_column='NODECODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nodecodetype = models.SmallIntegerField(db_column='NODECODETYPE', blank=True, null=True)  # Field name made lowercase.
    datasources = models.IntegerField(db_column='dataSources', blank=True, null=True)  # Field name made lowercase.
    custdata = models.CharField(db_column='custData', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_GL_TYPE'


class SysIdentity(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    regulation = models.CharField(db_column='REGULATION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    gentype = models.SmallIntegerField(db_column='GENTYPE', blank=True, null=True)  # Field name made lowercase.
    nolength = models.BigIntegerField(db_column='NOLENGTH', blank=True, null=True)  # Field name made lowercase.
    curdate = models.CharField(db_column='CURDATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    initvalue = models.BigIntegerField(db_column='INITVALUE', blank=True, null=True)  # Field name made lowercase.
    curvalue = models.BigIntegerField(db_column='CURVALUE', blank=True, null=True)  # Field name made lowercase.
    step = models.SmallIntegerField(db_column='STEP', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_IDENTITY'


class SysJob(models.Model):
    jobid = models.BigIntegerField(db_column='JOBID', primary_key=True)  # Field name made lowercase.
    jobname = models.CharField(db_column='JOBNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    jobcode = models.CharField(db_column='JOBCODE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    jobdesc = models.CharField(db_column='JOBDESC', max_length=400, blank=True, null=True)  # Field name made lowercase.
    setid = models.BigIntegerField(db_column='SETID', blank=True, null=True)  # Field name made lowercase.
    isdelete = models.BigIntegerField(db_column='ISDELETE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_JOB'


class SysJoblog(models.Model):
    logid = models.BigIntegerField(db_column='LOGID', primary_key=True)  # Field name made lowercase.
    jobname = models.CharField(db_column='JOBNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    trigname = models.CharField(db_column='TRIGNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='STARTTIME', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='CONTENT', blank=True, null=True)  # Field name made lowercase.
    state = models.BigIntegerField(db_column='STATE', blank=True, null=True)  # Field name made lowercase.
    runtime = models.BigIntegerField(db_column='RUNTIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_JOBLOG'


class SysLogSwitch(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    model = models.CharField(db_column='MODEL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  # Field name made lowercase.
    updby = models.CharField(db_column='UPDBY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    updbyid = models.BigIntegerField(db_column='UPDBYID', blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=300, blank=True, null=True)  # Field name made lowercase.
    lastuptime = models.DateTimeField(db_column='LASTUPTIME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_LOG_SWITCH'


class SysMessageLog(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sendtime = models.DateTimeField(db_column='SENDTIME', blank=True, null=True)  # Field name made lowercase.
    receiver = models.CharField(db_column='RECEIVER', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    messagetype = models.BigIntegerField(db_column='MESSAGETYPE', blank=True, null=True)  # Field name made lowercase.
    state = models.BigIntegerField(db_column='STATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_MESSAGE_LOG'


class SysMsgRead(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    messageid = models.BigIntegerField(db_column='MESSAGEID', blank=True, null=True)  # Field name made lowercase.
    receiverid = models.BigIntegerField(db_column='RECEIVERID', blank=True, null=True)  # Field name made lowercase.
    receiver = models.CharField(db_column='RECEIVER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    receivetime = models.DateTimeField(db_column='RECEIVETIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_MSG_READ'


class SysMsgReceiver(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    messageid = models.BigIntegerField(db_column='MESSAGEID', blank=True, null=True)  # Field name made lowercase.
    receivetype = models.SmallIntegerField(db_column='RECEIVETYPE', blank=True, null=True)  # Field name made lowercase.
    receiverid = models.BigIntegerField(db_column='RECEIVERID', blank=True, null=True)  # Field name made lowercase.
    receiver = models.CharField(db_column='RECEIVER', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_MSG_RECEIVER'


class SysMsgReply(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    messageid = models.BigIntegerField(db_column='MESSAGEID', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='CONTENT', blank=True, null=True)  # Field name made lowercase.
    replyid = models.BigIntegerField(db_column='REPLYID', blank=True, null=True)  # Field name made lowercase.
    reply = models.CharField(db_column='REPLY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    replytime = models.DateTimeField(db_column='REPLYTIME', blank=True, null=True)  # Field name made lowercase.
    isprivate = models.SmallIntegerField(db_column='ISPRIVATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_MSG_REPLY'


class SysMsgSend(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    messagetype = models.CharField(db_column='MESSAGETYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='CONTENT', blank=True, null=True)  # Field name made lowercase.
    sendtime = models.DateTimeField(db_column='SENDTIME', blank=True, null=True)  # Field name made lowercase.
    canreply = models.SmallIntegerField(db_column='CANREPLY', blank=True, null=True)  # Field name made lowercase.
    receivername = models.TextField(db_column='RECEIVERNAME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_MSG_SEND'


class SysOfficeTemplate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    templatetype = models.BigIntegerField(db_column='TEMPLATETYPE', blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  # Field name made lowercase.
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  # Field name made lowercase.
    path = models.CharField(db_column='PATH', max_length=200, blank=True, null=True)  # Field name made lowercase.
    templateblob = models.TextField(db_column='TEMPLATEBLOB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_OFFICE_TEMPLATE'


class SysOrg(models.Model):
    orgid = models.BigIntegerField(db_column='ORGID', primary_key=True)  # Field name made lowercase.
    demid = models.BigIntegerField(db_column='DEMID', blank=True, null=True)  # Field name made lowercase.
    orgname = models.CharField(db_column='ORGNAME', max_length=128)  # Field name made lowercase.
    orgdesc = models.CharField(db_column='ORGDESC', max_length=500, blank=True, null=True)  # Field name made lowercase.
    orgsupid = models.BigIntegerField(db_column='ORGSUPID', blank=True, null=True)  # Field name made lowercase.
    path = models.CharField(db_column='PATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    depth = models.BigIntegerField(db_column='DEPTH', blank=True, null=True)  # Field name made lowercase.
    orgtype = models.BigIntegerField(db_column='ORGTYPE', blank=True, null=True)  # Field name made lowercase.
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  # Field name made lowercase.
    updateid = models.BigIntegerField(db_column='UPDATEID', blank=True, null=True)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UPDATETIME', blank=True, null=True)  # Field name made lowercase.
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  # Field name made lowercase.
    fromtype = models.SmallIntegerField(db_column='FROMTYPE', blank=True, null=True)  # Field name made lowercase.
    orgpathname = models.CharField(db_column='ORGPATHNAME', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    isdelete = models.IntegerField(db_column='ISDELETE', blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=128, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_ORG'


class SysOrgAuth(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user_id = models.BigIntegerField(db_column='USER_ID')  # Field name made lowercase.
    org_id = models.BigIntegerField(db_column='ORG_ID')  # Field name made lowercase.
    dim_id = models.BigIntegerField(db_column='DIM_ID')  # Field name made lowercase.
    org_perms = models.CharField(db_column='ORG_PERMS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    user_perms = models.CharField(db_column='USER_PERMS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_ORG_AUTH'


class SysOrgParam(models.Model):
    valueid = models.BigIntegerField(db_column='VALUEID', blank=True, null=True)  # Field name made lowercase.
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  # Field name made lowercase.
    paramid = models.BigIntegerField(db_column='PARAMID', blank=True, null=True)  # Field name made lowercase.
    paramvalue = models.CharField(db_column='PARAMVALUE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    paramdatevalue = models.DateTimeField(db_column='PARAMDATEVALUE', blank=True, null=True)  # Field name made lowercase.
    paramintvalue = models.DecimalField(db_column='PARAMINTVALUE', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_ORG_PARAM'


class SysOrgRole(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  # Field name made lowercase.
    roleid = models.BigIntegerField(db_column='ROLEID', blank=True, null=True)  # Field name made lowercase.
    candel = models.SmallIntegerField(db_column='CANDEL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_ORG_ROLE'


class SysOrgRolemanage(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  # Field name made lowercase.
    roleid = models.BigIntegerField(db_column='ROLEID', blank=True, null=True)  # Field name made lowercase.
    candel = models.SmallIntegerField(db_column='CANDEL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_ORG_ROLEMANAGE'


class SysOrgType(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    demid = models.BigIntegerField(db_column='DEMID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    levels = models.SmallIntegerField(db_column='LEVELS', blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    icon = models.CharField(db_column='ICON', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_ORG_TYPE'


class SysOvertime(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='STARTTIME', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  # Field name made lowercase.
    worktype = models.SmallIntegerField(db_column='WORKTYPE', blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_OVERTIME'


class SysParam(models.Model):
    paramid = models.BigIntegerField(db_column='PARAMID', primary_key=True)  # Field name made lowercase.
    paramkey = models.CharField(db_column='PARAMKEY', max_length=32, blank=True, null=True)  # Field name made lowercase.
    paramname = models.CharField(db_column='PARAMNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    datatype = models.CharField(db_column='DATATYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    effect = models.SmallIntegerField(db_column='EFFECT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_PARAM'


class SysPaur(models.Model):
    paurid = models.BigIntegerField(db_column='PAURID', primary_key=True)  # Field name made lowercase.
    paurname = models.CharField(db_column='PAURNAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    aliasname = models.CharField(db_column='ALIASNAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    paurvalue = models.CharField(db_column='PAURVALUE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_PAUR'


class SysPersonScript(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    class_name = models.CharField(db_column='CLASS_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    class_ins_name = models.CharField(db_column='CLASS_INS_NAME', max_length=400, blank=True, null=True)  # Field name made lowercase.
    method_name = models.CharField(db_column='METHOD_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    method_desc = models.CharField(db_column='METHOD_DESC', max_length=200, blank=True, null=True)  # Field name made lowercase.
    return_type = models.CharField(db_column='RETURN_TYPE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    argument = models.CharField(db_column='ARGUMENT', max_length=200, blank=True, null=True)  # Field name made lowercase.
    enable = models.DecimalField(db_column='ENABLE', max_digits=1, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_PERSON_SCRIPT'


class SysPos(models.Model):
    posid = models.BigIntegerField(db_column='POSID', primary_key=True)  # Field name made lowercase.
    posname = models.CharField(db_column='POSNAME', max_length=100)  # Field name made lowercase.
    posdesc = models.CharField(db_column='POSDESC', max_length=200, blank=True, null=True)  # Field name made lowercase.
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  # Field name made lowercase.
    jobid = models.BigIntegerField(db_column='JOBID', blank=True, null=True)  # Field name made lowercase.
    isdelete = models.IntegerField(db_column='ISDELETE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_POS'


class SysPosition(models.Model):
    posid = models.BigIntegerField(db_column='POSID', primary_key=True)  # Field name made lowercase.
    posname = models.CharField(db_column='POSNAME', max_length=128)  # Field name made lowercase.
    posdesc = models.CharField(db_column='POSDESC', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  # Field name made lowercase.
    nodepath = models.CharField(db_column='NODEPATH', max_length=256, blank=True, null=True)  # Field name made lowercase.
    depth = models.IntegerField(db_column='DEPTH', blank=True, null=True)  # Field name made lowercase.
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  # Field name made lowercase.
    isleaf = models.SmallIntegerField(db_column='ISLEAF', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_POSITION'


class SysPosSub(models.Model):
    mainpositionid = models.BigIntegerField(db_column='MAINPOSITIONID')  # Field name made lowercase.
    subpositionid = models.BigIntegerField(db_column='SUBPOSITIONID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_POS_SUB'
        unique_together = (('MAINPOSITIONID', 'SUBPOSITIONID'),)


class SysProfile(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    homepage = models.CharField(db_column='HOMEPAGE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    skin = models.CharField(db_column='SKIN', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_PROFILE'


class SysQueryField(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sql_id = models.BigIntegerField(db_column='SQL_ID')  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    field_desc = models.CharField(db_column='FIELD_DESC', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    is_show = models.IntegerField(db_column='IS_SHOW', blank=True, null=True)  # Field name made lowercase.
    is_search = models.IntegerField(db_column='IS_SEARCH', blank=True, null=True)  # Field name made lowercase.
    control_type = models.IntegerField(db_column='CONTROL_TYPE', blank=True, null=True)  # Field name made lowercase.
    control_content = models.CharField(db_column='CONTROL_CONTENT', max_length=200, blank=True, null=True)  # Field name made lowercase.
    format = models.CharField(db_column='FORMAT', max_length=400, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_QUERY_FIELD'


class SysQuerySetting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sql_id = models.BigIntegerField(db_column='SQL_ID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    style = models.IntegerField(db_column='STYLE', blank=True, null=True)  # Field name made lowercase.
    need_page = models.IntegerField(db_column='NEED_PAGE', blank=True, null=True)  # Field name made lowercase.
    page_size = models.IntegerField(db_column='PAGE_SIZE', blank=True, null=True)  # Field name made lowercase.
    is_query = models.IntegerField(db_column='IS_QUERY', blank=True, null=True)  # Field name made lowercase.
    template_alias = models.CharField(db_column='TEMPLATE_ALIAS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    template_html = models.TextField(db_column='TEMPLATE_HTML', blank=True, null=True)  # Field name made lowercase.
    display_field = models.TextField(db_column='DISPLAY_FIELD', blank=True, null=True)  # Field name made lowercase.
    filter_field = models.TextField(db_column='FILTER_FIELD', blank=True, null=True)  # Field name made lowercase.
    condition_field = models.TextField(db_column='CONDITION_FIELD', blank=True, null=True)  # Field name made lowercase.
    sort_field = models.TextField(db_column='SORT_FIELD', blank=True, null=True)  # Field name made lowercase.
    export_field = models.TextField(db_column='EXPORT_FIELD', blank=True, null=True)  # Field name made lowercase.
    manage_field = models.TextField(db_column='MANAGE_FIELD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_QUERY_SETTING'


class SysQuerySql(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sql_field = models.CharField(db_column='SQL_', max_length=2000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    name = models.CharField(db_column='NAME', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    dsalias = models.CharField(db_column='DSALIAS', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    url_params = models.CharField(db_column='URL_PARAMS', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.BigIntegerField(db_column='CATEGORYID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_QUERY_SQL'


class SysReport(models.Model):
    reportid = models.BigIntegerField(db_column='REPORTID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=128, blank=True, null=True)  # Field name made lowercase.
    descp = models.CharField(db_column='DESCP', max_length=200, blank=True, null=True)  # Field name made lowercase.
    filepath = models.CharField(db_column='FILEPATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FILENAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.
    status = models.DecimalField(db_column='STATUS', max_digits=1, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    dsname = models.CharField(db_column='DSNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    params = models.CharField(db_column='PARAMS', max_length=500, blank=True, null=True)  # Field name made lowercase.
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  # Field name made lowercase.
    ext = models.CharField(db_column='EXT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    realsql = models.TextField(db_column='REALSQL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_REPORT'


class SysReportTemplate(models.Model):
    reportid = models.BigIntegerField(db_column='REPORTID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=128)  # Field name made lowercase.
    descp = models.CharField(db_column='DESCP', max_length=500)  # Field name made lowercase.
    reportlocation = models.CharField(db_column='REPORTLOCATION', max_length=128)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UPDATETIME')  # Field name made lowercase.
    reportkey = models.CharField(db_column='REPORTKEY', max_length=128, blank=True, null=True)  # Field name made lowercase.
    isdefaultin = models.SmallIntegerField(db_column='ISDEFAULTIN', blank=True, null=True)  # Field name made lowercase.
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_REPORT_TEMPLATE'


class SysRes(models.Model):
    resid = models.BigIntegerField(db_column='RESID', primary_key=True)  # Field name made lowercase.
    resname = models.CharField(db_column='RESNAME', max_length=128)  # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=128, blank=True, null=True)  # Field name made lowercase.
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  # Field name made lowercase.
    icon = models.CharField(db_column='ICON', max_length=100, blank=True, null=True)  # Field name made lowercase.
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  # Field name made lowercase.
    defaulturl = models.CharField(db_column='DEFAULTURL', max_length=256, blank=True, null=True)  # Field name made lowercase.
    isfolder = models.SmallIntegerField(db_column='ISFOLDER', blank=True, null=True)  # Field name made lowercase.
    isdisplayinmenu = models.SmallIntegerField(db_column='ISDISPLAYINMENU', blank=True, null=True)  # Field name made lowercase.
    isopen = models.SmallIntegerField(db_column='ISOPEN', blank=True, null=True)  # Field name made lowercase.
    systemid = models.BigIntegerField(db_column='SYSTEMID', blank=True, null=True)  # Field name made lowercase.
    path = models.CharField(db_column='PATH', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_RES'


class SysResurl(models.Model):
    resurlid = models.BigIntegerField(db_column='RESURLID', primary_key=True)  # Field name made lowercase.
    resid = models.BigIntegerField(db_column='RESID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_RESURL'


class SysRole(models.Model):
    roleid = models.BigIntegerField(db_column='ROLEID', primary_key=True)  # Field name made lowercase.
    systemid = models.BigIntegerField(db_column='SYSTEMID', blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=128, blank=True, null=True)  # Field name made lowercase.
    rolename = models.CharField(db_column='ROLENAME', max_length=128)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=256, blank=True, null=True)  # Field name made lowercase.
    allowdel = models.SmallIntegerField(db_column='ALLOWDEL', blank=True, null=True)  # Field name made lowercase.
    allowedit = models.SmallIntegerField(db_column='ALLOWEDIT', blank=True, null=True)  # Field name made lowercase.
    enabled = models.SmallIntegerField(db_column='ENABLED', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_ROLE'


class SysRolePos(models.Model):
    posid = models.BigIntegerField(db_column='POSID')  # Field name made lowercase.
    roleid = models.BigIntegerField(db_column='ROLEID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_ROLE_POS'
        unique_together = (('POSID', 'ROLEID'),)


class SysRoleRes(models.Model):
    roleresid = models.BigIntegerField(db_column='ROLERESID', primary_key=True)  # Field name made lowercase.
    roleid = models.BigIntegerField(db_column='ROLEID', blank=True, null=True)  # Field name made lowercase.
    resid = models.BigIntegerField(db_column='RESID', blank=True, null=True)  # Field name made lowercase.
    systemid = models.BigIntegerField(db_column='SYSTEMID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_ROLE_RES'


class SysScript(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    script = models.TextField(db_column='SCRIPT', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_SCRIPT'


class SysSeal(models.Model):
    sealid = models.BigIntegerField(db_column='SEALID', primary_key=True)  # Field name made lowercase.
    sealname = models.CharField(db_column='SEALNAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    sealpath = models.CharField(db_column='SEALPATH', max_length=128, blank=True, null=True)  # Field name made lowercase.
    belongid = models.BigIntegerField(db_column='BELONGID', blank=True, null=True)  # Field name made lowercase.
    belongname = models.CharField(db_column='BELONGNAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    attachmentid = models.CharField(db_column='ATTACHMENTID', max_length=80, blank=True, null=True)  # Field name made lowercase.
    showimageid = models.CharField(db_column='SHOWIMAGEID', max_length=80, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_SEAL'


class SysSealRight(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sealid = models.BigIntegerField(db_column='SEALID', blank=True, null=True)  # Field name made lowercase.
    righttype = models.CharField(db_column='RIGHTTYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rightid = models.BigIntegerField(db_column='RIGHTID', blank=True, null=True)  # Field name made lowercase.
    rightname = models.CharField(db_column='RIGHTNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    createuser = models.CharField(db_column='CREATEUSER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME')  # Field name made lowercase.
    controltype = models.SmallIntegerField(db_column='CONTROLTYPE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_SEAL_RIGHT'


class SysSubsystem(models.Model):
    systemid = models.BigIntegerField(db_column='SYSTEMID', primary_key=True)  # Field name made lowercase.
    sysname = models.CharField(db_column='SYSNAME', max_length=50)  # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    logo = models.CharField(db_column='LOGO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    defaulturl = models.CharField(db_column='DEFAULTURL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    allowdel = models.SmallIntegerField(db_column='ALLOWDEL', blank=True, null=True)  # Field name made lowercase.
    needorg = models.SmallIntegerField(db_column='NEEDORG', blank=True, null=True)  # Field name made lowercase.
    isactive = models.SmallIntegerField(db_column='ISACTIVE', blank=True, null=True)  # Field name made lowercase.
    islocal = models.SmallIntegerField(db_column='ISLOCAL', blank=True, null=True)  # Field name made lowercase.
    homepage = models.CharField(db_column='HOMEPAGE', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_SUBSYSTEM'


class SysTemplate(models.Model):
    templateid = models.BigIntegerField(db_column='TEMPLATEID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isdefault = models.SmallIntegerField(db_column='ISDEFAULT', blank=True, null=True)  # Field name made lowercase.
    usetype = models.SmallIntegerField(db_column='USETYPE', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    plaincontent = models.CharField(db_column='PLAINCONTENT', max_length=500, blank=True, null=True)  # Field name made lowercase.
    htmlcontent = models.CharField(db_column='HTMLCONTENT', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_TEMPLATE'


class SysTypeKey(models.Model):
    typeid = models.BigIntegerField(db_column='TYPEID', primary_key=True)  # Field name made lowercase.
    typekey = models.CharField(db_column='TYPEKEY', max_length=64)  # Field name made lowercase.
    typename = models.CharField(db_column='TYPENAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    flag = models.BigIntegerField(db_column='FLAG', blank=True, null=True)  # Field name made lowercase.
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  # Field name made lowercase.
    type = models.BigIntegerField(db_column='TYPE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_TYPE_KEY'


class SysUrlPermission(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    descp_field = models.CharField(db_column='DESCP_', max_length=200, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    url_field = models.CharField(db_column='URL_', max_length=2000, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    params_field = models.CharField(db_column='PARAMS_', max_length=500, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    enable_field = models.SmallIntegerField(db_column='ENABLE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'SYS_URL_PERMISSION'


class SysUrlRules(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    script_field = models.TextField(db_column='SCRIPT_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    enable_field = models.SmallIntegerField(db_column='ENABLE_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    sys_url_id_field = models.BigIntegerField(db_column='SYS_URL_ID_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    descp_field = models.CharField(db_column='DESCP_', max_length=500, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    sort_field = models.SmallIntegerField(db_column='SORT_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'SYS_URL_RULES'


class SysUser(models.Model):
    userid = models.BigIntegerField(db_column='USERID', primary_key=True)  # Field name made lowercase.
    fullname = models.CharField(db_column='FULLNAME', max_length=127, blank=True, null=True)  # Field name made lowercase.
    account = models.CharField(db_column='ACCOUNT', max_length=20)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=50)  # Field name made lowercase.
    isexpired = models.SmallIntegerField(db_column='ISEXPIRED', blank=True, null=True)  # Field name made lowercase.
    islock = models.SmallIntegerField(db_column='ISLOCK', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=128, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='MOBILE', max_length=32, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=32, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='SEX', max_length=2, blank=True, null=True)  # Field name made lowercase.
    picture = models.CharField(db_column='PICTURE', max_length=300, blank=True, null=True)  # Field name made lowercase.
    fromtype = models.SmallIntegerField(db_column='FROMTYPE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_USER'


class SysUserOrg(models.Model):
    userorgid = models.BigIntegerField(db_column='USERORGID', primary_key=True)  # Field name made lowercase.
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    isprimary = models.SmallIntegerField(db_column='ISPRIMARY')  # Field name made lowercase.
    ischarge = models.BigIntegerField(db_column='ISCHARGE', blank=True, null=True)  # Field name made lowercase.
    isgrademanage = models.SmallIntegerField(db_column='ISGRADEMANAGE', blank=True, null=True)  # Field name made lowercase.
    isdelete = models.SmallIntegerField(db_column='ISDELETE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_USER_ORG'


class SysUserParam(models.Model):
    valueid = models.BigIntegerField(db_column='VALUEID', primary_key=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    paramid = models.BigIntegerField(db_column='PARAMID', blank=True, null=True)  # Field name made lowercase.
    paramvalue = models.CharField(db_column='PARAMVALUE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    paramdatevalue = models.DateTimeField(db_column='PARAMDATEVALUE', blank=True, null=True)  # Field name made lowercase.
    paramintvalue = models.BigIntegerField(db_column='PARAMINTVALUE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_USER_PARAM'


class SysUserPos(models.Model):
    userposid = models.BigIntegerField(db_column='USERPOSID', primary_key=True)  # Field name made lowercase.
    posid = models.BigIntegerField(db_column='POSID', blank=True, null=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    isprimary = models.SmallIntegerField(db_column='ISPRIMARY', blank=True, null=True)  # Field name made lowercase.
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  # Field name made lowercase.
    jobid = models.BigIntegerField(db_column='JOBID', blank=True, null=True)  # Field name made lowercase.
    ischarge = models.SmallIntegerField(db_column='ISCHARGE', blank=True, null=True)  # Field name made lowercase.
    isdelete = models.SmallIntegerField(db_column='ISDELETE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_USER_POS'


class SysUserRole(models.Model):
    userroleid = models.BigIntegerField(db_column='USERROLEID', primary_key=True)  # Field name made lowercase.
    roleid = models.BigIntegerField(db_column='ROLEID', blank=True, null=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_USER_ROLE'


class SysUserUnder(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  # Field name made lowercase.
    underuserid = models.BigIntegerField(db_column='UNDERUSERID', blank=True, null=True)  # Field name made lowercase.
    underusername = models.CharField(db_column='UNDERUSERNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_USER_UNDER'


class SysVacation(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    years = models.SmallIntegerField(db_column='YEARS', blank=True, null=True)  # Field name made lowercase.
    stattime = models.DateTimeField(db_column='STATTIME', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_VACATION'


class SysWorktime(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    settingid = models.BigIntegerField(db_column='SETTINGID', blank=True, null=True)  # Field name made lowercase.
    starttime = models.CharField(db_column='STARTTIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    endtime = models.CharField(db_column='ENDTIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_WORKTIME'


class SysWorktimeSetting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_WORKTIME_SETTING'


class SysWsDataTemplate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=500, blank=True, null=True)  # Field name made lowercase.
    serviceid = models.BigIntegerField(db_column='SERVICEID', blank=True, null=True)  # Field name made lowercase.
    template = models.TextField(db_column='TEMPLATE', blank=True, null=True)  # Field name made lowercase.
    script = models.TextField(db_column='SCRIPT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SYS_WS_DATA_TEMPLATE'


class ApplyCompaign(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    apply_no = models.CharField(max_length=50, blank=True, null=True)
    apply_person = models.CharField(max_length=2000, blank=True, null=True)
    apply_personid = models.CharField(db_column='apply_personID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    apply_date = models.DateTimeField()
    mobile = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    zbbm = models.CharField(max_length=100, blank=True, null=True)
    bmz = models.CharField(max_length=100, blank=True, null=True)
    hdzt = models.CharField(max_length=200, blank=True, null=True)
    hdmd = models.CharField(max_length=2000, blank=True, null=True)
    hdfw = models.CharField(max_length=2000, blank=True, null=True)
    sysh = models.CharField(max_length=2000, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    hdxg = models.CharField(max_length=2000, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    hdnr = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'apply_compaign'


class ApplyForm(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    yxj = models.CharField(max_length=200, blank=True, null=True)
    zmszl = models.CharField(max_length=200, blank=True, null=True)
    zdss = models.CharField(max_length=200, blank=True, null=True)
    dxnd = models.CharField(max_length=200, blank=True, null=True)
    byms = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    fxxwsq = models.DateTimeField()
    zmstcx = models.CharField(max_length=200, blank=True, null=True)
    symd = models.CharField(max_length=200, blank=True, null=True)
    sfff = models.CharField(max_length=200, blank=True, null=True)
    zdsstf = models.CharField(max_length=200, blank=True, null=True)
    bk = models.CharField(max_length=200, blank=True, null=True)
    sqz = models.CharField(max_length=200, blank=True, null=True)
    sqzid = models.CharField(db_column='sqzID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    zdssexcel = models.CharField(db_column='zdssExcel', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'apply_form'


class CompaignDepts(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dept = models.CharField(max_length=2000, blank=True, null=True)
    deptid = models.CharField(db_column='deptID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    xzsm = models.CharField(max_length=200, blank=True, null=True)
    refid = models.ForeignKey(ApplyCompaign, db_column='REFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'compaign_depts'


class CompaignDetail(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    item = models.CharField(max_length=200, blank=True, null=True)
    count = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    amout = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    refid = models.ForeignKey(ApplyCompaign, db_column='REFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'compaign_detail'


class CompanyInfo(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    company_name = models.CharField(max_length=200, blank=True, null=True)
    ceo = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    fax = models.CharField(max_length=100, blank=True, null=True)
    helpdesk_tel = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    staff_count = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_info'


class ContractNotify(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=2000, blank=True, null=True)
    changed = models.CharField(max_length=2000, blank=True, null=True)
    memo = models.CharField(max_length=2000, blank=True, null=True)
    file = models.CharField(max_length=2000, blank=True, null=True)
    changed_flag = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_notify'


class DeviceLendNotify(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    member = models.CharField(max_length=2000, blank=True, null=True)
    memberid = models.CharField(db_column='memberID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    owner = models.CharField(max_length=2000, blank=True, null=True)
    ownerid = models.CharField(db_column='ownerID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    device = models.CharField(max_length=50, blank=True, null=True)
    device_id = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    hurry = models.CharField(max_length=2000, blank=True, null=True)
    reason = models.CharField(max_length=100, blank=True, null=True)
    lent_date = models.DateTimeField()
    return_date = models.DateTimeField()
    end_date = models.DateTimeField()
    content = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_lend_notify'


class EbApplications(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=20, blank=True, null=True)
    first_proposed = models.CharField(max_length=2000, blank=True, null=True)
    intended_use = models.CharField(max_length=2000, blank=True, null=True)
    delivery_method = models.CharField(max_length=20, blank=True, null=True)
    remark = models.CharField(max_length=2000, blank=True, null=True)
    attach_format = models.CharField(max_length=200, blank=True, null=True)
    cert_file = models.CharField(max_length=200, blank=True, null=True)
    doc_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_applications'


class EbAttendance(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    applicant = models.CharField(max_length=100, blank=True, null=True)
    applicantid = models.CharField(db_column='applicantID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    period = models.CharField(max_length=10, blank=True, null=True)
    approver = models.CharField(max_length=100, blank=True, null=True)
    approverid = models.CharField(db_column='approverID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    totaltime = models.CharField(db_column='totalTime', max_length=50, blank=True, null=True)  # Field name made lowercase.
    file = models.CharField(max_length=2000, blank=True, null=True)
    totalday = models.DecimalField(db_column='totalDay', max_digits=2, decimal_places=0)  # Field name made lowercase.
    nightcount = models.DecimalField(db_column='nightCount', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    transit = models.DecimalField(max_digits=13, decimal_places=0)
    transit_interval = models.CharField(max_length=2000)

    class Meta:
        managed = False
        db_table = 'eb_attendance'


class EbBankinfoUpdate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    bank_code = models.CharField(max_length=10, blank=True, null=True)
    branch_code = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    account_number = models.CharField(max_length=10, blank=True, null=True)
    owner_name = models.CharField(max_length=50, blank=True, null=True)
    owner_name_kana = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_bankinfo_update'


class EbCostPayment(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    applicant = models.CharField(max_length=100, blank=True, null=True)
    applicantid = models.CharField(db_column='applicantID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    period = models.CharField(max_length=10, blank=True, null=True)
    approver = models.CharField(max_length=100, blank=True, null=True)
    approverid = models.CharField(db_column='approverID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    totalamount = models.DecimalField(db_column='totalAmount', max_digits=13, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    totalamountinside = models.DecimalField(db_column='totalAmountInside', max_digits=13, decimal_places=0)  # Field name made lowercase.
    totalamountoutside = models.DecimalField(db_column='totalAmountOutside', max_digits=13, decimal_places=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eb_cost_payment'


class EbCostPaymentList(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    day = models.CharField(max_length=10, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    number = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    amount = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    receipt = models.CharField(max_length=10, blank=True, null=True)
    refid = models.ForeignKey(EbCostPayment, db_column='REFID', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'eb_cost_payment_list'


class EbDependment(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=50, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    change_date = models.DateTimeField()
    change_type = models.CharField(max_length=1, blank=True, null=True)
    tax_dependents = models.CharField(max_length=1, blank=True, null=True)
    health_insurance = models.CharField(max_length=1, blank=True, null=True)
    change_reason = models.CharField(max_length=1, blank=True, null=True)
    change_reason_other = models.CharField(max_length=512, blank=True, null=True)
    surname_kanji = models.CharField(max_length=50, blank=True, null=True)
    name_kanji = models.CharField(max_length=50, blank=True, null=True)
    surname_kana = models.CharField(max_length=50, blank=True, null=True)
    name_kana = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateTimeField()
    sex = models.CharField(max_length=1, blank=True, null=True)
    relationship = models.CharField(max_length=2, blank=True, null=True)
    live_division = models.CharField(max_length=1, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=1, blank=True, null=True)
    annual_income_est = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    monthly_payment = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    handicapped = models.CharField(max_length=1, blank=True, null=True)
    employment_insurance = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_dependment'


class EbDevice(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    device_id = models.CharField(max_length=50, blank=True, null=True)
    device_name = models.CharField(max_length=100, blank=True, null=True)
    device_info = models.CharField(max_length=2000, blank=True, null=True)
    device_type = models.CharField(max_length=2000, blank=True, null=True)
    purchase_datetime = models.DateTimeField()
    purchase_price = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    device_sn = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_device'


class EbDeviceLend(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    member = models.CharField(max_length=2000, blank=True, null=True)
    memberid = models.CharField(db_column='memberID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    owner = models.CharField(max_length=2000, blank=True, null=True)
    ownerid = models.CharField(db_column='ownerID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    device = models.CharField(max_length=50, blank=True, null=True)
    device_id = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    lent_date = models.DateTimeField()
    return_date = models.DateTimeField()
    end_date = models.DateTimeField()
    content = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_device_lend'


class EbDeviceSpecs(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    specs_name = models.CharField(max_length=50, blank=True, null=True)
    specs_value = models.CharField(max_length=100, blank=True, null=True)
    refid = models.ForeignKey(EbDevice, db_column='REFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eb_device_specs'


class EbDuringMbCert(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    retire_date = models.DateTimeField(blank=True, null=True)
    cert_file = models.CharField(max_length=500, blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    doc_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_during_mb_cert'


class EbEmpAddrUpdate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    owner = models.CharField(max_length=50, blank=True, null=True)
    relation = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=7, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    addr_thisyear = models.CharField(max_length=100, blank=True, null=True)
    em_contact_addr = models.CharField(max_length=100, blank=True, null=True)
    em_contact_tel = models.CharField(max_length=13, blank=True, null=True)
    em_contact_name = models.CharField(max_length=50, blank=True, null=True)
    private_tel_number = models.CharField(max_length=13, blank=True, null=True)
    business_tel_number = models.CharField(max_length=13, blank=True, null=True)
    private_mail_address = models.CharField(max_length=100, blank=True, null=True)
    business_mail_addres = models.CharField(max_length=100, blank=True, null=True)
    nearby_station = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_emp_addr_update'


class EbEmpContract(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    contract_date = models.DateTimeField(db_column='CONTRACT_DATE')  # Field name made lowercase.
    contract_no = models.CharField(db_column='CONTRACT_NO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    employer_type = models.CharField(db_column='EMPLOYER_TYPE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    employment_date = models.DateTimeField(db_column='EMPLOYMENT_DATE')  # Field name made lowercase.
    employment_period_en = models.DateTimeField(db_column='EMPLOYMENT_PERIOD_EN')  # Field name made lowercase.
    employment_period = models.CharField(db_column='EMPLOYMENT_PERIOD', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    business_addr = models.CharField(db_column='BUSINESS_ADDR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    business_type = models.CharField(db_column='BUSINESS_TYPE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    business_other = models.CharField(db_column='BUSINESS_OTHER', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    business_time = models.CharField(db_column='BUSINESS_TIME', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    allowance_base = models.DecimalField(db_column='ALLOWANCE_BASE', max_digits=13, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    allowance_base_memo = models.CharField(db_column='ALLOWANCE_BASE_MEMO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    pay_site = models.DecimalField(db_column='PAY_SITE', max_digits=13, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pay_site_memo = models.CharField(db_column='PAY_SITE_MEMO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    pay_position = models.DecimalField(db_column='PAY_POSITION', max_digits=13, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pay_position_memo = models.CharField(db_column='PAY_POSITION_MEMO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    pay_duties = models.DecimalField(db_column='PAY_DUTIES', max_digits=13, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pay_duties_memo = models.CharField(db_column='PAY_DUTIES_MEMO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    pay_diligence = models.DecimalField(db_column='PAY_DILIGENCE', max_digits=13, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pay_safety = models.DecimalField(db_column='PAY_SAFETY', max_digits=13, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pay_qual = models.DecimalField(db_column='PAY_QUAL', max_digits=13, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pay_qual_memo = models.CharField(db_column='PAY_QUAL_MEMO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    pay_commute = models.DecimalField(db_column='PAY_COMMUTE', max_digits=13, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pay_commute_memo = models.CharField(db_column='PAY_COMMUTE_MEMO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    pay_overtime = models.CharField(db_column='PAY_OVERTIME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pay_absence = models.CharField(db_column='PAY_ABSENCE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    endowment_insurance = models.CharField(db_column='ENDOWMENT_INSURANCE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    allowance_date = models.CharField(db_column='ALLOWANCE_DATE', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    allowance_change = models.CharField(db_column='ALLOWANCE_CHANGE', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    bonus = models.CharField(db_column='BONUS', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    holiday = models.CharField(db_column='HOLIDAY', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    paid_vacation = models.CharField(db_column='PAID_VACATION', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    not_paid_vacation = models.CharField(db_column='NOT_PAID_VACATION', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    about_discharge = models.CharField(db_column='ABOUT_DISCHARGE', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='MEMO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    cost = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_emp_contract'


class EbEmpEducation(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    start_ym = models.DateTimeField()
    end_ym = models.DateTimeField()
    school = models.CharField(max_length=100, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    undergraduate = models.CharField(max_length=100, blank=True, null=True)
    expert = models.CharField(max_length=100, blank=True, null=True)
    degree = models.CharField(max_length=2000, blank=True, null=True)
    refid = models.ForeignKey('EbEmployee', db_column='REFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eb_emp_education'


class EbEmpLanguage(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=2000, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    refid = models.ForeignKey('EbEmployee', db_column='REFID', blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'eb_emp_language'


class EbEmpPjCareer(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    start_ymd = models.DateTimeField()
    end_ym = models.DateTimeField()
    pj_name = models.CharField(max_length=100, blank=True, null=True)
    pj_overview = models.CharField(max_length=500, blank=True, null=True)
    pj_duty = models.CharField(max_length=500, blank=True, null=True)
    pj_platform = models.CharField(max_length=200, blank=True, null=True)
    pj_platformid = models.CharField(db_column='pj_platformID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    pj_framework = models.CharField(max_length=200, blank=True, null=True)
    pj_frameworkid = models.CharField(db_column='pj_frameworkID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    pj_language = models.CharField(max_length=200, blank=True, null=True)
    pj_languageid = models.CharField(db_column='pj_languageID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    pj_middleware = models.CharField(max_length=200, blank=True, null=True)
    pj_middlewareid = models.CharField(db_column='pj_middlewareID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    refid = models.ForeignKey('EbEmployee', db_column='REFID', blank=True, null=True)  # Field name made lowercase.
    pj_database = models.CharField(max_length=20, blank=True, null=True)
    pj_databaseid = models.CharField(db_column='pj_databaseID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pj_scope_ut = models.CharField(max_length=20, blank=True, null=True)
    pj_scope_post = models.CharField(max_length=20, blank=True, null=True)
    pj_role = models.CharField(max_length=20, blank=True, null=True)
    jp_scope_si = models.CharField(max_length=20, blank=True, null=True)
    jp_scope_st = models.CharField(max_length=20, blank=True, null=True)
    pj_scope_st = models.CharField(max_length=20, blank=True, null=True)
    pj_scope_pg = models.CharField(max_length=20, blank=True, null=True)
    pj_scope_ra = models.CharField(max_length=20, blank=True, null=True)
    pj_scope_rd = models.CharField(max_length=20, blank=True, null=True)
    pj_scope_bd = models.CharField(max_length=20, blank=True, null=True)
    pj_scope_dd = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_emp_pj_career'


class EbEmpQulification(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    get_date = models.DateTimeField()
    remark = models.CharField(max_length=2000, blank=True, null=True)
    refid = models.ForeignKey('EbEmployee', db_column='REFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eb_emp_qulification'


class EbEmployee(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    residence_name = models.CharField(max_length=50, blank=True, null=True)
    residence_name_kana = models.CharField(max_length=100, blank=True, null=True)
    passport_name = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateTimeField()
    sex = models.CharField(max_length=200, blank=True, null=True)
    marriage = models.CharField(max_length=200, blank=True, null=True)
    address_flag = models.CharField(max_length=1, blank=True, null=True)
    nationality = models.CharField(max_length=200, blank=True, null=True)
    family_owner = models.CharField(max_length=100, blank=True, null=True)
    relation = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    address_now = models.CharField(max_length=2000, blank=True, null=True)
    emergency_address = models.CharField(max_length=2000, blank=True, null=True)
    emergency_tel = models.CharField(max_length=100, blank=True, null=True)
    born_location = models.CharField(max_length=50, blank=True, null=True)
    private_tel_number = models.CharField(max_length=100, blank=True, null=True)
    station = models.CharField(max_length=50, blank=True, null=True)
    private_mail_address = models.CharField(max_length=100, blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expired_dt = models.DateTimeField(blank=True, null=True)
    immigration_date = models.DateTimeField(blank=True, null=True)
    id_photo = models.CharField(max_length=2000, blank=True, null=True)
    join_date = models.DateTimeField()
    business_mail_addr = models.CharField(max_length=100, blank=True, null=True)
    employment_type = models.CharField(max_length=100, blank=True, null=True)
    id_number = models.CharField(max_length=50, blank=True, null=True)
    id_card_expired_date = models.DateTimeField()
    residence_type = models.CharField(max_length=100, blank=True, null=True)
    account_id = models.CharField(max_length=50)
    contract_file = models.CharField(max_length=2000, blank=True, null=True)
    security_file = models.CharField(max_length=2000, blank=True, null=True)
    personal_info_file = models.CharField(max_length=2000, blank=True, null=True)
    user_id = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    titleid = models.CharField(max_length=50, blank=True, null=True)
    employee_agreement = models.CharField(max_length=2000, blank=True, null=True)
    blood_type = models.CharField(max_length=2, blank=True, null=True)
    business_tel_number = models.CharField(max_length=13, blank=True, null=True)
    pay_bank = models.CharField(max_length=10, blank=True, null=True)
    pay_branch = models.CharField(max_length=10, blank=True, null=True)
    pay_account = models.CharField(max_length=100, blank=True, null=True)
    pay_owner = models.CharField(max_length=50, blank=True, null=True)
    pay_owner_kana = models.CharField(max_length=50, blank=True, null=True)
    retire_date = models.DateTimeField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=2000, blank=True, null=True)
    emp_insurance_no = models.CharField(max_length=20, blank=True, null=True)
    emp_welfare_num = models.CharField(max_length=20, blank=True, null=True)
    retire_pref_date = models.CharField(max_length=50, blank=True, null=True)
    retire_reason = models.CharField(max_length=1000, blank=True, null=True)
    eb_motherland = models.CharField(max_length=10, blank=True, null=True)
    eb_motherland_addr = models.CharField(max_length=100, blank=True, null=True)
    eb_motherland_ctct = models.CharField(max_length=20, blank=True, null=True)
    contractid = models.CharField(db_column='contractID', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eb_employee'


class EbInsureLossCert(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateTimeField()
    retire_date = models.DateTimeField()
    get_date = models.DateTimeField()
    loss_date = models.DateTimeField()
    ins_name = models.CharField(max_length=50, blank=True, null=True)
    ins_number = models.CharField(max_length=50, blank=True, null=True)
    symbol = models.CharField(max_length=50, blank=True, null=True)
    pension_number = models.CharField(max_length=50, blank=True, null=True)
    cert_file = models.CharField(max_length=2000, blank=True, null=True)
    cert_number = models.CharField(max_length=100, blank=True, null=True)
    doc_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_insure_loss_cert'


class EbMRoomDevice(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    device_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    refid = models.ForeignKey('EbMeetingRoom', db_column='REFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eb_m_room_device'


class EbMarriageContact(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(max_length=2000, blank=True, null=True)
    reason_other = models.CharField(max_length=512, blank=True, null=True)
    marriage_date = models.DateTimeField()
    spouse_name = models.CharField(max_length=100, blank=True, null=True)
    attach_file_01 = models.CharField(max_length=2000, blank=True, null=True)
    attach_file_02 = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_marriage_contact'


class EbMeeting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    owner = models.CharField(max_length=2000, blank=True, null=True)
    ownerid = models.CharField(db_column='ownerID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=50, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    content = models.CharField(max_length=2000, blank=True, null=True)
    result = models.CharField(max_length=2000, blank=True, null=True)
    member = models.CharField(max_length=2000)
    memberid = models.CharField(db_column='memberID', max_length=2000)  # Field name made lowercase.
    writer = models.CharField(max_length=2000, blank=True, null=True)
    writerid = models.CharField(db_column='writerID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    room_id = models.CharField(max_length=50, blank=True, null=True)
    room = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_meeting'


class EbMeetingRoom(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    room_id = models.CharField(max_length=50, blank=True, null=True)
    room_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_meeting_room'


class EbNotice(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=100, blank=True, null=True)
    publish_date = models.DateTimeField()
    detail = models.CharField(max_length=2000, blank=True, null=True)
    attach_file01 = models.CharField(max_length=2000, blank=True, null=True)
    attach_file02 = models.CharField(max_length=2000, blank=True, null=True)
    attach_file03 = models.CharField(max_length=2000, blank=True, null=True)
    attach_file04 = models.CharField(max_length=2000, blank=True, null=True)
    summary = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_notice'


class EbResume(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=100, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    name_kata = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateTimeField()
    sex = models.CharField(max_length=2, blank=True, null=True)
    visa_date = models.DateTimeField()
    nearby_station = models.CharField(max_length=50, blank=True, null=True)
    last_update = models.DateTimeField()
    stay_year = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    age = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    flg = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    file_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_resume'


class EbResumeEducation(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=100, blank=True, null=True)
    start_ym = models.DateTimeField()
    end_ym = models.DateTimeField()
    school = models.CharField(max_length=100, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    undergraduate = models.CharField(max_length=100, blank=True, null=True)
    expert = models.CharField(max_length=100, blank=True, null=True)
    degree = models.CharField(max_length=10, blank=True, null=True)
    refid = models.ForeignKey(EbResume, db_column='REFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eb_resume_education'


class EbResumeLanguage(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    level = models.CharField(max_length=100, blank=True, null=True)
    refid = models.ForeignKey(EbResume, db_column='REFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eb_resume_language'


class EbResumePjCareer(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=100, blank=True, null=True)
    no = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    start_ymd = models.DateTimeField()
    end_ymd = models.DateTimeField()
    pj_overview = models.CharField(max_length=100, blank=True, null=True)
    pj_duty = models.CharField(max_length=100, blank=True, null=True)
    pj_platform = models.CharField(max_length=20, blank=True, null=True)
    pj_platformid = models.CharField(db_column='pj_platformID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pj_language = models.CharField(max_length=20, blank=True, null=True)
    pj_languageid = models.CharField(db_column='pj_languageID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pj_middleware = models.CharField(max_length=20, blank=True, null=True)
    pj_middlewareid = models.CharField(db_column='pj_middlewareID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pj_database = models.CharField(max_length=20, blank=True, null=True)
    pj_databaseid = models.CharField(db_column='pj_databaseID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pj_role = models.CharField(max_length=20, blank=True, null=True)
    pj_scope_rd = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_bd = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_dd = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_pg = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_ut = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_si = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_st = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_mt = models.CharField(max_length=1, blank=True, null=True)
    refid = models.ForeignKey(EbResume, db_column='REFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eb_resume_pj_career'


class EbResumeQualificat(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    get_date = models.DateTimeField()
    remark = models.CharField(max_length=100, blank=True, null=True)
    refid = models.ForeignKey(EbResume, db_column='REFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eb_resume_qualificat'


class EbRetireCert(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=10, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    work_type = models.CharField(max_length=50, blank=True, null=True)
    tile = models.CharField(max_length=100, blank=True, null=True)
    pay = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    reson = models.CharField(max_length=2, blank=True, null=True)
    comment = models.CharField(max_length=512, blank=True, null=True)
    others = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateTimeField()
    retire_day = models.CharField(max_length=50, blank=True, null=True)
    end_date = models.DateTimeField()
    name = models.CharField(max_length=50, blank=True, null=True)
    cert_file = models.CharField(max_length=2000, blank=True, null=True)
    doc_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_retire_cert'


class EbRetirement(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    retire_day = models.DateTimeField()
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    tel = models.CharField(max_length=13, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    health_insurance = models.CharField(max_length=512, blank=True, null=True)
    employment_insurance = models.CharField(max_length=512, blank=True, null=True)
    pension = models.CharField(max_length=512, blank=True, null=True)
    resident_tax = models.CharField(max_length=512, blank=True, null=True)
    income_tax = models.CharField(max_length=512, blank=True, null=True)
    certification = models.CharField(max_length=512, blank=True, null=True)
    attach_file_01 = models.CharField(max_length=512, blank=True, null=True)
    attach_file_02 = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_retirement'


class EbTransit(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    apply_no = models.CharField(max_length=10, blank=True, null=True)
    code = models.CharField(max_length=6, blank=True, null=True)
    start_ym = models.CharField(max_length=100, blank=True, null=True)
    spend_min = models.CharField(max_length=3, blank=True, null=True)
    start_station = models.CharField(max_length=10, blank=True, null=True)
    attachment01 = models.CharField(max_length=256, blank=True, null=True)
    attachment02 = models.CharField(max_length=256, blank=True, null=True)
    attachment03 = models.CharField(max_length=256, blank=True, null=True)
    attachment04 = models.CharField(max_length=256, blank=True, null=True)
    attachment05 = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=2000, blank=True, null=True)
    nameid = models.CharField(db_column='nameID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    start_ymd = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=5, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'eb_transit'


class EbTransitInterval(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    apply_no = models.CharField(max_length=10, blank=True, null=True)
    idx_no = models.CharField(max_length=100, blank=True, null=True)
    provider = models.CharField(max_length=50, blank=True, null=True)
    start_station = models.CharField(max_length=50, blank=True, null=True)
    arrive_station = models.CharField(max_length=50, blank=True, null=True)
    via_station = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    refid = models.ForeignKey(EbTransit, db_column='REFID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eb_transit_interval'


class EbVisaApplicaton(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    attach_file = models.CharField(max_length=2000, blank=True, null=True)
    expect_date = models.DateTimeField()
    delivery_method = models.CharField(max_length=30, blank=True, null=True)
    remark = models.CharField(max_length=2000, blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    company_doc = models.CharField(max_length=2000, blank=True, null=True)
    doc_number = models.CharField(max_length=20, blank=True, null=True)
    flg = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_visa_applicaton'


class EbVisaContact(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    visa_start_date = models.DateTimeField()
    visa_expire_date = models.DateTimeField()
    residence_dl = models.DateTimeField()
    visa_type = models.CharField(max_length=50, blank=True, null=True)
    attach_file = models.CharField(max_length=2000, blank=True, null=True)
    remark = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_visa_contact'


class NameChangeNotify(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    change_date = models.DateTimeField()
    reason = models.CharField(max_length=2000, blank=True, null=True)
    reason_other = models.CharField(max_length=512, blank=True, null=True)
    new_name = models.CharField(max_length=100, blank=True, null=True)
    new_name_furigana = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'name_change_notify'


class RecruitManagement(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    initial = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    test_rank = models.CharField(max_length=2000, blank=True, null=True)
    apply_date = models.DateTimeField()
    interview_date = models.DateTimeField()
    offersend_date = models.DateTimeField()
    offerarrive_date = models.DateTimeField()
    doc_create_date = models.DateTimeField()
    visa_app_date = models.DateTimeField()
    visa_get_date = models.DateTimeField()
    visa_ems_date = models.DateTimeField()
    checkin_date = models.DateTimeField()
    join_date = models.DateTimeField()
    contract_date = models.DateTimeField()
    new_training_date = models.DateTimeField()
    eb_resume_date = models.DateTimeField(db_column='EB_resume_date')  # Field name made lowercase.
    sales_date = models.DateTimeField()
    entry_date = models.DateTimeField()
    selink_date = models.DateTimeField()
    attatch_file = models.CharField(max_length=2000, blank=True, null=True)
    referee = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    interviewer = models.CharField(max_length=100, blank=True, null=True)
    con_tel = models.CharField(max_length=100, blank=True, null=True)
    con_mail = models.CharField(max_length=50, blank=True, null=True)
    im = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=2000, blank=True, null=True)
    base_salary = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    bonus = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    trans_cost = models.CharField(max_length=2000, blank=True, null=True)
    others_salary = models.CharField(max_length=50, blank=True, null=True)
    contract_type = models.CharField(max_length=2000, blank=True, null=True)
    trial_period = models.CharField(max_length=2000, blank=True, null=True)
    trial_end_date = models.DateTimeField()
    attach_file = models.CharField(max_length=20, blank=True, null=True)
    job_type = models.CharField(max_length=20, blank=True, null=True)
    result = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recruit_management'


class SchemaVersion(models.Model):
    version_rank = models.IntegerField()
    installed_rank = models.IntegerField()
    version = models.CharField(primary_key=True, max_length=50)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    script = models.CharField(max_length=1000)
    checksum = models.IntegerField(blank=True, null=True)
    installed_by = models.CharField(max_length=100)
    installed_on = models.DateTimeField()
    execution_time = models.IntegerField()
    success = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'schema_version'


class Test001(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    test = models.CharField(max_length=50, blank=True, null=True)
    file1 = models.CharField(max_length=200, blank=True, null=True)
    file2 = models.CharField(max_length=200, blank=True, null=True)
    remarks = models.CharField(max_length=100, blank=True, null=True)
    xxxx = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test001'
