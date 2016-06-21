# coding: UTF-8

from django.db import models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from eb import models as eb_models


class EboaManager(models.Manager):
    def get_queryset(self):
        return super(EboaManager, self).get_queryset().using("bpm_eboa")


class ActEvtLog(models.Model):
    log_nr_field = models.BigIntegerField(db_column='LOG_NR_', primary_key=True)  
    type_field = models.CharField(db_column='TYPE_', max_length=64, blank=True, null=True)  
    proc_def_id_field = models.CharField(db_column='PROC_DEF_ID_', max_length=64, blank=True, null=True)  
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  
    execution_id_field = models.CharField(db_column='EXECUTION_ID_', max_length=64, blank=True, null=True)  
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  
    time_stamp_field = models.DateTimeField(db_column='TIME_STAMP_')  
    user_id_field = models.CharField(db_column='USER_ID_', max_length=255, blank=True, null=True)  
    data_field = models.TextField(db_column='DATA_', blank=True, null=True)  
    lock_owner_field = models.CharField(db_column='LOCK_OWNER_', max_length=255, blank=True, null=True)  
    lock_time_field = models.DateTimeField(db_column='LOCK_TIME_', blank=True, null=True)  
    is_processed_field = models.IntegerField(db_column='IS_PROCESSED_', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_EVT_LOG'


class ActGeBytearray(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  
    deployment_id_field = models.ForeignKey('ActReDeployment', db_column='DEPLOYMENT_ID_', blank=True, null=True)  
    bytes_field = models.TextField(db_column='BYTES_', blank=True, null=True)  
    generated_field = models.IntegerField(db_column='GENERATED_', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_GE_BYTEARRAY'


class ActGeProperty(models.Model):
    name_field = models.CharField(db_column='NAME_', primary_key=True, max_length=64)  
    value_field = models.CharField(db_column='VALUE_', max_length=300, blank=True, null=True)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_GE_PROPERTY'


class ActHiActinst(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  
    proc_def_id_field = models.CharField(db_column='PROC_DEF_ID_', max_length=64)  
    proc_inst_id_field = models.BigIntegerField(db_column='PROC_INST_ID_', blank=True, null=True)  
    execution_id_field = models.BigIntegerField(db_column='EXECUTION_ID_', blank=True, null=True)  
    act_id_field = models.CharField(db_column='ACT_ID_', max_length=255)  
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  
    call_proc_inst_id_field = models.CharField(db_column='CALL_PROC_INST_ID_', max_length=64, blank=True, null=True)  
    act_name_field = models.CharField(db_column='ACT_NAME_', max_length=255, blank=True, null=True)  
    act_type_field = models.CharField(db_column='ACT_TYPE_', max_length=255)  
    assignee_field = models.BigIntegerField(db_column='ASSIGNEE_', blank=True, null=True)  
    start_time_field = models.DateTimeField(db_column='START_TIME_')  
    end_time_field = models.DateTimeField(db_column='END_TIME_', blank=True, null=True)  
    isstart = models.IntegerField(db_column='ISSTART', blank=True, null=True)  
    duration_field = models.BigIntegerField(db_column='DURATION_', blank=True, null=True)  
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_HI_ACTINST'


class ActHiAttachment(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    user_id_field = models.CharField(db_column='USER_ID_', max_length=255, blank=True, null=True)  
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  
    description_field = models.CharField(db_column='DESCRIPTION_', max_length=4000, blank=True, null=True)  
    type_field = models.CharField(db_column='TYPE_', max_length=255, blank=True, null=True)  
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  
    url_field = models.CharField(db_column='URL_', max_length=4000, blank=True, null=True)  
    content_id_field = models.CharField(db_column='CONTENT_ID_', max_length=64, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_HI_ATTACHMENT'


class ActHiComment(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    type_field = models.CharField(db_column='TYPE_', max_length=255, blank=True, null=True)  
    time_field = models.DateTimeField(db_column='TIME_')  
    user_id_field = models.CharField(db_column='USER_ID_', max_length=255, blank=True, null=True)  
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  
    action_field = models.CharField(db_column='ACTION_', max_length=255, blank=True, null=True)  
    message_field = models.CharField(db_column='MESSAGE_', max_length=4000, blank=True, null=True)  
    full_msg_field = models.TextField(db_column='FULL_MSG_', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_HI_COMMENT'


class ActHiDetail(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    type_field = models.CharField(db_column='TYPE_', max_length=255)  
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  
    execution_id_field = models.CharField(db_column='EXECUTION_ID_', max_length=64, blank=True, null=True)  
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  
    act_inst_id_field = models.CharField(db_column='ACT_INST_ID_', max_length=64, blank=True, null=True)  
    name_field = models.CharField(db_column='NAME_', max_length=255)  
    var_type_field = models.CharField(db_column='VAR_TYPE_', max_length=255, blank=True, null=True)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    time_field = models.DateTimeField(db_column='TIME_')  
    bytearray_id_field = models.CharField(db_column='BYTEARRAY_ID_', max_length=64, blank=True, null=True)  
    double_field = models.FloatField(db_column='DOUBLE_', blank=True, null=True)  
    long_field = models.BigIntegerField(db_column='LONG_', blank=True, null=True)  
    text_field = models.CharField(db_column='TEXT_', max_length=4000, blank=True, null=True)  
    text2_field = models.CharField(db_column='TEXT2_', max_length=4000, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_HI_DETAIL'


class ActHiIdentitylink(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    group_id_field = models.CharField(db_column='GROUP_ID_', max_length=255, blank=True, null=True)  
    type_field = models.CharField(db_column='TYPE_', max_length=255, blank=True, null=True)  
    user_id_field = models.CharField(db_column='USER_ID_', max_length=255, blank=True, null=True)  
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_HI_IDENTITYLINK'


class ActHiProcinst(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  
    proc_inst_id_field = models.BigIntegerField(db_column='PROC_INST_ID_', unique=True, blank=True, null=True)  
    business_key_field = models.CharField(db_column='BUSINESS_KEY_', max_length=255, blank=True, null=True)  
    proc_def_id_field = models.CharField(db_column='PROC_DEF_ID_', max_length=64)  
    start_time_field = models.DateTimeField(db_column='START_TIME_')  
    end_time_field = models.DateTimeField(db_column='END_TIME_', blank=True, null=True)  
    duration_field = models.BigIntegerField(db_column='DURATION_', blank=True, null=True)  
    start_user_id_field = models.BigIntegerField(db_column='START_USER_ID_', blank=True, null=True)  
    start_act_id_field = models.CharField(db_column='START_ACT_ID_', max_length=255, blank=True, null=True)  
    end_act_id_field = models.CharField(db_column='END_ACT_ID_', max_length=255, blank=True, null=True)  
    super_process_instance_id_field = models.BigIntegerField(db_column='SUPER_PROCESS_INSTANCE_ID_', blank=True, null=True)  
    delete_reason_field = models.CharField(db_column='DELETE_REASON_', max_length=4000, blank=True, null=True)  
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_HI_PROCINST'


class ActHiTaskinst(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  
    proc_def_id_field = models.CharField(db_column='PROC_DEF_ID_', max_length=64, blank=True, null=True)  
    task_def_key_field = models.CharField(db_column='TASK_DEF_KEY_', max_length=255, blank=True, null=True)  
    proc_inst_id_field = models.BigIntegerField(db_column='PROC_INST_ID_', blank=True, null=True)  
    execution_id_field = models.BigIntegerField(db_column='EXECUTION_ID_', blank=True, null=True)  
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  
    parent_task_id_field = models.BigIntegerField(db_column='PARENT_TASK_ID_', blank=True, null=True)  
    description_field = models.CharField(db_column='DESCRIPTION_', max_length=4000, blank=True, null=True)  
    owner_field = models.BigIntegerField(db_column='OWNER_', blank=True, null=True)  
    assignee_field = models.BigIntegerField(db_column='ASSIGNEE_', blank=True, null=True)  
    start_time_field = models.DateTimeField(db_column='START_TIME_')  
    claim_time_field = models.DateTimeField(db_column='CLAIM_TIME_', blank=True, null=True)  
    end_time_field = models.DateTimeField(db_column='END_TIME_', blank=True, null=True)  
    duration_field = models.BigIntegerField(db_column='DURATION_', blank=True, null=True)  
    delete_reason_field = models.CharField(db_column='DELETE_REASON_', max_length=4000, blank=True, null=True)  
    priority_field = models.IntegerField(db_column='PRIORITY_', blank=True, null=True)  
    due_date_field = models.DateTimeField(db_column='DUE_DATE_', blank=True, null=True)  
    form_key_field = models.CharField(db_column='FORM_KEY_', max_length=255, blank=True, null=True)  
    category_field = models.CharField(db_column='CATEGORY_', max_length=255, blank=True, null=True)  
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_HI_TASKINST'


class ActHiVarinst(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  
    execution_id_field = models.CharField(db_column='EXECUTION_ID_', max_length=64, blank=True, null=True)  
    task_id_field = models.CharField(db_column='TASK_ID_', max_length=64, blank=True, null=True)  
    name_field = models.CharField(db_column='NAME_', max_length=255)  
    var_type_field = models.CharField(db_column='VAR_TYPE_', max_length=100, blank=True, null=True)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    bytearray_id_field = models.CharField(db_column='BYTEARRAY_ID_', max_length=64, blank=True, null=True)  
    double_field = models.FloatField(db_column='DOUBLE_', blank=True, null=True)  
    long_field = models.BigIntegerField(db_column='LONG_', blank=True, null=True)  
    text_field = models.CharField(db_column='TEXT_', max_length=4000, blank=True, null=True)  
    text2_field = models.CharField(db_column='TEXT2_', max_length=4000, blank=True, null=True)  
    create_time_field = models.DateTimeField(db_column='CREATE_TIME_', blank=True, null=True)  
    last_updated_time_field = models.DateTimeField(db_column='LAST_UPDATED_TIME_', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_HI_VARINST'


class ActIdGroup(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  
    type_field = models.CharField(db_column='TYPE_', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_ID_GROUP'


class ActIdInfo(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    user_id_field = models.CharField(db_column='USER_ID_', max_length=64, blank=True, null=True)  
    type_field = models.CharField(db_column='TYPE_', max_length=64, blank=True, null=True)  
    key_field = models.CharField(db_column='KEY_', max_length=255, blank=True, null=True)  
    value_field = models.CharField(db_column='VALUE_', max_length=255, blank=True, null=True)  
    password_field = models.TextField(db_column='PASSWORD_', blank=True, null=True)  
    parent_id_field = models.CharField(db_column='PARENT_ID_', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_ID_INFO'


class ActIdMembership(models.Model):
    user_id_field = models.ForeignKey('ActIdUser', db_column='USER_ID_')  
    group_id_field = models.ForeignKey(ActIdGroup, db_column='GROUP_ID_')  

    class Meta:
        managed = False
        db_table = 'ACT_ID_MEMBERSHIP'
        unique_together = (('user_id_field', 'group_id_field'),)


class ActIdUser(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    first_field = models.CharField(db_column='FIRST_', max_length=255, blank=True, null=True)  
    last_field = models.CharField(db_column='LAST_', max_length=255, blank=True, null=True)  
    email_field = models.CharField(db_column='EMAIL_', max_length=255, blank=True, null=True)  
    pwd_field = models.CharField(db_column='PWD_', max_length=255, blank=True, null=True)  
    picture_id_field = models.CharField(db_column='PICTURE_ID_', max_length=64, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_ID_USER'


class ActReDeployment(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  
    category_field = models.CharField(db_column='CATEGORY_', max_length=255, blank=True, null=True)  
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  
    deploy_time_field = models.DateTimeField(db_column='DEPLOY_TIME_')  

    class Meta:
        managed = False
        db_table = 'ACT_RE_DEPLOYMENT'


class ActReModel(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  
    key_field = models.CharField(db_column='KEY_', max_length=255, blank=True, null=True)  
    category_field = models.CharField(db_column='CATEGORY_', max_length=255, blank=True, null=True)  
    create_time_field = models.DateTimeField(db_column='CREATE_TIME_', blank=True, null=True)  
    last_update_time_field = models.DateTimeField(db_column='LAST_UPDATE_TIME_', blank=True, null=True)  
    version_field = models.IntegerField(db_column='VERSION_', blank=True, null=True)  
    meta_info_field = models.CharField(db_column='META_INFO_', max_length=4000, blank=True, null=True)  
    deployment_id_field = models.ForeignKey(ActReDeployment, db_column='DEPLOYMENT_ID_', blank=True, null=True)  
    editor_source_value_id_field = models.CharField(db_column='EDITOR_SOURCE_VALUE_ID_', max_length=64, blank=True, null=True)  
    editor_source_extra_value_id_field = models.CharField(db_column='EDITOR_SOURCE_EXTRA_VALUE_ID_', max_length=64, blank=True, null=True)  
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_RE_MODEL'


class ActReProcdef(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    category_field = models.CharField(db_column='CATEGORY_', max_length=255, blank=True, null=True)  
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  
    key_field = models.CharField(db_column='KEY_', max_length=255)  
    version_field = models.IntegerField(db_column='VERSION_')  
    deployment_id_field = models.BigIntegerField(db_column='DEPLOYMENT_ID_', blank=True, null=True)  
    resource_name_field = models.CharField(db_column='RESOURCE_NAME_', max_length=4000, blank=True, null=True)  
    dgrm_resource_name_field = models.CharField(db_column='DGRM_RESOURCE_NAME_', max_length=4000, blank=True, null=True)  
    description_field = models.CharField(db_column='DESCRIPTION_', max_length=4000, blank=True, null=True)  
    has_start_form_key_field = models.IntegerField(db_column='HAS_START_FORM_KEY_', blank=True, null=True)  
    suspension_state_field = models.IntegerField(db_column='SUSPENSION_STATE_', blank=True, null=True)  
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_RE_PROCDEF'
        unique_together = (('key_field', 'version_field', 'tenant_id_field'),)


class ActRuEventSubscr(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    event_type_field = models.CharField(db_column='EVENT_TYPE_', max_length=255)  
    event_name_field = models.CharField(db_column='EVENT_NAME_', max_length=255, blank=True, null=True)  
    execution_id_field = models.ForeignKey('ActRuExecution', db_column='EXECUTION_ID_', blank=True, null=True)  
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  
    activity_id_field = models.CharField(db_column='ACTIVITY_ID_', max_length=64, blank=True, null=True)  
    configuration_field = models.CharField(db_column='CONFIGURATION_', max_length=255, blank=True, null=True)  
    created_field = models.DateTimeField(db_column='CREATED_')  
    proc_def_id_field = models.CharField(db_column='PROC_DEF_ID_', max_length=64, blank=True, null=True)  
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_RU_EVENT_SUBSCR'


class ActRuExecution(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    proc_inst_id_field = models.ForeignKey('self', related_name='proc_inst_id_set', db_column='PROC_INST_ID_', blank=True, null=True)
    business_key_field = models.CharField(db_column='BUSINESS_KEY_', max_length=255, blank=True, null=True)  
    parent_id_field = models.ForeignKey('self', related_name='parent_id_set', db_column='PARENT_ID_', blank=True, null=True)
    proc_def_id_field = models.ForeignKey(ActReProcdef, db_column='PROC_DEF_ID_', blank=True, null=True)  
    super_exec_field = models.ForeignKey('self', related_name='super_exec_set', db_column='SUPER_EXEC_', blank=True, null=True)
    act_id_field = models.CharField(db_column='ACT_ID_', max_length=255, blank=True, null=True)  
    is_active_field = models.IntegerField(db_column='IS_ACTIVE_', blank=True, null=True)  
    is_concurrent_field = models.IntegerField(db_column='IS_CONCURRENT_', blank=True, null=True)  
    is_scope_field = models.IntegerField(db_column='IS_SCOPE_', blank=True, null=True)  
    is_event_scope_field = models.IntegerField(db_column='IS_EVENT_SCOPE_', blank=True, null=True)  
    suspension_state_field = models.IntegerField(db_column='SUSPENSION_STATE_', blank=True, null=True)  
    cached_ent_state_field = models.IntegerField(db_column='CACHED_ENT_STATE_', blank=True, null=True)  
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_RU_EXECUTION'


class ActRuIdentitylink(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    group_id_field = models.BigIntegerField(db_column='GROUP_ID_', blank=True, null=True)  
    type_field = models.CharField(db_column='TYPE_', max_length=255, blank=True, null=True)  
    user_id_field = models.BigIntegerField(db_column='USER_ID_', blank=True, null=True)  
    task_id_field = models.ForeignKey('ActRuTask', db_column='TASK_ID_', blank=True, null=True)  
    proc_inst_id_field = models.CharField(db_column='PROC_INST_ID_', max_length=64, blank=True, null=True)  
    proc_def_id_field = models.ForeignKey(ActReProcdef, db_column='PROC_DEF_ID_', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_RU_IDENTITYLINK'


class ActRuJob(models.Model):
    id_field = models.CharField(db_column='ID_', primary_key=True, max_length=64)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    type_field = models.CharField(db_column='TYPE_', max_length=255)  
    lock_exp_time_field = models.DateTimeField(db_column='LOCK_EXP_TIME_', blank=True, null=True)  
    lock_owner_field = models.CharField(db_column='LOCK_OWNER_', max_length=255, blank=True, null=True)  
    exclusive_field = models.IntegerField(db_column='EXCLUSIVE_', blank=True, null=True)  
    execution_id_field = models.CharField(db_column='EXECUTION_ID_', max_length=64, blank=True, null=True)  
    process_instance_id_field = models.CharField(db_column='PROCESS_INSTANCE_ID_', max_length=64, blank=True, null=True)  
    proc_def_id_field = models.CharField(db_column='PROC_DEF_ID_', max_length=64, blank=True, null=True)  
    retries_field = models.IntegerField(db_column='RETRIES_', blank=True, null=True)  
    exception_stack_id_field = models.ForeignKey(ActGeBytearray, db_column='EXCEPTION_STACK_ID_', blank=True, null=True)  
    exception_msg_field = models.CharField(db_column='EXCEPTION_MSG_', max_length=4000, blank=True, null=True)  
    duedate_field = models.DateTimeField(db_column='DUEDATE_', blank=True, null=True)  
    repeat_field = models.CharField(db_column='REPEAT_', max_length=255, blank=True, null=True)  
    handler_type_field = models.CharField(db_column='HANDLER_TYPE_', max_length=255, blank=True, null=True)  
    handler_cfg_field = models.CharField(db_column='HANDLER_CFG_', max_length=4000, blank=True, null=True)  
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_RU_JOB'


class ActRuTask(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    execution_id_field = models.ForeignKey(ActRuExecution, related_name='actrutask_execution_id_set', db_column='EXECUTION_ID_', blank=True, null=True)
    proc_inst_id_field = models.ForeignKey(ActRuExecution, related_name='actrutask_proc_inst_id_set', db_column='PROC_INST_ID_', blank=True, null=True)
    proc_def_id_field = models.ForeignKey(ActReProcdef, db_column='PROC_DEF_ID_', blank=True, null=True)  
    name_field = models.CharField(db_column='NAME_', max_length=255, blank=True, null=True)  
    parent_task_id_field = models.BigIntegerField(db_column='PARENT_TASK_ID_', blank=True, null=True)  
    description_field = models.CharField(db_column='DESCRIPTION_', max_length=4000, blank=True, null=True)  
    task_def_key_field = models.CharField(db_column='TASK_DEF_KEY_', max_length=255, blank=True, null=True)  
    owner_field = models.BigIntegerField(db_column='OWNER_', blank=True, null=True)  
    assignee_field = models.BigIntegerField(db_column='ASSIGNEE_', blank=True, null=True)  
    delegation_field = models.CharField(db_column='DELEGATION_', max_length=64, blank=True, null=True)  
    priority_field = models.IntegerField(db_column='PRIORITY_', blank=True, null=True)  
    create_time_field = models.DateTimeField(db_column='CREATE_TIME_')  
    due_date_field = models.DateTimeField(db_column='DUE_DATE_', blank=True, null=True)  
    category_field = models.CharField(db_column='CATEGORY_', max_length=255, blank=True, null=True)  
    suspension_state_field = models.IntegerField(db_column='SUSPENSION_STATE_', blank=True, null=True)  
    tenant_id_field = models.CharField(db_column='TENANT_ID_', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_RU_TASK'


class ActRuVariable(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  
    rev_field = models.IntegerField(db_column='REV_', blank=True, null=True)  
    type_field = models.CharField(db_column='TYPE_', max_length=255)  
    name_field = models.CharField(db_column='NAME_', max_length=255)  
    execution_id_field = models.ForeignKey(ActRuExecution, related_name='actruvariable_execution_id_set', db_column='EXECUTION_ID_', blank=True, null=True)
    proc_inst_id_field = models.ForeignKey(ActRuExecution, related_name='actruvariable_proc_inst_id_set', db_column='PROC_INST_ID_', blank=True, null=True)
    task_id_field = models.BigIntegerField(db_column='TASK_ID_', blank=True, null=True)  
    bytearray_id_field = models.ForeignKey(ActGeBytearray, db_column='BYTEARRAY_ID_', blank=True, null=True)  
    double_field = models.FloatField(db_column='DOUBLE_', blank=True, null=True)  
    long_field = models.BigIntegerField(db_column='LONG_', blank=True, null=True)  
    text_field = models.CharField(db_column='TEXT_', max_length=4000, blank=True, null=True)  
    text2_field = models.CharField(db_column='TEXT2_', max_length=4000, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ACT_RU_VARIABLE'


class BpmAgentCondition(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    settingid = models.BigIntegerField(db_column='SETTINGID', blank=True, null=True)  
    con = models.CharField(db_column='CON', max_length=1000, blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  
    agentid = models.BigIntegerField(db_column='AGENTID', blank=True, null=True)  
    agent = models.CharField(db_column='AGENT', max_length=100, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_AGENT_CONDITION'


class BpmAgentDef(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    settingid = models.BigIntegerField(db_column='SETTINGID', blank=True, null=True)  
    flowkey = models.CharField(db_column='FLOWKEY', max_length=50, blank=True, null=True)  
    flowname = models.CharField(db_column='FLOWNAME', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_AGENT_DEF'


class BpmAgentSetting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    authid = models.BigIntegerField(db_column='AUTHID', blank=True, null=True)  
    authname = models.CharField(db_column='AUTHNAME', max_length=100, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME')  
    startdate = models.DateTimeField(db_column='STARTDATE')  
    enddate = models.DateTimeField(db_column='ENDDATE', blank=True, null=True)  
    enabled = models.SmallIntegerField(db_column='ENABLED', blank=True, null=True)  
    authtype = models.SmallIntegerField(db_column='AUTHTYPE', blank=True, null=True)  
    agentid = models.BigIntegerField(db_column='AGENTID', blank=True, null=True)  
    agent = models.CharField(db_column='AGENT', max_length=100, blank=True, null=True)  
    flowkey = models.CharField(db_column='FLOWKEY', max_length=100, blank=True, null=True)  
    flowname = models.CharField(db_column='FLOWNAME', max_length=100, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_AGENT_SETTING'


class BpmApprovalItem(models.Model):
    itemid = models.BigIntegerField(db_column='ITEMID', primary_key=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    defkey = models.CharField(db_column='DEFKEY', max_length=128, blank=True, null=True)  
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  
    type = models.SmallIntegerField(db_column='TYPE', blank=True, null=True)  
    expression = models.CharField(db_column='EXPRESSION', max_length=3000, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_APPROVAL_ITEM'


class BpmBusLink(models.Model):
    bus_id = models.BigIntegerField(db_column='BUS_ID')  
    bus_form_table = models.CharField(db_column='BUS_FORM_TABLE', max_length=255)  
    bus_pk = models.BigIntegerField(db_column='BUS_PK', blank=True, null=True)  
    bus_pkstr = models.CharField(db_column='BUS_PKSTR', max_length=50, blank=True, null=True)  
    bus_def_id = models.BigIntegerField(db_column='BUS_DEF_ID', blank=True, null=True)  
    bus_flow_runid = models.BigIntegerField(db_column='BUS_FLOW_RUNID', blank=True, null=True)  
    bus_creator_id = models.BigIntegerField(db_column='BUS_CREATOR_ID', blank=True, null=True)  
    bus_creator = models.CharField(db_column='BUS_CREATOR', max_length=50, blank=True, null=True)  
    bus_org_id = models.BigIntegerField(db_column='BUS_ORG_ID', blank=True, null=True)  
    bus_org_name = models.CharField(db_column='BUS_ORG_NAME', max_length=200, blank=True, null=True)  
    bus_createtime = models.DateTimeField(db_column='BUS_CREATETIME')  
    bus_updid = models.BigIntegerField(db_column='BUS_UPDID', blank=True, null=True)  
    bus_upd = models.CharField(db_column='BUS_UPD', max_length=50, blank=True, null=True)  
    bus_updtime = models.DateTimeField(db_column='BUS_UPDTIME')  

    class Meta:
        managed = False
        db_table = 'BPM_BUS_LINK'
        unique_together = (('bus_id', 'bus_form_table'),)


class BpmCommonWsParams(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    setid = models.BigIntegerField(db_column='SETID')  
    name = models.CharField(db_column='NAME', max_length=200, blank=True, null=True)  
    param_type = models.IntegerField(db_column='PARAM_TYPE', blank=True, null=True)  
    description = models.CharField(db_column='DESCRIPTION', max_length=400, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_COMMON_WS_PARAMS'


class BpmCommonWsSet(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    alias = models.CharField(db_column='ALIAS', max_length=200)  
    wsdl_url = models.CharField(db_column='WSDL_URL', max_length=400, blank=True, null=True)  
    document = models.TextField(db_column='DOCUMENT', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_COMMON_WS_SET'


class BpmCommuReceiver(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    opinionid = models.BigIntegerField(db_column='OPINIONID', blank=True, null=True)
    recevierid = models.BigIntegerField(db_column='RECEVIERID', blank=True, null=True)
    receivername = models.CharField(db_column='RECEIVERNAME', max_length=100, blank=True, null=True)
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)
    receivetime = models.DateTimeField(db_column='RECEIVETIME')
    createtime = models.DateTimeField(db_column='CREATETIME')
    feedbacktime = models.DateTimeField(db_column='FEEDBACKTIME')
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BPM_COMMU_RECEIVER'


class BpmDataTemplate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)
    tableid = models.BigIntegerField(db_column='TABLEID', blank=True, null=True)
    formkey = models.BigIntegerField(db_column='FORMKEY', blank=True, null=True)
    name = models.CharField(db_column='NAME', max_length=300, blank=True, null=True)
    alias = models.CharField(db_column='ALIAS', max_length=50, blank=True, null=True)
    style = models.SmallIntegerField(db_column='STYLE', blank=True, null=True)
    needpage = models.SmallIntegerField(db_column='NEEDPAGE', blank=True, null=True)
    pagesize = models.SmallIntegerField(db_column='PAGESIZE', blank=True, null=True)
    templatealias = models.CharField(db_column='TEMPLATEALIAS', max_length=50, blank=True, null=True)
    templatehtml = models.TextField(db_column='TEMPLATEHTML', blank=True, null=True)
    displayfield = models.TextField(db_column='DISPLAYFIELD', blank=True, null=True)
    sortfield = models.CharField(db_column='SORTFIELD', max_length=200, blank=True, null=True)
    conditionfield = models.TextField(db_column='CONDITIONFIELD', blank=True, null=True)
    managefield = models.CharField(db_column='MANAGEFIELD', max_length=2000, blank=True, null=True)
    filterfield = models.TextField(db_column='FILTERFIELD', blank=True, null=True)
    varfield = models.CharField(db_column='VARFIELD', max_length=200, blank=True, null=True)
    filtertype = models.SmallIntegerField(db_column='FILTERTYPE', blank=True, null=True)
    source = models.SmallIntegerField(db_column='SOURCE', blank=True, null=True)
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)
    isquery = models.SmallIntegerField(db_column='ISQUERY', blank=True, null=True)
    isfilter = models.IntegerField(db_column='ISFILTER', blank=True, null=True)
    printfield = models.TextField(db_column='PRINTFIELD', blank=True, null=True)
    exportfield = models.TextField(db_column='EXPORTFIELD', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BPM_DATA_TEMPLATE'


class BpmDefinition(models.Model):
    defid = models.BigIntegerField(db_column='DEFID', primary_key=True)
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)
    subject = models.CharField(db_column='SUBJECT', max_length=256)
    defkey = models.CharField(db_column='DEFKEY', max_length=128)
    tasknamerule = models.CharField(db_column='TASKNAMERULE', max_length=512, blank=True, null=True)
    descp = models.CharField(db_column='DESCP', max_length=1024, blank=True, null=True)  
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  
    defxml = models.TextField(db_column='DEFXML', blank=True, null=True)  
    actdeployid = models.BigIntegerField(db_column='ACTDEPLOYID', blank=True, null=True)  
    actdefkey = models.CharField(db_column='ACTDEFKEY', max_length=255, blank=True, null=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=128, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  
    updatetime = models.DateTimeField(db_column='UPDATETIME', blank=True, null=True)  
    createby = models.BigIntegerField(db_column='CREATEBY', blank=True, null=True)  
    updateby = models.BigIntegerField(db_column='UPDATEBY', blank=True, null=True)  
    reason = models.CharField(db_column='REASON', max_length=512, blank=True, null=True)  
    versionno = models.BigIntegerField(db_column='VERSIONNO', blank=True, null=True)  
    parentdefid = models.BigIntegerField(db_column='PARENTDEFID', blank=True, null=True)  
    ismain = models.SmallIntegerField(db_column='ISMAIN', blank=True, null=True)  
    tofirstnode = models.BigIntegerField(db_column='TOFIRSTNODE', blank=True, null=True)  
    showfirstassignee = models.SmallIntegerField(db_column='SHOWFIRSTASSIGNEE', blank=True, null=True)  
    canchoicepath = models.CharField(db_column='CANCHOICEPATH', max_length=500, blank=True, null=True)  
    isuseoutform = models.SmallIntegerField(db_column='ISUSEOUTFORM', blank=True, null=True)  
    formdetailurl = models.CharField(db_column='FORMDETAILURL', max_length=200, blank=True, null=True)  
    allowfinishedcc = models.SmallIntegerField(db_column='ALLOWFINISHEDCC', blank=True, null=True)  
    submitconfirm = models.SmallIntegerField(db_column='SUBMITCONFIRM', blank=True, null=True)  
    allowdivert = models.SmallIntegerField(db_column='ALLOWDIVERT', blank=True, null=True)  
    informstart = models.CharField(db_column='INFORMSTART', max_length=20, blank=True, null=True)  
    informtype = models.CharField(db_column='INFORMTYPE', max_length=20, blank=True, null=True)  
    attachment = models.CharField(db_column='ATTACHMENT', max_length=80, blank=True, null=True)  
    sameexecutorjump = models.SmallIntegerField(db_column='SAMEEXECUTORJUMP', blank=True, null=True)  
    allowrefer = models.SmallIntegerField(db_column='ALLOWREFER', blank=True, null=True)  
    instanceamount = models.SmallIntegerField(db_column='INSTANCEAMOUNT', blank=True, null=True)  
    allowfinisheddivert = models.SmallIntegerField(db_column='ALLOWFINISHEDDIVERT', blank=True, null=True)  
    isprintform = models.SmallIntegerField(db_column='ISPRINTFORM', blank=True, null=True)  
    directstart = models.SmallIntegerField(db_column='DIRECTSTART', blank=True, null=True)  
    ccmessagetype = models.CharField(db_column='CCMESSAGETYPE', max_length=100, blank=True, null=True)  
    allowdeldraf = models.SmallIntegerField(db_column='ALLOWDELDRAF', blank=True, null=True)  
    teststatustag = models.CharField(db_column='TESTSTATUSTAG', max_length=100, blank=True, null=True)  
    allowmobile = models.IntegerField(db_column='ALLOWMOBILE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_DEFINITION'


class BpmDefAct(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    authorize_id = models.BigIntegerField(db_column='AUTHORIZE_ID')  
    def_key = models.CharField(db_column='DEF_KEY', max_length=100)  
    def_name = models.CharField(db_column='DEF_NAME', max_length=200, blank=True, null=True)  
    right_content = models.CharField(db_column='RIGHT_CONTENT', max_length=400, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_DEF_ACT'


class BpmDefAuthorize(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    authorize_desc = models.CharField(db_column='AUTHORIZE_DESC', max_length=512, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_DEF_AUTHORIZE'


class BpmDefAuthType(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    authorize_id = models.BigIntegerField(db_column='AUTHORIZE_ID')  
    authorize_type = models.CharField(db_column='AUTHORIZE_TYPE', max_length=64)  

    class Meta:
        managed = False
        db_table = 'BPM_DEF_AUTH_TYPE'


class BpmDefRights(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    flowtypeid = models.BigIntegerField(db_column='FLOWTYPEID', blank=True, null=True)  
    righttype = models.BigIntegerField(db_column='RIGHTTYPE', blank=True, null=True)  
    ownerid = models.BigIntegerField(db_column='OWNERID', blank=True, null=True)  
    ownername = models.CharField(db_column='OWNERNAME', max_length=128, blank=True, null=True)  
    searchtype = models.BigIntegerField(db_column='SEARCHTYPE', blank=True, null=True)  
    defkey = models.CharField(db_column='DEFKEY', max_length=100, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_DEF_RIGHTS'


class BpmDefUser(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    authorize_id = models.BigIntegerField(db_column='AUTHORIZE_ID')  
    owner_id = models.BigIntegerField(db_column='OWNER_ID')  
    owner_name = models.CharField(db_column='OWNER_NAME', max_length=200, blank=True, null=True)  
    right_type = models.CharField(db_column='RIGHT_TYPE', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_DEF_USER'


class BpmDefVars(models.Model):
    varid = models.BigIntegerField(db_column='VARID', primary_key=True)  
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  
    varname = models.CharField(db_column='VARNAME', max_length=128)  
    varkey = models.CharField(db_column='VARKEY', max_length=128, blank=True, null=True)  
    vardatatype = models.CharField(db_column='VARDATATYPE', max_length=64, blank=True, null=True)  
    defvalue = models.CharField(db_column='DEFVALUE', max_length=256, blank=True, null=True)  
    nodename = models.CharField(db_column='NODENAME', max_length=256, blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=256, blank=True, null=True)  
    actdeployid = models.BigIntegerField(db_column='ACTDEPLOYID', blank=True, null=True)  
    varscope = models.CharField(db_column='VARSCOPE', max_length=64, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_DEF_VARS'


class BpmExeStack(models.Model):
    stackid = models.BigIntegerField(db_column='STACKID', primary_key=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=64, blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=128)  
    nodename = models.CharField(db_column='NODENAME', max_length=256, blank=True, null=True)  
    starttime = models.DateTimeField(db_column='STARTTIME', blank=True, null=True)  
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  
    assignees = models.CharField(db_column='ASSIGNEES', max_length=1024, blank=True, null=True)  
    ismultitask = models.SmallIntegerField(db_column='ISMULTITASK', blank=True, null=True)  
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  
    taskids = models.CharField(db_column='TASKIDS', max_length=512, blank=True, null=True)  
    nodepath = models.CharField(db_column='NODEPATH', max_length=1024, blank=True, null=True)  
    depth = models.BigIntegerField(db_column='DEPTH', blank=True, null=True)  
    tasktoken = models.CharField(db_column='TASKTOKEN', max_length=128, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_EXE_STACK'


class BpmFormDef(models.Model):
    formdefid = models.BigIntegerField(db_column='FORMDEFID', primary_key=True)  
    categoryid = models.BigIntegerField(db_column='CATEGORYID', blank=True, null=True)  
    formkey = models.CharField(db_column='FORMKEY', max_length=128, blank=True, null=True)  
    subject = models.CharField(db_column='SUBJECT', max_length=128, blank=True, null=True)  
    formdesc = models.CharField(db_column='FORMDESC', max_length=200, blank=True, null=True)  
    html = models.TextField(db_column='HTML', blank=True, null=True)  
    template = models.TextField(db_column='TEMPLATE', blank=True, null=True)  
    isdefault = models.SmallIntegerField(db_column='ISDEFAULT', blank=True, null=True)  
    versionno = models.BigIntegerField(db_column='VERSIONNO', blank=True, null=True)  
    tableid = models.BigIntegerField(db_column='TABLEID', blank=True, null=True)  
    ispublished = models.SmallIntegerField(db_column='ISPUBLISHED', blank=True, null=True)  
    publishedby = models.CharField(db_column='PUBLISHEDBY', max_length=20, blank=True, null=True)  
    publishtime = models.DateTimeField(db_column='PUBLISHTIME', blank=True, null=True)  
    tabtitle = models.CharField(db_column='TABTITLE', max_length=500, blank=True, null=True)  
    designtype = models.SmallIntegerField(db_column='DESIGNTYPE', blank=True, null=True)  
    templatesid = models.CharField(db_column='TEMPLATESID', max_length=128, blank=True, null=True)  
    createby = models.BigIntegerField(db_column='CREATEBY', blank=True, null=True)  
    creator = models.CharField(db_column='CREATOR', max_length=50, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME')  

    class Meta:
        managed = False
        db_table = 'BPM_FORM_DEF'


class BpmFormDefHi(models.Model):
    hisid = models.BigIntegerField(db_column='HISID', primary_key=True)  
    formdefid = models.BigIntegerField(db_column='FORMDEFID')  
    categoryid = models.BigIntegerField(db_column='CATEGORYID', blank=True, null=True)  
    formkey = models.CharField(db_column='FORMKEY', max_length=200, blank=True, null=True)  
    subject = models.CharField(db_column='SUBJECT', max_length=128, blank=True, null=True)  
    formdesc = models.CharField(db_column='FORMDESC', max_length=200, blank=True, null=True)  
    html = models.TextField(db_column='HTML', blank=True, null=True)  
    template = models.TextField(db_column='TEMPLATE', blank=True, null=True)  
    isdefault = models.SmallIntegerField(db_column='ISDEFAULT', blank=True, null=True)  
    versionno = models.BigIntegerField(db_column='VERSIONNO', blank=True, null=True)  
    tableid = models.BigIntegerField(db_column='TABLEID', blank=True, null=True)  
    ispublished = models.SmallIntegerField(db_column='ISPUBLISHED', blank=True, null=True)  
    publishedby = models.CharField(db_column='PUBLISHEDBY', max_length=20, blank=True, null=True)  
    publishtime = models.DateTimeField(db_column='PUBLISHTIME', blank=True, null=True)  
    tabtitle = models.CharField(db_column='TABTITLE', max_length=500, blank=True, null=True)  
    designtype = models.SmallIntegerField(db_column='DESIGNTYPE', blank=True, null=True)  
    templatesid = models.CharField(db_column='TEMPLATESID', max_length=128, blank=True, null=True)  
    createby = models.BigIntegerField(db_column='CREATEBY', blank=True, null=True)  
    creator = models.CharField(db_column='CREATOR', max_length=50, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_FORM_DEF_HI'


class BpmFormDialog(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    alias = models.CharField(db_column='ALIAS', max_length=50, blank=True, null=True)  
    style = models.SmallIntegerField(db_column='STYLE', blank=True, null=True)  
    width = models.BigIntegerField(db_column='WIDTH', blank=True, null=True)  
    height = models.BigIntegerField(db_column='HEIGHT', blank=True, null=True)  
    issingle = models.SmallIntegerField(db_column='ISSINGLE', blank=True, null=True)  
    needpage = models.SmallIntegerField(db_column='NEEDPAGE', blank=True, null=True)  
    istable = models.SmallIntegerField(db_column='ISTABLE', blank=True, null=True)  
    objname = models.CharField(db_column='OBJNAME', max_length=50, blank=True, null=True)  
    displayfield = models.CharField(db_column='DISPLAYFIELD', max_length=2000, blank=True, null=True)  
    conditionfield = models.CharField(db_column='CONDITIONFIELD', max_length=2000, blank=True, null=True)  
    resultfield = models.CharField(db_column='RESULTFIELD', max_length=1000, blank=True, null=True)  
    dsname = models.CharField(db_column='DSNAME', max_length=50, blank=True, null=True)  
    dsalias = models.CharField(db_column='DSALIAS', max_length=50, blank=True, null=True)  
    pagesize = models.SmallIntegerField(db_column='PAGESIZE', blank=True, null=True)  
    sortfield = models.CharField(db_column='SORTFIELD', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_FORM_DIALOG'


class BpmFormField(models.Model):
    fieldid = models.BigIntegerField(db_column='FIELDID', primary_key=True)  
    tableid = models.BigIntegerField(db_column='TABLEID', blank=True, null=True)  
    fieldname = models.CharField(db_column='FIELDNAME', max_length=128)  
    fieldtype = models.CharField(db_column='FIELDTYPE', max_length=128)  
    isrequired = models.SmallIntegerField(db_column='ISREQUIRED', blank=True, null=True)  
    islist = models.SmallIntegerField(db_column='ISLIST', blank=True, null=True)  
    isquery = models.SmallIntegerField(db_column='ISQUERY', blank=True, null=True)  
    fielddesc = models.CharField(db_column='FIELDDESC', max_length=128, blank=True, null=True)  
    charlen = models.BigIntegerField(db_column='CHARLEN', blank=True, null=True)  
    intlen = models.BigIntegerField(db_column='INTLEN', blank=True, null=True)  
    decimallen = models.BigIntegerField(db_column='DECIMALLEN', blank=True, null=True)  
    dicttype = models.CharField(db_column='DICTTYPE', max_length=100, blank=True, null=True)  
    isdeleted = models.SmallIntegerField(db_column='ISDELETED', blank=True, null=True)  
    validrule = models.CharField(db_column='VALIDRULE', max_length=64, blank=True, null=True)  
    originalname = models.CharField(db_column='ORIGINALNAME', max_length=128, blank=True, null=True)  
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  
    valuefrom = models.SmallIntegerField(db_column='VALUEFROM', blank=True, null=True)  
    script = models.CharField(db_column='SCRIPT', max_length=1000, blank=True, null=True)  
    controltype = models.SmallIntegerField(db_column='CONTROLTYPE', blank=True, null=True)  
    ishidden = models.SmallIntegerField(db_column='ISHIDDEN', blank=True, null=True)  
    isflowvar = models.SmallIntegerField(db_column='ISFLOWVAR', blank=True, null=True)  
    serialnum = models.CharField(db_column='SERIALNUM', max_length=20, blank=True, null=True)  
    options = models.CharField(db_column='OPTIONS', max_length=1000, blank=True, null=True)  
    ctlproperty = models.CharField(db_column='CTLPROPERTY', max_length=2000, blank=True, null=True)  
    isallowmobile = models.SmallIntegerField(db_column='ISALLOWMOBILE', blank=True, null=True)  
    iswebsign = models.SmallIntegerField(db_column='ISWEBSIGN', blank=True, null=True)  
    isreference = models.SmallIntegerField(db_column='ISREFERENCE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_FORM_FIELD'


class BpmFormQuery(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    alias = models.CharField(db_column='ALIAS', max_length=50, blank=True, null=True)  
    obj_name = models.CharField(db_column='OBJ_NAME', max_length=50, blank=True, null=True)  
    needpage = models.BigIntegerField(db_column='NEEDPAGE', blank=True, null=True)  
    conditionfield = models.CharField(db_column='CONDITIONFIELD', max_length=2000, blank=True, null=True)  
    resultfield = models.CharField(db_column='RESULTFIELD', max_length=2000, blank=True, null=True)  
    dsname = models.CharField(db_column='DSNAME', max_length=50, blank=True, null=True)  
    dsalias = models.CharField(db_column='DSALIAS', max_length=50, blank=True, null=True)  
    pagesize = models.BigIntegerField(db_column='PAGESIZE', blank=True, null=True)  
    istable = models.BigIntegerField(db_column='ISTABLE', blank=True, null=True)  
    sortfield = models.CharField(db_column='SORTFIELD', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_FORM_QUERY'


class BpmFormRights(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    formdefid = models.BigIntegerField(db_column='FORMDEFID', blank=True, null=True)  
    name = models.CharField(db_column='NAME', max_length=128, blank=True, null=True)  
    permission = models.CharField(db_column='PERMISSION', max_length=2000, blank=True, null=True)  
    type = models.SmallIntegerField(db_column='TYPE', blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=60, blank=True, null=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=60, blank=True, null=True)  
    parentactdefid = models.CharField(db_column='PARENTACTDEFID', max_length=128, blank=True, null=True)  
    platform = models.IntegerField(db_column='PLATFORM', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_FORM_RIGHTS'


class BpmFormRule(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    regulation = models.CharField(db_column='REGULATION', max_length=100, blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=100, blank=True, null=True)  
    tipinfo = models.CharField(db_column='TIPINFO', max_length=100, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_FORM_RULE'


class BpmFormRun(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    formdefid = models.BigIntegerField(db_column='FORMDEFID', blank=True, null=True)  
    formdefkey = models.BigIntegerField(db_column='FORMDEFKEY', blank=True, null=True)  
    actinstanceid = models.CharField(db_column='ACTINSTANCEID', max_length=64, blank=True, null=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=64, blank=True, null=True)  
    actnodeid = models.CharField(db_column='ACTNODEID', max_length=64, blank=True, null=True)  
    runid = models.BigIntegerField(db_column='RUNID', blank=True, null=True)  
    settype = models.SmallIntegerField(db_column='SETTYPE', blank=True, null=True)  
    formtype = models.SmallIntegerField(db_column='FORMTYPE', blank=True, null=True)  
    formurl = models.CharField(db_column='FORMURL', max_length=255, blank=True, null=True)  
    mobileformid = models.BigIntegerField(db_column='MOBILEFORMID', blank=True, null=True)  
    mobileformkey = models.BigIntegerField(db_column='MOBILEFORMKEY', blank=True, null=True)  
    mobileformurl = models.CharField(db_column='MOBILEFORMURL', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_FORM_RUN'


class BpmFormTable(models.Model):
    tableid = models.BigIntegerField(db_column='TABLEID', primary_key=True)  
    tablename = models.CharField(db_column='TABLENAME', max_length=128)  
    tabledesc = models.CharField(db_column='TABLEDESC', max_length=128, blank=True, null=True)  
    ismain = models.SmallIntegerField(db_column='ISMAIN', blank=True, null=True)  
    maintableid = models.BigIntegerField(db_column='MAINTABLEID', blank=True, null=True)  
    ispublished = models.SmallIntegerField(db_column='ISPUBLISHED', blank=True, null=True)  
    publishedby = models.CharField(db_column='PUBLISHEDBY', max_length=100, blank=True, null=True)  
    publishtime = models.DateTimeField(db_column='PUBLISHTIME', blank=True, null=True)  
    isexternal = models.SmallIntegerField(db_column='ISEXTERNAL', blank=True, null=True)  
    dsalias = models.CharField(db_column='DSALIAS', max_length=50, blank=True, null=True)  
    dsname = models.CharField(db_column='DSNAME', max_length=50, blank=True, null=True)  
    relation = models.CharField(db_column='RELATION', max_length=500, blank=True, null=True)  
    keytype = models.SmallIntegerField(db_column='KEYTYPE', blank=True, null=True)  
    keyvalue = models.CharField(db_column='KEYVALUE', max_length=20, blank=True, null=True)  
    pkfield = models.CharField(db_column='PKFIELD', max_length=20, blank=True, null=True)  
    listtemplate = models.TextField(db_column='LISTTEMPLATE', blank=True, null=True)  
    detailtemplate = models.TextField(db_column='DETAILTEMPLATE', blank=True, null=True)  
    genbyform = models.SmallIntegerField(db_column='GENBYFORM', blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME')  
    creator = models.CharField(db_column='CREATOR', max_length=50, blank=True, null=True)  
    createby = models.BigIntegerField(db_column='CREATEBY', blank=True, null=True)  
    keydatatype = models.SmallIntegerField(db_column='KEYDATATYPE', blank=True, null=True)  
    team = models.TextField(db_column='TEAM', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_FORM_TABLE'


class BpmFormTemplate(models.Model):
    templateid = models.BigIntegerField(db_column='TEMPLATEID', primary_key=True)  
    templatename = models.CharField(db_column='TEMPLATENAME', max_length=200, blank=True, null=True)  
    templatetype = models.CharField(db_column='TEMPLATETYPE', max_length=20, blank=True, null=True)  
    macrotemplatealias = models.CharField(db_column='MACROTEMPLATEALIAS', max_length=50, blank=True, null=True)  
    html = models.TextField(db_column='HTML', blank=True, null=True)  
    templatedesc = models.CharField(db_column='TEMPLATEDESC', max_length=400, blank=True, null=True)  
    canedit = models.SmallIntegerField(db_column='CANEDIT', blank=True, null=True)  
    alias = models.CharField(db_column='ALIAS', max_length=50, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_FORM_TEMPLATE'


class BpmGangedSet(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=100, blank=True, null=True)  
    nodename = models.CharField(db_column='NODENAME', max_length=200, blank=True, null=True)  
    choisefield = models.TextField(db_column='CHOISEFIELD', blank=True, null=True)  
    changefield = models.TextField(db_column='CHANGEFIELD', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_GANGED_SET'


class BpmMobileForm(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    formid = models.BigIntegerField(db_column='FORMID', blank=True, null=True)  
    formkey = models.BigIntegerField(db_column='FORMKEY', blank=True, null=True)  
    html = models.TextField(db_column='HTML', blank=True, null=True)  
    template = models.TextField(db_column='TEMPLATE', blank=True, null=True)  
    guid = models.CharField(db_column='GUID', max_length=128, blank=True, null=True)  
    isdefault = models.IntegerField(db_column='ISDEFAULT', blank=True, null=True)  
    formjson = models.TextField(db_column='FORMJSON', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_MOBILE_FORM'


class BpmMonGroup(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=200, blank=True, null=True)  
    grade = models.SmallIntegerField(db_column='GRADE', blank=True, null=True)  
    enabled = models.SmallIntegerField(db_column='ENABLED', blank=True, null=True)  
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  
    creator = models.CharField(db_column='CREATOR', max_length=50, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_MON_GROUP'


class BpmMonGroupitem(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    groupid = models.BigIntegerField(db_column='GROUPID', blank=True, null=True)  
    flowkey = models.CharField(db_column='FLOWKEY', max_length=50, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_MON_GROUPITEM'


class BpmMonOrgrole(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    groupid = models.BigIntegerField(db_column='GROUPID', blank=True, null=True)  
    roleid = models.BigIntegerField(db_column='ROLEID', blank=True, null=True)  
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_MON_ORGROLE'


class BpmNodeBtn(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=64, blank=True, null=True)  
    isstartform = models.SmallIntegerField(db_column='ISSTARTFORM', blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=50, blank=True, null=True)  
    btnname = models.CharField(db_column='BTNNAME', max_length=50, blank=True, null=True)  
    iconclsname = models.CharField(db_column='ICONCLSNAME', max_length=50, blank=True, null=True)  
    operatortype = models.SmallIntegerField(db_column='OPERATORTYPE', blank=True, null=True)  
    prevscript = models.CharField(db_column='PREVSCRIPT', max_length=2000, blank=True, null=True)  
    afterscript = models.CharField(db_column='AFTERSCRIPT', max_length=2000, blank=True, null=True)  
    nodetype = models.SmallIntegerField(db_column='NODETYPE', blank=True, null=True)  
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_NODE_BTN'


class BpmNodeMessage(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=64, blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=50, blank=True, null=True)  
    messagetype = models.SmallIntegerField(db_column='MESSAGETYPE', blank=True, null=True)  
    subject = models.CharField(db_column='SUBJECT', max_length=200, blank=True, null=True)  
    template = models.TextField(db_column='TEMPLATE', blank=True, null=True)  
    issend = models.SmallIntegerField(db_column='ISSEND', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_NODE_MESSAGE'


class BpmNodePrivilege(models.Model):
    privilegeid = models.BigIntegerField(db_column='PRIVILEGEID', primary_key=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=128, blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=128, blank=True, null=True)  
    privilegemode = models.SmallIntegerField(db_column='PRIVILEGEMODE', blank=True, null=True)  
    usertype = models.SmallIntegerField(db_column='USERTYPE', blank=True, null=True)  
    cmpnames = models.TextField(db_column='CMPNAMES', blank=True, null=True)  
    cmpids = models.TextField(db_column='CMPIDS', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_NODE_PRIVILEGE'


class BpmNodeRule(models.Model):
    ruleid = models.BigIntegerField(db_column='RULEID', primary_key=True)  
    rulename = models.CharField(db_column='RULENAME', max_length=128)  
    conditioncode = models.TextField(db_column='CONDITIONCODE', blank=True, null=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=50, blank=True, null=True)  
    priority = models.BigIntegerField(db_column='PRIORITY', blank=True, null=True)  
    targetnode = models.CharField(db_column='TARGETNODE', max_length=20, blank=True, null=True)  
    targetnodename = models.CharField(db_column='TARGETNODENAME', max_length=255, blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_NODE_RULE'


class BpmNodeScript(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    memo = models.CharField(db_column='MEMO', max_length=50, blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=20, blank=True, null=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=64, blank=True, null=True)  
    script = models.TextField(db_column='SCRIPT', blank=True, null=True)  
    scripttype = models.BigIntegerField(db_column='SCRIPTTYPE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_NODE_SCRIPT'


class BpmNodeSet(models.Model):
    setid = models.BigIntegerField(db_column='SETID', primary_key=True)  
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  
    nodename = models.CharField(db_column='NODENAME', max_length=256, blank=True, null=True)  
    nodeorder = models.SmallIntegerField(db_column='NODEORDER', blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=128, blank=True, null=True)  
    formtype = models.SmallIntegerField(db_column='FORMTYPE', blank=True, null=True)  
    formurl = models.CharField(db_column='FORMURL', max_length=255, blank=True, null=True)  
    formkey = models.BigIntegerField(db_column='FORMKEY', blank=True, null=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  
    formdefname = models.CharField(db_column='FORMDEFNAME', max_length=255, blank=True, null=True)  
    nodetype = models.SmallIntegerField(db_column='NODETYPE', blank=True, null=True)  
    jointaskkey = models.CharField(db_column='JOINTASKKEY', max_length=128, blank=True, null=True)  
    jointaskname = models.CharField(db_column='JOINTASKNAME', max_length=256, blank=True, null=True)  
    beforehandler = models.CharField(db_column='BEFOREHANDLER', max_length=100, blank=True, null=True)  
    afterhandler = models.CharField(db_column='AFTERHANDLER', max_length=100, blank=True, null=True)  
    jumptype = models.CharField(db_column='JUMPTYPE', max_length=32, blank=True, null=True)  
    settype = models.SmallIntegerField(db_column='SETTYPE', blank=True, null=True)  
    isjumpfordef = models.SmallIntegerField(db_column='ISJUMPFORDEF', blank=True, null=True)  
    ishideoption = models.SmallIntegerField(db_column='ISHIDEOPTION', blank=True, null=True)  
    ishidepath = models.SmallIntegerField(db_column='ISHIDEPATH', blank=True, null=True)  
    detailurl = models.CharField(db_column='DETAILURL', max_length=256, blank=True, null=True)  
    isallowmobile = models.SmallIntegerField(db_column='ISALLOWMOBILE', blank=True, null=True)  
    informtype = models.CharField(db_column='INFORMTYPE', max_length=20, blank=True, null=True)  
    parentactdefid = models.CharField(db_column='PARENTACTDEFID', max_length=127, blank=True, null=True)  
    mobileformkey = models.BigIntegerField(db_column='MOBILEFORMKEY', blank=True, null=True)  
    mobileformurl = models.CharField(db_column='MOBILEFORMURL', max_length=256, blank=True, null=True)  
    mobiledetailurl = models.CharField(db_column='MOBILEDETAILURL', max_length=256, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_NODE_SET'


class BpmNodeSign(models.Model):
    signid = models.BigIntegerField(db_column='SIGNID', primary_key=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=128, blank=True, null=True)  
    voteamount = models.BigIntegerField(db_column='VOTEAMOUNT', blank=True, null=True)  
    decidetype = models.SmallIntegerField(db_column='DECIDETYPE')  
    votetype = models.SmallIntegerField(db_column='VOTETYPE', blank=True, null=True)  
    flowmode = models.SmallIntegerField(db_column='FLOWMODE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_NODE_SIGN'


class BpmNodeUser(models.Model):
    nodeuserid = models.BigIntegerField(db_column='NODEUSERID', primary_key=True)  
    cmpids = models.TextField(db_column='CMPIDS', blank=True, null=True)  
    cmpnames = models.TextField(db_column='CMPNAMES', blank=True, null=True)  
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  
    assigntype = models.CharField(db_column='ASSIGNTYPE', max_length=20)  
    comptype = models.SmallIntegerField(db_column='COMPTYPE', blank=True, null=True)  
    conditionid = models.BigIntegerField(db_column='CONDITIONID', blank=True, null=True)  
    extractuser = models.SmallIntegerField(db_column='EXTRACTUSER', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_NODE_USER'


class BpmNodeWebservice(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=128, blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=128, blank=True, null=True)  
    document = models.TextField(db_column='DOCUMENT', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_NODE_WEBSERVICE'


class BpmNodeWsParams(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    webserviceid = models.BigIntegerField(db_column='WEBSERVICEID', blank=True, null=True)  
    paratype = models.BigIntegerField(db_column='PARATYPE', blank=True, null=True)  
    varid = models.BigIntegerField(db_column='VARID', blank=True, null=True)  
    wsname = models.CharField(db_column='WSNAME', max_length=256, blank=True, null=True)  
    type = models.CharField(db_column='TYPE', max_length=128, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_NODE_WS_PARAMS'


class BpmPrintTemplate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    form_key = models.BigIntegerField(db_column='FORM_KEY', blank=True, null=True)  
    temapalte_name = models.CharField(db_column='TEMAPALTE_NAME', max_length=200, blank=True, null=True)  
    is_default = models.SmallIntegerField(db_column='IS_DEFAULT', blank=True, null=True)  
    tableid = models.BigIntegerField(db_column='TABLEID', blank=True, null=True)  
    html = models.TextField(db_column='HTML', blank=True, null=True)  
    template = models.TextField(db_column='TEMPLATE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_PRINT_TEMPLATE'


class BpmProCpto(models.Model):
    copy_id = models.BigIntegerField(db_column='COPY_ID', primary_key=True)  
    acact_inst_id = models.BigIntegerField(db_column='ACACT_INST_ID')  
    run_id = models.BigIntegerField(db_column='RUN_ID')  
    node_key = models.CharField(db_column='NODE_KEY', max_length=100, blank=True, null=True)  
    node_name = models.CharField(db_column='NODE_NAME', max_length=100, blank=True, null=True)  
    cc_uid = models.BigIntegerField(db_column='CC_UID', blank=True, null=True)  
    cc_uname = models.CharField(db_column='CC_UNAME', max_length=50, blank=True, null=True)  
    cc_time = models.DateTimeField(db_column='CC_TIME')  
    is_readed = models.SmallIntegerField(db_column='IS_READED', blank=True, null=True)  
    fill_opinion = models.CharField(db_column='FILL_OPINION', max_length=2000, blank=True, null=True)  
    subject = models.CharField(db_column='SUBJECT', max_length=300, blank=True, null=True)  
    read_time = models.DateTimeField(db_column='READ_TIME')  
    cp_type = models.SmallIntegerField(db_column='CP_TYPE', blank=True, null=True)  
    create_id = models.BigIntegerField(db_column='CREATE_ID', blank=True, null=True)  
    creator = models.CharField(db_column='CREATOR', max_length=50, blank=True, null=True)  
    def_typeid = models.BigIntegerField(db_column='DEF_TYPEID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_PRO_CPTO'


class BpmProRun(models.Model):
    runid = models.BigIntegerField(db_column='RUNID', primary_key=True)  
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  
    processname = models.CharField(db_column='PROCESSNAME', max_length=256, blank=True, null=True)  
    subject = models.CharField(db_column='SUBJECT', max_length=600, blank=True, null=True)  
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  
    creator = models.CharField(db_column='CREATOR', max_length=128, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  
    busdescp = models.CharField(db_column='BUSDESCP', max_length=3000, blank=True, null=True)  
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=256, blank=True, null=True)  
    businesskey = models.CharField(db_column='BUSINESSKEY', max_length=255, blank=True, null=True)  
    businessurl = models.CharField(db_column='BUSINESSURL', max_length=255, blank=True, null=True)  
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  
    duration = models.BigIntegerField(db_column='DURATION', blank=True, null=True)  
    pkname = models.CharField(db_column='PKNAME', max_length=50, blank=True, null=True)  
    tablename = models.CharField(db_column='TABLENAME', max_length=50, blank=True, null=True)  
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  
    startorgid = models.BigIntegerField(db_column='STARTORGID', blank=True, null=True)  
    startorgname = models.CharField(db_column='STARTORGNAME', max_length=200, blank=True, null=True)  
    formdefid = models.BigIntegerField(db_column='FORMDEFID', blank=True, null=True)  
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  
    dsalias = models.CharField(db_column='DSALIAS', max_length=50, blank=True, null=True)  
    flowkey = models.CharField(db_column='FLOWKEY', max_length=50, blank=True, null=True)  
    formtype = models.SmallIntegerField(db_column='FORMTYPE', blank=True, null=True)  
    formkeyurl = models.CharField(db_column='FORMKEYURL', max_length=50, blank=True, null=True)  
    lastsubmitduration = models.BigIntegerField(db_column='LASTSUBMITDURATION', blank=True, null=True)  
    isformal = models.SmallIntegerField(db_column='ISFORMAL', blank=True, null=True)  
    startnode = models.CharField(db_column='STARTNODE', max_length=50, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_PRO_RUN'


class BpmProRunHis(models.Model):
    runid = models.BigIntegerField(db_column='RUNID', primary_key=True)  
    defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)  
    processname = models.CharField(db_column='PROCESSNAME', max_length=256, blank=True, null=True)  
    subject = models.CharField(db_column='SUBJECT', max_length=600, blank=True, null=True)  
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  
    creator = models.CharField(db_column='CREATOR', max_length=128, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  
    busdescp = models.CharField(db_column='BUSDESCP', max_length=3000, blank=True, null=True)  
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=256, blank=True, null=True)  
    businesskey = models.CharField(db_column='BUSINESSKEY', max_length=255, blank=True, null=True)  
    businessurl = models.CharField(db_column='BUSINESSURL', max_length=255, blank=True, null=True)  
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  
    duration = models.BigIntegerField(db_column='DURATION', blank=True, null=True)  
    pkname = models.CharField(db_column='PKNAME', max_length=50, blank=True, null=True)  
    tablename = models.CharField(db_column='TABLENAME', max_length=50, blank=True, null=True)  
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  
    startorgid = models.BigIntegerField(db_column='STARTORGID', blank=True, null=True)  
    startorgname = models.CharField(db_column='STARTORGNAME', max_length=200, blank=True, null=True)  
    formdefid = models.BigIntegerField(db_column='FORMDEFID', blank=True, null=True)  
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  
    dsalias = models.CharField(db_column='DSALIAS', max_length=50, blank=True, null=True)  
    flowkey = models.CharField(db_column='FLOWKEY', max_length=50, blank=True, null=True)  
    formtype = models.SmallIntegerField(db_column='FORMTYPE', blank=True, null=True)  
    formkeyurl = models.CharField(db_column='FORMKEYURL', max_length=50, blank=True, null=True)  
    lastsubmitduration = models.BigIntegerField(db_column='LASTSUBMITDURATION', blank=True, null=True)  
    isformal = models.SmallIntegerField(db_column='ISFORMAL', blank=True, null=True)  
    startnode = models.CharField(db_column='STARTNODE', max_length=50, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_PRO_RUN_HIS'


# class BpmProStatus(models.Model):
#     id = models.BigIntegerField(db_column='ID', blank=True, null=True)
#     actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)
#     nodeid = models.CharField(db_column='NODEID', max_length=64, blank=True, null=True)
#     nodename = models.CharField(db_column='NODENAME', max_length=255, blank=True, null=True)
#     status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)
#     lastupdatetime = models.DateTimeField(db_column='LASTUPDATETIME', blank=True, null=True)
#     actdefid = models.CharField(db_column='ACTDEFID', max_length=64, blank=True, null=True)
#     defid = models.BigIntegerField(db_column='DEFID', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'BPM_PRO_STATUS'


class BpmProTransto(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  
    transtype = models.SmallIntegerField(db_column='TRANSTYPE', blank=True, null=True)  
    action = models.SmallIntegerField(db_column='ACTION', blank=True, null=True)  
    createuserid = models.BigIntegerField(db_column='CREATEUSERID', blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME')  
    transresult = models.SmallIntegerField(db_column='TRANSRESULT', blank=True, null=True)  
    assignee = models.CharField(db_column='ASSIGNEE', max_length=256, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_PRO_TRANSTO'


class BpmReferDefinition(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    defid = models.CharField(db_column='DEFID', max_length=200, blank=True, null=True)  
    refer_defkey = models.CharField(db_column='REFER_DEFKEY', max_length=128, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME')  
    createid = models.BigIntegerField(db_column='CREATEID', blank=True, null=True)  
    updatetime = models.DateTimeField(db_column='UPDATETIME')  
    state = models.SmallIntegerField(db_column='STATE', blank=True, null=True)  
    remark = models.CharField(db_column='REMARK', max_length=400, blank=True, null=True)  
    subject = models.CharField(db_column='SUBJECT', max_length=200, blank=True, null=True)  
    updateid = models.BigIntegerField(db_column='UPDATEID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_REFER_DEFINITION'


class BpmRunLog(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    username = models.CharField(db_column='USERNAME', max_length=50, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  
    operatortype = models.SmallIntegerField(db_column='OPERATORTYPE', blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=300, blank=True, null=True)  
    runid = models.BigIntegerField(db_column='RUNID', blank=True, null=True)  
    processsubject = models.CharField(db_column='PROCESSSUBJECT', max_length=300, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_RUN_LOG'


class BpmSubtableRights(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=100, blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=50, blank=True, null=True)  
    tableid = models.BigIntegerField(db_column='TABLEID', blank=True, null=True)  
    permissiontype = models.SmallIntegerField(db_column='PERMISSIONTYPE', blank=True, null=True)  
    permissionseting = models.CharField(db_column='PERMISSIONSETING', max_length=2000, blank=True, null=True)  
    parentactdefid = models.CharField(db_column='PARENTACTDEFID', max_length=100, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_SUBTABLE_RIGHTS'


class BpmTaskDue(models.Model):
    taskdueid = models.BigIntegerField(db_column='TASKDUEID', primary_key=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=50, blank=True, null=True)  
    reminderstart = models.BigIntegerField(db_column='REMINDERSTART')  
    reminderend = models.BigIntegerField(db_column='REMINDEREND', blank=True, null=True)  
    times = models.BigIntegerField(db_column='TIMES', blank=True, null=True)  
    mailcontent = models.TextField(db_column='MAILCONTENT', blank=True, null=True)  
    msgcontent = models.TextField(db_column='MSGCONTENT', blank=True, null=True)  
    smscontent = models.TextField(db_column='SMSCONTENT', blank=True, null=True)  
    action = models.BigIntegerField(db_column='ACTION', blank=True, null=True)  
    script = models.CharField(db_column='SCRIPT', max_length=2000, blank=True, null=True)  
    completetime = models.BigIntegerField(db_column='COMPLETETIME', blank=True, null=True)  
    condexp = models.TextField(db_column='CONDEXP', blank=True, null=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    relativenodeid = models.CharField(db_column='RELATIVENODEID', max_length=100, blank=True, null=True)  
    relativenodetype = models.BigIntegerField(db_column='RELATIVENODETYPE', blank=True, null=True)  
    relativetimetype = models.BigIntegerField(db_column='RELATIVETIMETYPE', blank=True, null=True)  
    assignerid = models.BigIntegerField(db_column='ASSIGNERID', blank=True, null=True)  
    assignername = models.CharField(db_column='ASSIGNERNAME', max_length=50, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_TASK_DUE'


class BpmTaskExe(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  
    assignee_id = models.BigIntegerField(db_column='ASSIGNEE_ID', blank=True, null=True)  
    assignee_name = models.CharField(db_column='ASSIGNEE_NAME', max_length=50, blank=True, null=True)  
    owner_id = models.BigIntegerField(db_column='OWNER_ID', blank=True, null=True)  
    owner_name = models.CharField(db_column='OWNER_NAME', max_length=200, blank=True, null=True)  
    subject = models.CharField(db_column='SUBJECT', max_length=400, blank=True, null=True)  
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=4000, blank=True, null=True)  
    cratetime = models.DateTimeField(db_column='CRATETIME', blank=True, null=True)  
    act_inst_id = models.BigIntegerField(db_column='ACT_INST_ID', blank=True, null=True)  
    task_name = models.CharField(db_column='TASK_NAME', max_length=400, blank=True, null=True)  
    task_def_key = models.CharField(db_column='TASK_DEF_KEY', max_length=64, blank=True, null=True)  
    exe_time = models.DateTimeField(db_column='EXE_TIME', blank=True, null=True)  
    exe_user_id = models.BigIntegerField(db_column='EXE_USER_ID', blank=True, null=True)  
    exe_user_name = models.CharField(db_column='EXE_USER_NAME', max_length=256, blank=True, null=True)  
    assign_type = models.SmallIntegerField(db_column='ASSIGN_TYPE', blank=True, null=True)  
    runid = models.BigIntegerField(db_column='RUNID', blank=True, null=True)  
    type_id = models.BigIntegerField(db_column='TYPE_ID', blank=True, null=True)  
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  
    creator = models.CharField(db_column='CREATOR', max_length=256, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_TASK_EXE'


class BpmTaskFork(models.Model):
    taskforkid = models.BigIntegerField(db_column='TASKFORKID', primary_key=True)  
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  
    forktaskname = models.CharField(db_column='FORKTASKNAME', max_length=256, blank=True, null=True)  
    forktaskkey = models.CharField(db_column='FORKTASKKEY', max_length=256, blank=True, null=True)  
    forksn = models.BigIntegerField(db_column='FORKSN', blank=True, null=True)  
    forkcount = models.BigIntegerField(db_column='FORKCOUNT', blank=True, null=True)  
    fininshcount = models.BigIntegerField(db_column='FININSHCOUNT', blank=True, null=True)  
    forktime = models.DateTimeField(db_column='FORKTIME', blank=True, null=True)  
    jointaskname = models.CharField(db_column='JOINTASKNAME', max_length=256, blank=True, null=True)  
    jointaskkey = models.CharField(db_column='JOINTASKKEY', max_length=256, blank=True, null=True)  
    forktokens = models.CharField(db_column='FORKTOKENS', max_length=512, blank=True, null=True)  
    forktokenpre = models.CharField(db_column='FORKTOKENPRE', max_length=64, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_TASK_FORK'


class BpmTaskOpinion(models.Model):
    opinionid = models.BigIntegerField(db_column='OPINIONID', primary_key=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  
    taskname = models.CharField(db_column='TASKNAME', max_length=255, blank=True, null=True)  
    taskkey = models.CharField(db_column='TASKKEY', max_length=64, blank=True, null=True)  
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  
    tasktoken = models.CharField(db_column='TASKTOKEN', max_length=50, blank=True, null=True)  
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  
    starttime = models.DateTimeField(db_column='STARTTIME')  
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  
    durtime = models.BigIntegerField(db_column='DURTIME', blank=True, null=True)  
    exeuserid = models.BigIntegerField(db_column='EXEUSERID', blank=True, null=True)  
    exefullname = models.CharField(db_column='EXEFULLNAME', max_length=127, blank=True, null=True)  
    opinion = models.TextField(db_column='OPINION', blank=True, null=True)  
    checkstatus = models.SmallIntegerField(db_column='CHECKSTATUS', blank=True, null=True)  
    formdefid = models.BigIntegerField(db_column='FORMDEFID', blank=True, null=True)  
    fieldname = models.CharField(db_column='FIELDNAME', max_length=50, blank=True, null=True)  
    superexecution = models.BigIntegerField(db_column='SUPEREXECUTION', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_TASK_OPINION'


class BpmTaskRead(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    actinstid = models.BigIntegerField(db_column='ACTINSTID', blank=True, null=True)  
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    username = models.CharField(db_column='USERNAME', max_length=100, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_TASK_READ'


class BpmTaskReminderstate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  
    remindertime = models.DateTimeField(db_column='REMINDERTIME', blank=True, null=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    actinstanceid = models.BigIntegerField(db_column='ACTINSTANCEID', blank=True, null=True)  
    remindtype = models.SmallIntegerField(db_column='REMINDTYPE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_TASK_REMINDERSTATE'


class BpmTksignData(models.Model):
    dataid = models.BigIntegerField(db_column='DATAID', primary_key=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  
    actinstid = models.BigIntegerField(db_column='ACTINSTID')  
    nodename = models.CharField(db_column='NODENAME', max_length=128, blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=127)  
    taskid = models.BigIntegerField(db_column='TASKID', blank=True, null=True)  
    voteuserid = models.CharField(db_column='VOTEUSERID', max_length=1000)  
    voteusername = models.CharField(db_column='VOTEUSERNAME', max_length=1000, blank=True, null=True)  
    votetime = models.DateTimeField(db_column='VOTETIME', blank=True, null=True)  
    isagree = models.SmallIntegerField(db_column='ISAGREE', blank=True, null=True)  
    content = models.CharField(db_column='CONTENT', max_length=200, blank=True, null=True)  
    signnums = models.BigIntegerField(db_column='SIGNNUMS', blank=True, null=True)  
    iscompleted = models.SmallIntegerField(db_column='ISCOMPLETED', blank=True, null=True)  
    batch = models.SmallIntegerField(db_column='BATCH', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_TKSIGN_DATA'


class BpmUserCondition(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    setid = models.BigIntegerField(db_column='SETID', blank=True, null=True)  
    conditionname = models.CharField(db_column='CONDITIONNAME', max_length=127, blank=True, null=True)  
    actdefid = models.CharField(db_column='ACTDEFID', max_length=127, blank=True, null=True)  
    nodeid = models.CharField(db_column='NODEID', max_length=128, blank=True, null=True)  
    conditioncode = models.TextField(db_column='CONDITIONCODE', blank=True, null=True)  
    sn = models.DecimalField(db_column='SN', max_digits=38, decimal_places=0, blank=True, null=True)  
    conditionshow = models.TextField(db_column='CONDITIONSHOW', blank=True, null=True)  
    conditiontype = models.SmallIntegerField(db_column='CONDITIONTYPE', blank=True, null=True)  
    groupno = models.SmallIntegerField(db_column='GROUPNO', blank=True, null=True)  
    formidentity = models.CharField(db_column='FORMIDENTITY', max_length=30, blank=True, null=True)  
    parentactdefid = models.CharField(db_column='PARENTACTDEFID', max_length=128, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BPM_USER_CONDITION'


class BusQueryFilter(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    ruleid = models.BigIntegerField(db_column='RULEID', blank=True, null=True)  
    tablename = models.CharField(db_column='TABLENAME', max_length=256, blank=True, null=True)  
    filtername = models.CharField(db_column='FILTERNAME', max_length=256, blank=True, null=True)  
    filterdesc = models.TextField(db_column='FILTERDESC', blank=True, null=True)  
    filterkey = models.CharField(db_column='FILTERKEY', max_length=256, blank=True, null=True)  
    queryparameter = models.TextField(db_column='QUERYPARAMETER', blank=True, null=True)  
    sortparameter = models.TextField(db_column='SORTPARAMETER', blank=True, null=True)  
    isshare = models.SmallIntegerField(db_column='ISSHARE', blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME')  
    createby = models.BigIntegerField(db_column='CREATEBY', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BUS_QUERY_FILTER'


class BusQueryRule(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    tablename = models.CharField(db_column='TABLENAME', max_length=128, blank=True, null=True)  
    needpage = models.SmallIntegerField(db_column='NEEDPAGE', blank=True, null=True)  
    pagesize = models.BigIntegerField(db_column='PAGESIZE', blank=True, null=True)  
    isquery = models.SmallIntegerField(db_column='ISQUERY', blank=True, null=True)  
    isfilter = models.SmallIntegerField(db_column='ISFILTER', blank=True, null=True)  
    displayfield = models.TextField(db_column='DISPLAYFIELD', blank=True, null=True)  
    filterfield = models.TextField(db_column='FILTERFIELD', blank=True, null=True)  
    sortfield = models.TextField(db_column='SORTFIELD', blank=True, null=True)  
    exportfield = models.TextField(db_column='EXPORTFIELD', blank=True, null=True)  
    printfield = models.TextField(db_column='PRINTFIELD', blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME')  
    createby = models.BigIntegerField(db_column='CREATEBY', blank=True, null=True)  
    updatetime = models.DateTimeField(db_column='UPDATETIME')  
    updateby = models.BigIntegerField(db_column='UPDATEBY', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BUS_QUERY_RULE'


class BusQuerySetting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    tablename = models.CharField(db_column='TABLENAME', max_length=100, blank=True, null=True)  
    displayfield = models.TextField(db_column='DISPLAYFIELD', blank=True, null=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'BUS_QUERY_SETTING'


class BusQueryShare(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    filterid = models.BigIntegerField(db_column='FILTERID', blank=True, null=True)  
    shareright = models.TextField(db_column='SHARERIGHT', blank=True, null=True)  
    sharerid = models.BigIntegerField(db_column='SHARERID', blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME')  

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
    userid = models.BigIntegerField(db_column='USERID', primary_key=True)  
    username = models.CharField(db_column='USERNAME', max_length=127, blank=True, null=True)  
    idcard = models.CharField(db_column='IDCARD', max_length=40, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'MOBILE_USER_INFO'


class OutMail(models.Model):
    mailid = models.BigIntegerField(db_column='MAILID', primary_key=True)  
    title = models.CharField(db_column='TITLE', max_length=512, blank=True, null=True)  
    content = models.TextField(db_column='CONTENT', blank=True, null=True)  
    senderaddresses = models.CharField(db_column='SENDERADDRESSES', max_length=128, blank=True, null=True)  
    sendername = models.CharField(db_column='SENDERNAME', max_length=128, blank=True, null=True)  
    receiveraddresses = models.TextField(db_column='RECEIVERADDRESSES', blank=True, null=True)  
    receivernames = models.TextField(db_column='RECEIVERNAMES', blank=True, null=True)  
    ccaddresses = models.TextField(db_column='CCADDRESSES', blank=True, null=True)  
    bccanames = models.TextField(db_column='BCCANAMES', blank=True, null=True)  
    bccaddresses = models.TextField(db_column='BCCADDRESSES', blank=True, null=True)  
    ccnames = models.TextField(db_column='CCNAMES', blank=True, null=True)  
    emailid = models.CharField(db_column='EMAILID', max_length=128, blank=True, null=True)  
    types = models.BigIntegerField(db_column='TYPES', blank=True, null=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    isreply = models.BigIntegerField(db_column='ISREPLY', blank=True, null=True)  
    maildate = models.DateTimeField(db_column='MAILDATE', blank=True, null=True)  
    fileids = models.CharField(db_column='FILEIDS', max_length=512, blank=True, null=True)  
    isread = models.BigIntegerField(db_column='ISREAD', blank=True, null=True)  
    setid = models.BigIntegerField(db_column='SETID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'OUT_MAIL'


class OutMailAttachment(models.Model):
    fileid = models.BigIntegerField(db_column='FILEID', primary_key=True)  
    filename = models.CharField(db_column='FILENAME', max_length=100, blank=True, null=True)  
    filepath = models.CharField(db_column='FILEPATH', max_length=100, blank=True, null=True)  
    mailid = models.BigIntegerField(db_column='MAILID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'OUT_MAIL_ATTACHMENT'


class OutMailLinkman(models.Model):
    linkid = models.BigIntegerField(db_column='LINKID', primary_key=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    mailid = models.BigIntegerField(db_column='MAILID', blank=True, null=True)  
    sendtime = models.DateTimeField(db_column='SENDTIME', blank=True, null=True)  
    linkname = models.CharField(db_column='LINKNAME', max_length=20, blank=True, null=True)  
    linkaddress = models.CharField(db_column='LINKADDRESS', max_length=2000, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'OUT_MAIL_LINKMAN'


class OutMailUserSeting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    username = models.CharField(db_column='USERNAME', max_length=128, blank=True, null=True)  
    mailaddress = models.CharField(db_column='MAILADDRESS', max_length=128, blank=True, null=True)  
    mailpass = models.CharField(db_column='MAILPASS', max_length=128, blank=True, null=True)  
    smtphost = models.CharField(db_column='SMTPHOST', max_length=128, blank=True, null=True)  
    smtpport = models.CharField(db_column='SMTPPORT', max_length=64, blank=True, null=True)  
    pophost = models.CharField(db_column='POPHOST', max_length=128, blank=True, null=True)  
    popport = models.CharField(db_column='POPPORT', max_length=64, blank=True, null=True)  
    imaphost = models.CharField(db_column='IMAPHOST', max_length=128, blank=True, null=True)  
    imapport = models.CharField(db_column='IMAPPORT', max_length=128, blank=True, null=True)  
    isdefault = models.SmallIntegerField(db_column='ISDEFAULT', blank=True, null=True)  
    mailtype = models.CharField(db_column='MAILTYPE', max_length=50, blank=True, null=True)  
    usessl = models.SmallIntegerField(db_column='USESSL', blank=True, null=True)  
    isdeleteremote = models.SmallIntegerField(db_column='ISDELETEREMOTE', blank=True, null=True)  
    isvalidate = models.SmallIntegerField(db_column='ISVALIDATE', blank=True, null=True)  
    ishandleattach = models.SmallIntegerField(db_column='ISHANDLEATTACH', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'OUT_MAIL_USER_SETING'


class QrtzBlobTriggers(models.Model):
    sched_name = models.ForeignKey('QrtzTriggers', related_name='QrtzTriggersBlobScheds', db_column='SCHED_NAME')
    trigger_name = models.ForeignKey('QrtzTriggers', related_name='QrtzTriggersBlobTriggers', db_column='TRIGGER_NAME')
    trigger_group = models.ForeignKey('QrtzTriggers', related_name='QrtzTriggersBlobTriggerGroups', db_column='TRIGGER_GROUP')
    blob_data = models.TextField(db_column='BLOB_DATA', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'QRTZ_BLOB_TRIGGERS'
        unique_together = (('sched_name', 'trigger_name', 'trigger_group'),)


class QrtzCalendars(models.Model):
    sched_name = models.CharField(db_column='SCHED_NAME', max_length=120)  
    calendar_name = models.CharField(db_column='CALENDAR_NAME', max_length=200)  
    calendar = models.TextField(db_column='CALENDAR')  

    class Meta:
        managed = False
        db_table = 'QRTZ_CALENDARS'
        unique_together = (('sched_name', 'calendar_name'),)


class QrtzCronTriggers(models.Model):
    sched_name = models.ForeignKey('QrtzTriggers', related_name='QrtzTriggersCronScheds', db_column='SCHED_NAME')
    trigger_name = models.ForeignKey('QrtzTriggers', related_name='QrtzTriggersCronTriggers', db_column='TRIGGER_NAME')
    trigger_group = models.ForeignKey('QrtzTriggers', related_name='QrtzTriggersCronTriggerGroups', db_column='TRIGGER_GROUP')
    cron_expression = models.CharField(db_column='CRON_EXPRESSION', max_length=120)  
    time_zone_id = models.CharField(db_column='TIME_ZONE_ID', max_length=80, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'QRTZ_CRON_TRIGGERS'
        unique_together = (('sched_name', 'trigger_name', 'trigger_group'),)


class QrtzFiredTriggers(models.Model):
    sched_name = models.CharField(db_column='SCHED_NAME', max_length=120)  
    entry_id = models.CharField(db_column='ENTRY_ID', max_length=95)  
    trigger_name = models.CharField(db_column='TRIGGER_NAME', max_length=140)  
    trigger_group = models.CharField(db_column='TRIGGER_GROUP', max_length=50)  
    instance_name = models.CharField(db_column='INSTANCE_NAME', max_length=200)  
    fired_time = models.BigIntegerField(db_column='FIRED_TIME')  
    priority = models.BigIntegerField(db_column='PRIORITY')  
    state = models.CharField(db_column='STATE', max_length=16)  
    job_name = models.CharField(db_column='JOB_NAME', max_length=150, blank=True, null=True)  
    job_group = models.CharField(db_column='JOB_GROUP', max_length=50, blank=True, null=True)  
    is_nonconcurrent = models.CharField(db_column='IS_NONCONCURRENT', max_length=1, blank=True, null=True)  
    requests_recovery = models.CharField(db_column='REQUESTS_RECOVERY', max_length=1, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'QRTZ_FIRED_TRIGGERS'
        unique_together = (('sched_name', 'entry_id'),)


class QrtzJobDetails(models.Model):
    sched_name = models.CharField(db_column='SCHED_NAME', max_length=120)  
    job_name = models.CharField(db_column='JOB_NAME', max_length=150)  
    job_group = models.CharField(db_column='JOB_GROUP', max_length=50)  
    description = models.CharField(db_column='DESCRIPTION', max_length=250, blank=True, null=True)  
    job_class_name = models.CharField(db_column='JOB_CLASS_NAME', max_length=250)  
    is_durable = models.CharField(db_column='IS_DURABLE', max_length=1)  
    is_nonconcurrent = models.CharField(db_column='IS_NONCONCURRENT', max_length=1)  
    is_update_data = models.CharField(db_column='IS_UPDATE_DATA', max_length=1)  
    requests_recovery = models.CharField(db_column='REQUESTS_RECOVERY', max_length=1)  
    job_data = models.TextField(db_column='JOB_DATA', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'QRTZ_JOB_DETAILS'
        unique_together = (('sched_name', 'job_name', 'job_group'),)


class QrtzLocks(models.Model):
    sched_name = models.CharField(db_column='SCHED_NAME', max_length=120)  
    lock_name = models.CharField(db_column='LOCK_NAME', max_length=40)  

    class Meta:
        managed = False
        db_table = 'QRTZ_LOCKS'
        unique_together = (('sched_name', 'lock_name'),)


class QrtzPausedTriggerGrps(models.Model):
    sched_name = models.CharField(db_column='SCHED_NAME', max_length=120)  
    trigger_group = models.CharField(db_column='TRIGGER_GROUP', max_length=200)  

    class Meta:
        managed = False
        db_table = 'QRTZ_PAUSED_TRIGGER_GRPS'
        unique_together = (('sched_name', 'trigger_group'),)


class QrtzSchedulerState(models.Model):
    sched_name = models.CharField(db_column='SCHED_NAME', max_length=120)  
    instance_name = models.CharField(db_column='INSTANCE_NAME', max_length=200)  
    last_checkin_time = models.BigIntegerField(db_column='LAST_CHECKIN_TIME')  
    checkin_interval = models.BigIntegerField(db_column='CHECKIN_INTERVAL')  

    class Meta:
        managed = False
        db_table = 'QRTZ_SCHEDULER_STATE'
        unique_together = (('sched_name', 'instance_name'),)


class QrtzSimpleTriggers(models.Model):
    sched_name = models.ForeignKey('QrtzTriggers', related_name='QrtzTriggersSimpleScheds', db_column='SCHED_NAME')
    trigger_name = models.ForeignKey('QrtzTriggers', related_name='QrtzTriggersSimpleTriggers', db_column='TRIGGER_NAME')
    trigger_group = models.ForeignKey('QrtzTriggers', related_name='QrtzTriggersSimpleTriggerGroups', db_column='TRIGGER_GROUP')
    repeat_count = models.BigIntegerField(db_column='REPEAT_COUNT')  
    repeat_interval = models.BigIntegerField(db_column='REPEAT_INTERVAL')  
    times_triggered = models.BigIntegerField(db_column='TIMES_TRIGGERED')  

    class Meta:
        managed = False
        db_table = 'QRTZ_SIMPLE_TRIGGERS'
        unique_together = (('sched_name', 'trigger_name', 'trigger_group'),)


class QrtzSimpropTriggers(models.Model):
    sched_name = models.ForeignKey('QrtzTriggers', related_name='QrtzTriggersSimpropScheds', db_column='SCHED_NAME')
    trigger_name = models.ForeignKey('QrtzTriggers', related_name='QrtzTriggersSimpropTriggers', db_column='TRIGGER_NAME')
    trigger_group = models.ForeignKey('QrtzTriggers', related_name='QrtzTriggersSimpropTriggerGroups', db_column='TRIGGER_GROUP')
    str_prop_1 = models.CharField(db_column='STR_PROP_1', max_length=512, blank=True, null=True)  
    str_prop_2 = models.CharField(db_column='STR_PROP_2', max_length=512, blank=True, null=True)  
    str_prop_3 = models.CharField(db_column='STR_PROP_3', max_length=512, blank=True, null=True)  
    int_prop_1 = models.BigIntegerField(db_column='INT_PROP_1', blank=True, null=True)  
    int_prop_2 = models.BigIntegerField(db_column='INT_PROP_2', blank=True, null=True)  
    long_prop_1 = models.BigIntegerField(db_column='LONG_PROP_1', blank=True, null=True)  
    long_prop_2 = models.BigIntegerField(db_column='LONG_PROP_2', blank=True, null=True)  
    dec_prop_1 = models.DecimalField(db_column='DEC_PROP_1', max_digits=13, decimal_places=4, blank=True, null=True)  
    dec_prop_2 = models.DecimalField(db_column='DEC_PROP_2', max_digits=13, decimal_places=4, blank=True, null=True)  
    bool_prop_1 = models.CharField(db_column='BOOL_PROP_1', max_length=1, blank=True, null=True)  
    bool_prop_2 = models.CharField(db_column='BOOL_PROP_2', max_length=1, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'QRTZ_SIMPROP_TRIGGERS'
        unique_together = (('sched_name', 'trigger_name', 'trigger_group'),)


class QrtzTriggers(models.Model):
    sched_name = models.ForeignKey(QrtzJobDetails, related_name='qrtztriggers_sched_name_set', db_column='SCHED_NAME')
    trigger_name = models.CharField(db_column='TRIGGER_NAME', max_length=140)  
    trigger_group = models.CharField(db_column='TRIGGER_GROUP', max_length=50)  
    job_name = models.ForeignKey(QrtzJobDetails, related_name='qrtztriggers_job_name_set', db_column='JOB_NAME')
    job_group = models.ForeignKey(QrtzJobDetails, related_name='qrtztriggers_job_group_set', db_column='JOB_GROUP')
    description = models.CharField(db_column='DESCRIPTION', max_length=250, blank=True, null=True)  
    next_fire_time = models.BigIntegerField(db_column='NEXT_FIRE_TIME', blank=True, null=True)  
    prev_fire_time = models.BigIntegerField(db_column='PREV_FIRE_TIME', blank=True, null=True)  
    priority = models.BigIntegerField(db_column='PRIORITY', blank=True, null=True)  
    trigger_state = models.CharField(db_column='TRIGGER_STATE', max_length=16)  
    trigger_type = models.CharField(db_column='TRIGGER_TYPE', max_length=8)  
    start_time = models.BigIntegerField(db_column='START_TIME')  
    end_time = models.BigIntegerField(db_column='END_TIME', blank=True, null=True)  
    calendar_name = models.CharField(db_column='CALENDAR_NAME', max_length=200, blank=True, null=True)  
    misfire_instr = models.SmallIntegerField(db_column='MISFIRE_INSTR', blank=True, null=True)  
    job_data = models.TextField(db_column='JOB_DATA', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'QRTZ_TRIGGERS'
        unique_together = (('sched_name', 'trigger_name', 'trigger_group'),)


class RepLabel(models.Model):
    lbl_id = models.BigIntegerField(db_column='LBL_ID', primary_key=True)  
    lbl_code = models.CharField(db_column='LBL_CODE', max_length=100)  
    lbl_label = models.CharField(db_column='LBL_LABEL', max_length=100)  
    lbl_module = models.CharField(db_column='LBL_MODULE', max_length=100, blank=True, null=True)  
    lbl_category = models.CharField(db_column='LBL_CATEGORY', max_length=100, blank=True, null=True)  
    lbl_comments = models.CharField(db_column='LBL_COMMENTS', max_length=100, blank=True, null=True)  
    lbl_page = models.CharField(db_column='LBL_PAGE', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'REP_LABEL'


class RepLabelLocale(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    lbl_code = models.CharField(db_column='LBL_CODE', max_length=100, blank=True, null=True)  
    lal_value = models.CharField(db_column='LAL_VALUE', max_length=100, blank=True, null=True)  
    lal_locale = models.CharField(db_column='LAL_LOCALE', max_length=20, blank=True, null=True)  
    lal_updated = models.DateTimeField(db_column='LAL_UPDATED', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'REP_LABEL_LOCALE'


class RepLocale(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(db_column='CODE', max_length=20)  
    locale = models.CharField(db_column='LOCALE', max_length=20)  
    active = models.SmallIntegerField(db_column='ACTIVE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'REP_LOCALE'


class RepMsg(models.Model):
    msg_id = models.BigIntegerField(db_column='MSG_ID', primary_key=True)  
    msg_code = models.CharField(db_column='MSG_CODE', max_length=255, blank=True, null=True)  
    msg_desc = models.CharField(db_column='MSG_DESC', max_length=1024, blank=True, null=True)  
    msg_category = models.CharField(db_column='MSG_CATEGORY', max_length=255, blank=True, null=True)  
    msg_page = models.CharField(db_column='MSG_PAGE', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'REP_MSG'


class RepMsgLocale(models.Model):
    msl_id = models.BigIntegerField(db_column='MSL_ID', primary_key=True)  
    msl_value = models.CharField(db_column='MSL_VALUE', max_length=1024, blank=True, null=True)  
    msl_locale = models.CharField(db_column='MSL_LOCALE', max_length=20, blank=True, null=True)  
    msg_code = models.CharField(db_column='MSG_CODE', max_length=100, blank=True, null=True)  
    msl_updated = models.DateTimeField(db_column='MSL_UPDATED', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'REP_MSG_LOCALE'


class SysAcceptIp(models.Model):
    acceptid = models.BigIntegerField(db_column='ACCEPTID', primary_key=True)  
    title = models.CharField(db_column='TITLE', max_length=128, blank=True, null=True)  
    startip = models.CharField(db_column='STARTIP', max_length=20, blank=True, null=True)  
    endip = models.CharField(db_column='ENDIP', max_length=20, blank=True, null=True)  
    remark = models.CharField(db_column='REMARK', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_ACCEPT_IP'


class SysAliasScript(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    alias_name = models.CharField(db_column='ALIAS_NAME', max_length=100, blank=True, null=True)  
    alias_desc = models.CharField(db_column='ALIAS_DESC', max_length=100, blank=True, null=True)  
    class_name = models.CharField(db_column='CLASS_NAME', max_length=400, blank=True, null=True)  
    class_ins_name = models.CharField(db_column='CLASS_INS_NAME', max_length=200, blank=True, null=True)  
    method_name = models.CharField(db_column='METHOD_NAME', max_length=200, blank=True, null=True)  
    method_desc = models.CharField(db_column='METHOD_DESC', max_length=400, blank=True, null=True)  
    script_comten = models.TextField(db_column='SCRIPT_COMTEN', blank=True, null=True)  
    return_type = models.CharField(db_column='RETURN_TYPE', max_length=50, blank=True, null=True)  
    script_type = models.CharField(db_column='SCRIPT_TYPE', max_length=50, blank=True, null=True)  
    argument = models.TextField(db_column='ARGUMENT', blank=True, null=True)  
    enable = models.DecimalField(db_column='ENABLE', max_digits=2, decimal_places=0, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_ALIAS_SCRIPT'


class SysAudit(models.Model):
    auditid = models.BigIntegerField(db_column='AUDITID', primary_key=True)  
    opname = models.CharField(db_column='OPNAME', max_length=128, blank=True, null=True)  
    exetime = models.DateTimeField(db_column='EXETIME', blank=True, null=True)  
    executorid = models.BigIntegerField(db_column='EXECUTORID', blank=True, null=True)  
    executor = models.CharField(db_column='EXECUTOR', max_length=64, blank=True, null=True)  
    fromip = models.CharField(db_column='FROMIP', max_length=64, blank=True, null=True)  
    exemethod = models.CharField(db_column='EXEMETHOD', max_length=128, blank=True, null=True)  
    requesturi = models.CharField(db_column='REQUESTURI', max_length=256, blank=True, null=True)  
    reqparams = models.TextField(db_column='REQPARAMS', blank=True, null=True)  
    ownermodel = models.CharField(db_column='OWNERMODEL', max_length=200, blank=True, null=True)  
    exectype = models.CharField(db_column='EXECTYPE', max_length=200, blank=True, null=True)  
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  
    detail = models.TextField(db_column='DETAIL', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_AUDIT'


class SysAuthRole(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    auth_id = models.BigIntegerField(db_column='AUTH_ID', blank=True, null=True)  
    role_id = models.BigIntegerField(db_column='ROLE_ID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_AUTH_ROLE'


class SysCalendar(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=400, blank=True, null=True)  
    isdefault = models.BigIntegerField(db_column='ISDEFAULT', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_CALENDAR'


class SysCalendarAssign(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    canlendarid = models.BigIntegerField(db_column='CANLENDARID', blank=True, null=True)  
    assigntype = models.SmallIntegerField(db_column='ASSIGNTYPE', blank=True, null=True)  
    assignid = models.BigIntegerField(db_column='ASSIGNID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_CALENDAR_ASSIGN'


class SysCalendarSetting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    calendarid = models.BigIntegerField(db_column='CALENDARID', blank=True, null=True)  
    years = models.SmallIntegerField(db_column='YEARS', blank=True, null=True)  
    months = models.SmallIntegerField(db_column='MONTHS', blank=True, null=True)  
    days = models.SmallIntegerField(db_column='DAYS', blank=True, null=True)  
    type = models.SmallIntegerField(db_column='TYPE', blank=True, null=True)  
    worktimeid = models.BigIntegerField(db_column='WORKTIMEID')  
    calday = models.CharField(db_column='CALDAY', max_length=20, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_CALENDAR_SETTING'


class SysCodeTemplate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    template_name = models.CharField(db_column='TEMPLATE_NAME', max_length=200, blank=True, null=True)  
    html = models.TextField(db_column='HTML', blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  
    template_alias = models.CharField(db_column='TEMPLATE_ALIAS', max_length=200, blank=True, null=True)  
    template_type = models.SmallIntegerField(db_column='TEMPLATE_TYPE', blank=True, null=True)  
    issubneed = models.SmallIntegerField(db_column='ISSUBNEED', blank=True, null=True)  
    filename = models.CharField(db_column='FILENAME', max_length=200, blank=True, null=True)  
    filedir = models.CharField(db_column='FILEDIR', max_length=200, blank=True, null=True)  
    formedit = models.SmallIntegerField(db_column='FORMEDIT', blank=True, null=True)  
    formdetail = models.SmallIntegerField(db_column='FORMDETAIL', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_CODE_TEMPLATE'


class SysConditionScript(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    class_name = models.CharField(db_column='CLASS_NAME', max_length=400, blank=True, null=True)  
    class_ins_name = models.CharField(db_column='CLASS_INS_NAME', max_length=200, blank=True, null=True)  
    method_name = models.CharField(db_column='METHOD_NAME', max_length=200, blank=True, null=True)  
    method_desc = models.CharField(db_column='METHOD_DESC', max_length=400, blank=True, null=True)  
    return_type = models.CharField(db_column='RETURN_TYPE', max_length=50, blank=True, null=True)  
    argument = models.TextField(db_column='ARGUMENT', blank=True, null=True)  
    enable = models.SmallIntegerField(db_column='ENABLE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_CONDITION_SCRIPT'


class SysDatasource2(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    alias = models.CharField(db_column='ALIAS', max_length=20, blank=True, null=True)  
    drivername = models.CharField(db_column='DRIVERNAME', max_length=100, blank=True, null=True)  
    url = models.CharField(db_column='URL', max_length=100, blank=True, null=True)  
    username = models.CharField(db_column='USERNAME', max_length=20, blank=True, null=True)  
    password = models.CharField(db_column='PASSWORD', max_length=20, blank=True, null=True)  
    dbtype = models.CharField(db_column='DBTYPE', max_length=20, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_DATASOURCE'


class SysDataSource(models.Model):
    id_field = models.DecimalField(db_column='ID_', primary_key=True, max_digits=18, decimal_places=0)  
    name_field = models.CharField(db_column='NAME_', max_length=64, blank=True, null=True)  
    alias_field = models.CharField(db_column='ALIAS_', max_length=64, blank=True, null=True)  
    db_type_field = models.CharField(db_column='DB_TYPE_', max_length=64, blank=True, null=True)  
    setting_json_field = models.TextField(db_column='SETTING_JSON_', blank=True, null=True)  
    init_on_start_field = models.SmallIntegerField(db_column='INIT_ON_START_', blank=True, null=True)  
    enabled_field = models.SmallIntegerField(db_column='ENABLED_', blank=True, null=True)  
    class_path_field = models.CharField(db_column='CLASS_PATH_', max_length=128, blank=True, null=True)  
    init_method_field = models.CharField(db_column='INIT_METHOD_', max_length=128, blank=True, null=True)  
    close_method_field = models.CharField(db_column='CLOSE_METHOD_', max_length=128, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_DATA_SOURCE'
        unique_together = (('name_field', 'alias_field'),)


class SysDataSourceDef(models.Model):
    id_field = models.DecimalField(db_column='ID_', primary_key=True, max_digits=18, decimal_places=0)  
    name_field = models.CharField(db_column='NAME_', max_length=64)  
    class_path_field = models.CharField(db_column='CLASS_PATH_', max_length=128)  
    setting_json_field = models.TextField(db_column='SETTING_JSON_', blank=True, null=True)  
    init_method_field = models.CharField(db_column='INIT_METHOD_', max_length=64, blank=True, null=True)  
    is_system_field = models.SmallIntegerField(db_column='IS_SYSTEM_', blank=True, null=True)  
    close_method_field = models.CharField(db_column='CLOSE_METHOD_', max_length=64, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_DATA_SOURCE_DEF'
        unique_together = (('class_path_field', 'name_field'),)


class SysDbId(models.Model):
    id = models.SmallIntegerField(db_column='ID', primary_key=True)  
    incremental = models.BigIntegerField(db_column='INCREMENTAL', blank=True, null=True)  
    bound = models.BigIntegerField(db_column='BOUND', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_DB_ID'


class SysDemension(models.Model):
    demid = models.BigIntegerField(db_column='DEMID', primary_key=True)  
    demname = models.CharField(db_column='DEMNAME', max_length=128)  
    demdesc = models.CharField(db_column='DEMDESC', max_length=1024, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_DEMENSION'


class SysDesktopColumn(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    servicemethod = models.CharField(db_column='SERVICEMETHOD', max_length=50, blank=True, null=True)  
    templatename = models.CharField(db_column='TEMPLATENAME', max_length=50, blank=True, null=True)  
    templateid = models.CharField(db_column='TEMPLATEID', max_length=20, blank=True, null=True)  
    templatepath = models.CharField(db_column='TEMPLATEPATH', max_length=200, blank=True, null=True)  
    columnurl = models.CharField(db_column='COLUMNURL', max_length=200, blank=True, null=True)  
    html = models.TextField(db_column='HTML', blank=True, null=True)  
    issys = models.SmallIntegerField(db_column='ISSYS', blank=True, null=True)  
    methodtype = models.SmallIntegerField(db_column='METHODTYPE', blank=True, null=True)  
    queryalias = models.CharField(db_column='QUERYALIAS', max_length=100, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_DESKTOP_COLUMN'


class SysDesktopLayout(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    cols = models.SmallIntegerField(db_column='COLS', blank=True, null=True)  
    width = models.CharField(db_column='WIDTH', max_length=50, blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=100, blank=True, null=True)  
    isdefault = models.BigIntegerField(db_column='ISDEFAULT', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_DESKTOP_LAYOUT'


class SysDesktopLayoutcol(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    layoutid = models.BigIntegerField(db_column='LAYOUTID', blank=True, null=True)  
    columnid = models.BigIntegerField(db_column='COLUMNID', blank=True, null=True)  
    col = models.BigIntegerField(db_column='COL', blank=True, null=True)  
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_DESKTOP_LAYOUTCOL'


class SysDesktopMycolumn(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    layoutid = models.BigIntegerField(db_column='LAYOUTID', blank=True, null=True)  
    columnid = models.BigIntegerField(db_column='COLUMNID', blank=True, null=True)  
    col = models.SmallIntegerField(db_column='COL', blank=True, null=True)  
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  
    columnname = models.CharField(db_column='COLUMNNAME', max_length=100, blank=True, null=True)  
    servicemethod = models.CharField(db_column='SERVICEMETHOD', max_length=400, blank=True, null=True)  
    columnhtml = models.CharField(db_column='COLUMNHTML', max_length=200, blank=True, null=True)  
    columnurl = models.CharField(db_column='COLUMNURL', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_DESKTOP_MYCOLUMN'


class SysDic(models.Model):
    dicid = models.BigIntegerField(db_column='DICID', primary_key=True)  
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  
    itemkey = models.CharField(db_column='ITEMKEY', max_length=64, blank=True, null=True)  
    itemname = models.CharField(db_column='ITEMNAME', max_length=64)  
    itemvalue = models.CharField(db_column='ITEMVALUE', max_length=128)  
    descp = models.CharField(db_column='DESCP', max_length=256, blank=True, null=True)  
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  
    nodepath = models.CharField(db_column='NODEPATH', max_length=100, blank=True, null=True)  
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_DIC'


class SysErrorLog(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    hashcode = models.CharField(db_column='HASHCODE', max_length=40, blank=True, null=True)  
    account = models.CharField(db_column='ACCOUNT', max_length=50, blank=True, null=True)  
    ip = models.CharField(db_column='IP', max_length=30, blank=True, null=True)  
    errorurl = models.CharField(db_column='ERRORURL', max_length=2000, blank=True, null=True)  
    error = models.TextField(db_column='ERROR', blank=True, null=True)  
    errordate = models.DateTimeField(db_column='ERRORDATE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_ERROR_LOG'


class SysExcelImprule(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    table_name = models.CharField(db_column='TABLE_NAME', max_length=30, blank=True, null=True)  
    column_str = models.CharField(db_column='COLUMN_STR', max_length=200, blank=True, null=True)  
    mark = models.CharField(db_column='MARK', max_length=200, blank=True, null=True)  
    imp_type = models.SmallIntegerField(db_column='IMP_TYPE', blank=True, null=True)  
    busi_date = models.DateTimeField(db_column='BUSI_DATE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_EXCEL_IMPRULE'


class SysFile(models.Model):
    fileid = models.CharField(db_column='FILEID', primary_key=True, max_length=80)  
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  
    filename = models.CharField(db_column='FILENAME', max_length=128)  
    filepath = models.CharField(db_column='FILEPATH', max_length=128)  
    createtime = models.DateTimeField(db_column='CREATETIME')  
    ext = models.CharField(db_column='EXT', max_length=32, blank=True, null=True)  
    filetype = models.CharField(db_column='FILETYPE', max_length=32)  
    note = models.CharField(db_column='NOTE', max_length=1024, blank=True, null=True)  
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  
    creator = models.CharField(db_column='CREATOR', max_length=32)  
    totalbytes = models.BigIntegerField(db_column='TOTALBYTES', blank=True, null=True)  
    delflag = models.SmallIntegerField(db_column='DELFLAG', blank=True, null=True)  
    fileblob = models.TextField(db_column='FILEBLOB', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_FILE'


class SysGlType(models.Model):
    typeid = models.BigIntegerField(db_column='TYPEID', primary_key=True)  
    typename = models.CharField(db_column='TYPENAME', max_length=128)  
    nodepath = models.CharField(db_column='NODEPATH', max_length=200, blank=True, null=True)  
    depth = models.BigIntegerField(db_column='DEPTH')  
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  
    catkey = models.CharField(db_column='CATKEY', max_length=64, blank=True, null=True)  
    nodekey = models.CharField(db_column='NODEKEY', max_length=64)  
    sn = models.BigIntegerField(db_column='SN')  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    depid = models.BigIntegerField(db_column='DEPID', blank=True, null=True)  
    type = models.BigIntegerField(db_column='TYPE', blank=True, null=True)  
    isleaf = models.SmallIntegerField(db_column='ISLEAF', blank=True, null=True)  
    nodecode = models.CharField(db_column='NODECODE', max_length=20, blank=True, null=True)  
    nodecodetype = models.SmallIntegerField(db_column='NODECODETYPE', blank=True, null=True)  
    datasources = models.IntegerField(db_column='dataSources', blank=True, null=True)  
    custdata = models.CharField(db_column='custData', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_GL_TYPE'


class SysIdentity(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    alias = models.CharField(db_column='ALIAS', max_length=20, blank=True, null=True)  
    regulation = models.CharField(db_column='REGULATION', max_length=100, blank=True, null=True)  
    gentype = models.SmallIntegerField(db_column='GENTYPE', blank=True, null=True)  
    nolength = models.BigIntegerField(db_column='NOLENGTH', blank=True, null=True)  
    curdate = models.CharField(db_column='CURDATE', max_length=10, blank=True, null=True)  
    initvalue = models.BigIntegerField(db_column='INITVALUE', blank=True, null=True)  
    curvalue = models.BigIntegerField(db_column='CURVALUE', blank=True, null=True)  
    step = models.SmallIntegerField(db_column='STEP', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_IDENTITY'


class SysJob(models.Model):
    jobid = models.BigIntegerField(db_column='JOBID', primary_key=True)  
    jobname = models.CharField(db_column='JOBNAME', max_length=100, blank=True, null=True)  
    jobcode = models.CharField(db_column='JOBCODE', max_length=100, blank=True, null=True)  
    jobdesc = models.CharField(db_column='JOBDESC', max_length=400, blank=True, null=True)  
    setid = models.BigIntegerField(db_column='SETID', blank=True, null=True)  
    isdelete = models.BigIntegerField(db_column='ISDELETE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_JOB'


class SysJoblog(models.Model):
    logid = models.BigIntegerField(db_column='LOGID', primary_key=True)  
    jobname = models.CharField(db_column='JOBNAME', max_length=50, blank=True, null=True)  
    trigname = models.CharField(db_column='TRIGNAME', max_length=50, blank=True, null=True)  
    starttime = models.DateTimeField(db_column='STARTTIME', blank=True, null=True)  
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  
    content = models.TextField(db_column='CONTENT', blank=True, null=True)  
    state = models.BigIntegerField(db_column='STATE', blank=True, null=True)  
    runtime = models.BigIntegerField(db_column='RUNTIME', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_JOBLOG'


class SysLogSwitch(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    model = models.CharField(db_column='MODEL', max_length=50, blank=True, null=True)  
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME')  
    creator = models.CharField(db_column='CREATOR', max_length=20, blank=True, null=True)  
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  
    updby = models.CharField(db_column='UPDBY', max_length=20, blank=True, null=True)  
    updbyid = models.BigIntegerField(db_column='UPDBYID', blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=300, blank=True, null=True)  
    lastuptime = models.DateTimeField(db_column='LASTUPTIME')  

    class Meta:
        managed = False
        db_table = 'SYS_LOG_SWITCH'


class SysMessageLog(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    subject = models.CharField(db_column='SUBJECT', max_length=100, blank=True, null=True)  
    sendtime = models.DateTimeField(db_column='SENDTIME', blank=True, null=True)  
    receiver = models.CharField(db_column='RECEIVER', max_length=1000, blank=True, null=True)  
    messagetype = models.BigIntegerField(db_column='MESSAGETYPE', blank=True, null=True)  
    state = models.BigIntegerField(db_column='STATE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_MESSAGE_LOG'


class SysMsgRead(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    messageid = models.BigIntegerField(db_column='MESSAGEID', blank=True, null=True)  
    receiverid = models.BigIntegerField(db_column='RECEIVERID', blank=True, null=True)  
    receiver = models.CharField(db_column='RECEIVER', max_length=20, blank=True, null=True)  
    receivetime = models.DateTimeField(db_column='RECEIVETIME', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_MSG_READ'


class SysMsgReceiver(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    messageid = models.BigIntegerField(db_column='MESSAGEID', blank=True, null=True)  
    receivetype = models.SmallIntegerField(db_column='RECEIVETYPE', blank=True, null=True)  
    receiverid = models.BigIntegerField(db_column='RECEIVERID', blank=True, null=True)  
    receiver = models.CharField(db_column='RECEIVER', max_length=20, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_MSG_RECEIVER'


class SysMsgReply(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    messageid = models.BigIntegerField(db_column='MESSAGEID', blank=True, null=True)  
    content = models.TextField(db_column='CONTENT', blank=True, null=True)  
    replyid = models.BigIntegerField(db_column='REPLYID', blank=True, null=True)  
    reply = models.CharField(db_column='REPLY', max_length=20, blank=True, null=True)  
    replytime = models.DateTimeField(db_column='REPLYTIME', blank=True, null=True)  
    isprivate = models.SmallIntegerField(db_column='ISPRIVATE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_MSG_REPLY'


class SysMsgSend(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    subject = models.CharField(db_column='SUBJECT', max_length=100, blank=True, null=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    username = models.CharField(db_column='USERNAME', max_length=20, blank=True, null=True)  
    messagetype = models.CharField(db_column='MESSAGETYPE', max_length=50, blank=True, null=True)  
    content = models.TextField(db_column='CONTENT', blank=True, null=True)  
    sendtime = models.DateTimeField(db_column='SENDTIME', blank=True, null=True)  
    canreply = models.SmallIntegerField(db_column='CANREPLY', blank=True, null=True)  
    receivername = models.TextField(db_column='RECEIVERNAME', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_MSG_SEND'


class SysOfficeTemplate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    subject = models.CharField(db_column='SUBJECT', max_length=20, blank=True, null=True)  
    templatetype = models.BigIntegerField(db_column='TEMPLATETYPE', blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  
    creator = models.CharField(db_column='CREATOR', max_length=20, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  
    path = models.CharField(db_column='PATH', max_length=200, blank=True, null=True)  
    templateblob = models.TextField(db_column='TEMPLATEBLOB', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_OFFICE_TEMPLATE'


class SysOrg(models.Model):
    orgid = models.BigIntegerField(db_column='ORGID', primary_key=True)  
    demid = models.BigIntegerField(db_column='DEMID', blank=True, null=True)  
    orgname = models.CharField(db_column='ORGNAME', max_length=128)  
    orgdesc = models.CharField(db_column='ORGDESC', max_length=500, blank=True, null=True)  
    orgsupid = models.BigIntegerField(db_column='ORGSUPID', blank=True, null=True)  
    path = models.CharField(db_column='PATH', max_length=128, blank=True, null=True)  
    depth = models.BigIntegerField(db_column='DEPTH', blank=True, null=True)  
    orgtype = models.BigIntegerField(db_column='ORGTYPE', blank=True, null=True)  
    creatorid = models.BigIntegerField(db_column='CREATORID', blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  
    updateid = models.BigIntegerField(db_column='UPDATEID', blank=True, null=True)  
    updatetime = models.DateTimeField(db_column='UPDATETIME', blank=True, null=True)  
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  
    fromtype = models.SmallIntegerField(db_column='FROMTYPE', blank=True, null=True)  
    orgpathname = models.CharField(db_column='ORGPATHNAME', max_length=2000, blank=True, null=True)  
    isdelete = models.NullBooleanField(db_column='ISDELETE', blank=True, null=True)
    code = models.CharField(db_column='CODE', max_length=128, blank=True, null=True)
    members = models.ManyToManyField('SysUser', through='SysUserOrg', through_fields=('orgid', 'userid'))

    objects = EboaManager()

    class Meta:
        managed = False
        db_table = 'SYS_ORG'
        verbose_name = verbose_name_plural = u"組織"

    def __unicode__(self):
        return self.orgname


class SysOrgAuth(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    user_id = models.BigIntegerField(db_column='USER_ID')  
    org_id = models.BigIntegerField(db_column='ORG_ID')  
    dim_id = models.BigIntegerField(db_column='DIM_ID')  
    org_perms = models.CharField(db_column='ORG_PERMS', max_length=255, blank=True, null=True)  
    user_perms = models.CharField(db_column='USER_PERMS', max_length=255, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_ORG_AUTH'


class SysOrgParam(models.Model):
    valueid = models.BigIntegerField(db_column='VALUEID', blank=True, null=True)  
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  
    paramid = models.BigIntegerField(db_column='PARAMID', blank=True, null=True)  
    paramvalue = models.CharField(db_column='PARAMVALUE', max_length=200, blank=True, null=True)  
    paramdatevalue = models.DateTimeField(db_column='PARAMDATEVALUE', blank=True, null=True)  
    paramintvalue = models.DecimalField(db_column='PARAMINTVALUE', max_digits=18, decimal_places=2, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_ORG_PARAM'


class SysOrgRole(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  
    roleid = models.BigIntegerField(db_column='ROLEID', blank=True, null=True)  
    candel = models.SmallIntegerField(db_column='CANDEL', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_ORG_ROLE'


class SysOrgRolemanage(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  
    roleid = models.BigIntegerField(db_column='ROLEID', blank=True, null=True)  
    candel = models.SmallIntegerField(db_column='CANDEL', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_ORG_ROLEMANAGE'


class SysOrgType(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    demid = models.BigIntegerField(db_column='DEMID', blank=True, null=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    levels = models.SmallIntegerField(db_column='LEVELS', blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=100, blank=True, null=True)  
    icon = models.CharField(db_column='ICON', max_length=100, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_ORG_TYPE'


class SysOvertime(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    subject = models.CharField(db_column='SUBJECT', max_length=50, blank=True, null=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    starttime = models.DateTimeField(db_column='STARTTIME', blank=True, null=True)  
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  
    worktype = models.SmallIntegerField(db_column='WORKTYPE', blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_OVERTIME'


class SysParam(models.Model):
    paramid = models.BigIntegerField(db_column='PARAMID', primary_key=True)  
    paramkey = models.CharField(db_column='PARAMKEY', max_length=32, blank=True, null=True)  
    paramname = models.CharField(db_column='PARAMNAME', max_length=50, blank=True, null=True)  
    datatype = models.CharField(db_column='DATATYPE', max_length=20, blank=True, null=True)  
    effect = models.SmallIntegerField(db_column='EFFECT', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_PARAM'


class SysPaur(models.Model):
    paurid = models.BigIntegerField(db_column='PAURID', primary_key=True)  
    paurname = models.CharField(db_column='PAURNAME', max_length=30, blank=True, null=True)  
    aliasname = models.CharField(db_column='ALIASNAME', max_length=30, blank=True, null=True)  
    paurvalue = models.CharField(db_column='PAURVALUE', max_length=50, blank=True, null=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_PAUR'


class SysPersonScript(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    class_name = models.CharField(db_column='CLASS_NAME', max_length=200, blank=True, null=True)  
    class_ins_name = models.CharField(db_column='CLASS_INS_NAME', max_length=400, blank=True, null=True)  
    method_name = models.CharField(db_column='METHOD_NAME', max_length=200, blank=True, null=True)  
    method_desc = models.CharField(db_column='METHOD_DESC', max_length=200, blank=True, null=True)  
    return_type = models.CharField(db_column='RETURN_TYPE', max_length=200, blank=True, null=True)  
    argument = models.CharField(db_column='ARGUMENT', max_length=200, blank=True, null=True)  
    enable = models.DecimalField(db_column='ENABLE', max_digits=1, decimal_places=0, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_PERSON_SCRIPT'


class SysPos(models.Model):
    posid = models.BigIntegerField(db_column='POSID', primary_key=True)  
    posname = models.CharField(db_column='POSNAME', max_length=100)  
    posdesc = models.CharField(db_column='POSDESC', max_length=200, blank=True, null=True)  
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  
    jobid = models.BigIntegerField(db_column='JOBID', blank=True, null=True)  
    isdelete = models.IntegerField(db_column='ISDELETE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_POS'


class SysPosition(models.Model):
    posid = models.BigIntegerField(db_column='POSID', primary_key=True)  
    posname = models.CharField(db_column='POSNAME', max_length=128)  
    posdesc = models.CharField(db_column='POSDESC', max_length=1024, blank=True, null=True)  
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  
    nodepath = models.CharField(db_column='NODEPATH', max_length=256, blank=True, null=True)  
    depth = models.IntegerField(db_column='DEPTH', blank=True, null=True)  
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  
    isleaf = models.SmallIntegerField(db_column='ISLEAF', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_POSITION'


class SysPosSub(models.Model):
    mainpositionid = models.BigIntegerField(db_column='MAINPOSITIONID')  
    subpositionid = models.BigIntegerField(db_column='SUBPOSITIONID')  

    class Meta:
        managed = False
        db_table = 'SYS_POS_SUB'
        unique_together = (('mainpositionid', 'subpositionid'),)


class SysProfile(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    homepage = models.CharField(db_column='HOMEPAGE', max_length=50, blank=True, null=True)  
    skin = models.CharField(db_column='SKIN', max_length=20, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_PROFILE'


class SysQueryField(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    sql_id = models.BigIntegerField(db_column='SQL_ID')  
    name = models.CharField(db_column='NAME', max_length=200, blank=True, null=True)  
    type = models.CharField(db_column='TYPE', max_length=50, blank=True, null=True)  
    field_desc = models.CharField(db_column='FIELD_DESC', max_length=2000, blank=True, null=True)  
    is_show = models.IntegerField(db_column='IS_SHOW', blank=True, null=True)  
    is_search = models.IntegerField(db_column='IS_SEARCH', blank=True, null=True)  
    control_type = models.IntegerField(db_column='CONTROL_TYPE', blank=True, null=True)  
    control_content = models.CharField(db_column='CONTROL_CONTENT', max_length=200, blank=True, null=True)  
    format = models.CharField(db_column='FORMAT', max_length=400, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_QUERY_FIELD'


class SysQuerySetting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    sql_id = models.BigIntegerField(db_column='SQL_ID', blank=True, null=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    alias = models.CharField(db_column='ALIAS', max_length=50, blank=True, null=True)  
    style = models.IntegerField(db_column='STYLE', blank=True, null=True)  
    need_page = models.IntegerField(db_column='NEED_PAGE', blank=True, null=True)  
    page_size = models.IntegerField(db_column='PAGE_SIZE', blank=True, null=True)  
    is_query = models.IntegerField(db_column='IS_QUERY', blank=True, null=True)  
    template_alias = models.CharField(db_column='TEMPLATE_ALIAS', max_length=50, blank=True, null=True)  
    template_html = models.TextField(db_column='TEMPLATE_HTML', blank=True, null=True)  
    display_field = models.TextField(db_column='DISPLAY_FIELD', blank=True, null=True)  
    filter_field = models.TextField(db_column='FILTER_FIELD', blank=True, null=True)  
    condition_field = models.TextField(db_column='CONDITION_FIELD', blank=True, null=True)  
    sort_field = models.TextField(db_column='SORT_FIELD', blank=True, null=True)  
    export_field = models.TextField(db_column='EXPORT_FIELD', blank=True, null=True)  
    manage_field = models.TextField(db_column='MANAGE_FIELD', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_QUERY_SETTING'


class SysQuerySql(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    sql_field = models.CharField(db_column='SQL_', max_length=2000, blank=True, null=True)  
    name = models.CharField(db_column='NAME', max_length=2000, blank=True, null=True)  
    dsalias = models.CharField(db_column='DSALIAS', max_length=2000, blank=True, null=True)  
    url_params = models.CharField(db_column='URL_PARAMS', max_length=2000, blank=True, null=True)  
    categoryid = models.BigIntegerField(db_column='CATEGORYID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_QUERY_SQL'


class SysReport(models.Model):
    reportid = models.BigIntegerField(db_column='REPORTID', primary_key=True)  
    title = models.CharField(db_column='TITLE', max_length=128, blank=True, null=True)  
    descp = models.CharField(db_column='DESCP', max_length=200, blank=True, null=True)  
    filepath = models.CharField(db_column='FILEPATH', max_length=128, blank=True, null=True)  
    filename = models.CharField(db_column='FILENAME', max_length=128, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME')  
    status = models.DecimalField(db_column='STATUS', max_digits=1, decimal_places=0, blank=True, null=True)  
    dsname = models.CharField(db_column='DSNAME', max_length=50, blank=True, null=True)  
    params = models.CharField(db_column='PARAMS', max_length=500, blank=True, null=True)  
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  
    ext = models.CharField(db_column='EXT', max_length=20, blank=True, null=True)  
    realsql = models.TextField(db_column='REALSQL', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_REPORT'


class SysReportTemplate(models.Model):
    reportid = models.BigIntegerField(db_column='REPORTID', primary_key=True)  
    title = models.CharField(db_column='TITLE', max_length=128)  
    descp = models.CharField(db_column='DESCP', max_length=500)  
    reportlocation = models.CharField(db_column='REPORTLOCATION', max_length=128)  
    createtime = models.DateTimeField(db_column='CREATETIME')  
    updatetime = models.DateTimeField(db_column='UPDATETIME')  
    reportkey = models.CharField(db_column='REPORTKEY', max_length=128, blank=True, null=True)  
    isdefaultin = models.SmallIntegerField(db_column='ISDEFAULTIN', blank=True, null=True)  
    typeid = models.BigIntegerField(db_column='TYPEID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_REPORT_TEMPLATE'


class SysRes(models.Model):
    resid = models.BigIntegerField(db_column='RESID', primary_key=True)  
    resname = models.CharField(db_column='RESNAME', max_length=128)  
    alias = models.CharField(db_column='ALIAS', max_length=128, blank=True, null=True)  
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  
    icon = models.CharField(db_column='ICON', max_length=100, blank=True, null=True)  
    parentid = models.BigIntegerField(db_column='PARENTID', blank=True, null=True)  
    defaulturl = models.CharField(db_column='DEFAULTURL', max_length=256, blank=True, null=True)  
    isfolder = models.SmallIntegerField(db_column='ISFOLDER', blank=True, null=True)  
    isdisplayinmenu = models.SmallIntegerField(db_column='ISDISPLAYINMENU', blank=True, null=True)  
    isopen = models.SmallIntegerField(db_column='ISOPEN', blank=True, null=True)  
    systemid = models.BigIntegerField(db_column='SYSTEMID', blank=True, null=True)  
    path = models.CharField(db_column='PATH', max_length=500, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_RES'


class SysResurl(models.Model):
    resurlid = models.BigIntegerField(db_column='RESURLID', primary_key=True)  
    resid = models.BigIntegerField(db_column='RESID', blank=True, null=True)  
    name = models.CharField(db_column='NAME', max_length=100, blank=True, null=True)  
    url = models.CharField(db_column='URL', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_RESURL'


class SysRole(models.Model):
    roleid = models.BigIntegerField(db_column='ROLEID', primary_key=True)  
    systemid = models.BigIntegerField(db_column='SYSTEMID', blank=True, null=True)  
    alias = models.CharField(db_column='ALIAS', max_length=128, blank=True, null=True)  
    rolename = models.CharField(db_column='ROLENAME', max_length=128)  
    memo = models.CharField(db_column='MEMO', max_length=256, blank=True, null=True)  
    allowdel = models.SmallIntegerField(db_column='ALLOWDEL', blank=True, null=True)  
    allowedit = models.SmallIntegerField(db_column='ALLOWEDIT', blank=True, null=True)  
    enabled = models.SmallIntegerField(db_column='ENABLED', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_ROLE'


class SysRolePos(models.Model):
    posid = models.BigIntegerField(db_column='POSID')  
    roleid = models.BigIntegerField(db_column='ROLEID')  

    class Meta:
        managed = False
        db_table = 'SYS_ROLE_POS'
        unique_together = (('posid', 'roleid'),)


class SysRoleRes(models.Model):
    roleresid = models.BigIntegerField(db_column='ROLERESID', primary_key=True)  
    roleid = models.BigIntegerField(db_column='ROLEID', blank=True, null=True)  
    resid = models.BigIntegerField(db_column='RESID', blank=True, null=True)  
    systemid = models.BigIntegerField(db_column='SYSTEMID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_ROLE_RES'


class SysScript(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    script = models.TextField(db_column='SCRIPT', blank=True, null=True)  
    category = models.CharField(db_column='CATEGORY', max_length=50, blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_SCRIPT'


class SysSeal(models.Model):
    sealid = models.BigIntegerField(db_column='SEALID', primary_key=True)  
    sealname = models.CharField(db_column='SEALNAME', max_length=128, blank=True, null=True)  
    sealpath = models.CharField(db_column='SEALPATH', max_length=128, blank=True, null=True)  
    belongid = models.BigIntegerField(db_column='BELONGID', blank=True, null=True)  
    belongname = models.CharField(db_column='BELONGNAME', max_length=128, blank=True, null=True)  
    attachmentid = models.CharField(db_column='ATTACHMENTID', max_length=80, blank=True, null=True)  
    showimageid = models.CharField(db_column='SHOWIMAGEID', max_length=80, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_SEAL'


class SysSealRight(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    sealid = models.BigIntegerField(db_column='SEALID', blank=True, null=True)  
    righttype = models.CharField(db_column='RIGHTTYPE', max_length=20, blank=True, null=True)  
    rightid = models.BigIntegerField(db_column='RIGHTID', blank=True, null=True)  
    rightname = models.CharField(db_column='RIGHTNAME', max_length=100, blank=True, null=True)  
    createuser = models.CharField(db_column='CREATEUSER', max_length=20, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME')  
    controltype = models.SmallIntegerField(db_column='CONTROLTYPE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_SEAL_RIGHT'


class SysSubsystem(models.Model):
    systemid = models.BigIntegerField(db_column='SYSTEMID', primary_key=True)  
    sysname = models.CharField(db_column='SYSNAME', max_length=50)  
    alias = models.CharField(db_column='ALIAS', max_length=20, blank=True, null=True)  
    logo = models.CharField(db_column='LOGO', max_length=100, blank=True, null=True)  
    defaulturl = models.CharField(db_column='DEFAULTURL', max_length=50, blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  
    creator = models.CharField(db_column='CREATOR', max_length=20, blank=True, null=True)  
    allowdel = models.SmallIntegerField(db_column='ALLOWDEL', blank=True, null=True)  
    needorg = models.SmallIntegerField(db_column='NEEDORG', blank=True, null=True)  
    isactive = models.SmallIntegerField(db_column='ISACTIVE', blank=True, null=True)  
    islocal = models.SmallIntegerField(db_column='ISLOCAL', blank=True, null=True)  
    homepage = models.CharField(db_column='HOMEPAGE', max_length=256, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_SUBSYSTEM'


class SysTemplate(models.Model):
    templateid = models.BigIntegerField(db_column='TEMPLATEID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    isdefault = models.SmallIntegerField(db_column='ISDEFAULT', blank=True, null=True)  
    usetype = models.SmallIntegerField(db_column='USETYPE', blank=True, null=True)  
    title = models.CharField(db_column='TITLE', max_length=200, blank=True, null=True)  
    plaincontent = models.CharField(db_column='PLAINCONTENT', max_length=500, blank=True, null=True)  
    htmlcontent = models.CharField(db_column='HTMLCONTENT', max_length=500, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_TEMPLATE'


class SysTypeKey(models.Model):
    typeid = models.BigIntegerField(db_column='TYPEID', primary_key=True)  
    typekey = models.CharField(db_column='TYPEKEY', max_length=64)  
    typename = models.CharField(db_column='TYPENAME', max_length=128, blank=True, null=True)  
    flag = models.BigIntegerField(db_column='FLAG', blank=True, null=True)  
    sn = models.BigIntegerField(db_column='SN', blank=True, null=True)  
    type = models.BigIntegerField(db_column='TYPE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_TYPE_KEY'


class SysUrlPermission(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  
    descp_field = models.CharField(db_column='DESCP_', max_length=200, blank=True, null=True)  
    url_field = models.CharField(db_column='URL_', max_length=2000, blank=True, null=True)  
    params_field = models.CharField(db_column='PARAMS_', max_length=500, blank=True, null=True)  
    enable_field = models.SmallIntegerField(db_column='ENABLE_', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_URL_PERMISSION'


class SysUrlRules(models.Model):
    id_field = models.BigIntegerField(db_column='ID_', primary_key=True)  
    script_field = models.TextField(db_column='SCRIPT_', blank=True, null=True)  
    enable_field = models.SmallIntegerField(db_column='ENABLE_', blank=True, null=True)  
    sys_url_id_field = models.BigIntegerField(db_column='SYS_URL_ID_', blank=True, null=True)  
    descp_field = models.CharField(db_column='DESCP_', max_length=500, blank=True, null=True)  
    sort_field = models.SmallIntegerField(db_column='SORT_', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_URL_RULES'


class SysUser(models.Model):
    userid = models.BigIntegerField(db_column='USERID', primary_key=True)  
    fullname = models.CharField(db_column='FULLNAME', max_length=127, blank=True, null=True)  
    account = models.CharField(db_column='ACCOUNT', max_length=20)  
    password = models.CharField(db_column='PASSWORD', editable=False, max_length=50)
    isexpired = models.SmallIntegerField(db_column='ISEXPIRED', blank=True, null=True)  
    islock = models.SmallIntegerField(db_column='ISLOCK', blank=True, null=True)  
    createtime = models.DateTimeField(db_column='CREATETIME', blank=True, null=True)  
    status = models.SmallIntegerField(db_column='STATUS', blank=True, null=True)  
    email = models.CharField(db_column='EMAIL', max_length=128, blank=True, null=True)  
    mobile = models.CharField(db_column='MOBILE', max_length=32, blank=True, null=True)  
    phone = models.CharField(db_column='PHONE', max_length=32, blank=True, null=True)  
    sex = models.CharField(db_column='SEX', max_length=2, blank=True, null=True)  
    picture = models.CharField(db_column='PICTURE', max_length=300, blank=True, null=True)  
    fromtype = models.SmallIntegerField(db_column='FROMTYPE', blank=True, null=True)

    objects = EboaManager()

    class Meta:
        managed = False
        db_table = 'SYS_USER'

    def __unicode__(self):
        return self.fullname

    def get_section(self):
        orgs = self.sysorg_set.all()
        if orgs.count() > 0:
            return orgs[0]

        return None


class SysUserOrg(models.Model):
    userorgid = models.BigIntegerField(db_column='USERORGID', primary_key=True)
    orgid = models.ForeignKey(SysOrg, db_column='ORGID', blank=True, null=True)
    userid = models.ForeignKey(SysUser, db_column='USERID', blank=True, null=True)
    isprimary = models.SmallIntegerField(db_column='ISPRIMARY')  
    ischarge = models.BigIntegerField(db_column='ISCHARGE', blank=True, null=True)  
    isgrademanage = models.SmallIntegerField(db_column='ISGRADEMANAGE', blank=True, null=True)  
    isdelete = models.NullBooleanField(db_column='ISDELETE', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SYS_USER_ORG'


class SysUserParam(models.Model):
    valueid = models.BigIntegerField(db_column='VALUEID', primary_key=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    paramid = models.BigIntegerField(db_column='PARAMID', blank=True, null=True)  
    paramvalue = models.CharField(db_column='PARAMVALUE', max_length=200, blank=True, null=True)  
    paramdatevalue = models.DateTimeField(db_column='PARAMDATEVALUE', blank=True, null=True)  
    paramintvalue = models.BigIntegerField(db_column='PARAMINTVALUE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_USER_PARAM'


class SysUserPos(models.Model):
    userposid = models.BigIntegerField(db_column='USERPOSID', primary_key=True)  
    posid = models.BigIntegerField(db_column='POSID', blank=True, null=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    isprimary = models.SmallIntegerField(db_column='ISPRIMARY', blank=True, null=True)  
    orgid = models.BigIntegerField(db_column='ORGID', blank=True, null=True)  
    jobid = models.BigIntegerField(db_column='JOBID', blank=True, null=True)  
    ischarge = models.SmallIntegerField(db_column='ISCHARGE', blank=True, null=True)  
    isdelete = models.SmallIntegerField(db_column='ISDELETE', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_USER_POS'


class SysUserRole(models.Model):
    userroleid = models.BigIntegerField(db_column='USERROLEID', primary_key=True)  
    roleid = models.BigIntegerField(db_column='ROLEID', blank=True, null=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_USER_ROLE'


class SysUserUnder(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    userid = models.BigIntegerField(db_column='USERID', blank=True, null=True)  
    underuserid = models.BigIntegerField(db_column='UNDERUSERID', blank=True, null=True)  
    underusername = models.CharField(db_column='UNDERUSERNAME', max_length=50, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_USER_UNDER'


class SysVacation(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    years = models.SmallIntegerField(db_column='YEARS', blank=True, null=True)  
    stattime = models.DateTimeField(db_column='STATTIME', blank=True, null=True)  
    endtime = models.DateTimeField(db_column='ENDTIME', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_VACATION'


class SysWorktime(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    settingid = models.BigIntegerField(db_column='SETTINGID', blank=True, null=True)  
    starttime = models.CharField(db_column='STARTTIME', max_length=10, blank=True, null=True)  
    endtime = models.CharField(db_column='ENDTIME', max_length=10, blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_WORKTIME'


class SysWorktimeSetting(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_WORKTIME_SETTING'


class SysWsDataTemplate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=500, blank=True, null=True)  
    serviceid = models.BigIntegerField(db_column='SERVICEID', blank=True, null=True)  
    template = models.TextField(db_column='TEMPLATE', blank=True, null=True)  
    script = models.TextField(db_column='SCRIPT', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'SYS_WS_DATA_TEMPLATE'


class ApplyCompaign(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    apply_no = models.CharField(max_length=50, blank=True, null=True)
    apply_person = models.CharField(max_length=2000, blank=True, null=True)
    apply_personid = models.CharField(db_column='apply_personID', max_length=2000, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
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
    sqzid = models.CharField(db_column='sqzID', max_length=20, blank=True, null=True)  
    zdssexcel = models.CharField(db_column='zdssExcel', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'apply_form'


class CompaignDepts(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    dept = models.CharField(max_length=2000, blank=True, null=True)
    deptid = models.CharField(db_column='deptID', max_length=2000, blank=True, null=True)  
    xzsm = models.CharField(max_length=200, blank=True, null=True)
    refid = models.ForeignKey(ApplyCompaign, db_column='REFID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'compaign_depts'


class CompaignDetail(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    item = models.CharField(max_length=200, blank=True, null=True)
    count = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    amout = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    refid = models.ForeignKey(ApplyCompaign, db_column='REFID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'compaign_detail'


class CompanyInfo(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  
    type = models.CharField(max_length=2000, blank=True, null=True)
    changed = models.CharField(max_length=2000, blank=True, null=True)
    memo = models.CharField(max_length=2000, blank=True, null=True)
    file = models.CharField(max_length=2000, blank=True, null=True)
    changed_flag = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_notify'


class DeviceLendNotify(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    member = models.CharField(max_length=2000, blank=True, null=True)
    memberid = models.CharField(db_column='memberID', max_length=2000, blank=True, null=True)  
    owner = models.CharField(max_length=2000, blank=True, null=True)
    ownerid = models.CharField(db_column='ownerID', max_length=2000, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    applicant_name = models.CharField(max_length=100, db_column='applicant', blank=True, null=True)
    applicant = models.ForeignKey(SysUser, to_field='userid', db_column='applicantID', max_length=100,
                                  blank=True, null=True)
    period = models.CharField(max_length=10, blank=True, null=True)
    approver = models.CharField(max_length=100, blank=True, null=True)
    approverid = models.CharField(db_column='approverID', max_length=100, blank=True, null=True)  
    totaltime = models.CharField(db_column='totalTime', max_length=50, blank=True, null=True)  
    file = models.CharField(max_length=2000, blank=True, null=True)
    totalday = models.DecimalField(db_column='totalDay', max_digits=2, decimal_places=0)  
    nightcount = models.DecimalField(db_column='nightCount', max_digits=2, decimal_places=0, blank=True, null=True)  
    transit = models.DecimalField(max_digits=13, decimal_places=0)
    transit_interval = models.CharField(max_length=2000)

    objects = EboaManager()

    class Meta:
        managed = False
        db_table = 'eb_attendance'
        verbose_name = verbose_name_plural = u"出勤"

    def __unicode__(self):
        if self.applicant:
            return self.applicant.fullname
        else:
            return self.applicant_name

    def get_cost_payment(self):
        """精算金額を取得する。

        :return:
        """
        cost_list = EbCostPayment.objects.filter(applicant=self.applicant, period=self.period)
        if cost_list.count() > 0:
            cost = cost_list[0]
            return cost.totalamountinside
        return 0

    def get_eb_member(self):
        if not self.applicant and not hasattr(self.applicant, 'ebemployee'):
            return None
        user_code = self.applicant.ebemployee.code
        try:
            return eb_models.Member.objects.get(employee_id=user_code)
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None

    def get_advance_amount(self):
        """管理職立替金額を取得する。

        :return:
        """
        member = self.get_eb_member()
        if member:
            expenses = member.employeeexpenses_set.filter(year=self.period[:4], month=self.period[-2:])
            if expenses.count() > 0:
                return expenses[0].advance_amount
            else:
                return 0
        return 0


class EbBankinfoUpdate(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    applicant_name = models.CharField(db_column='applicant', max_length=100, blank=True, null=True)
    applicant = models.ForeignKey(SysUser, db_column='applicantID', max_length=100, blank=True, null=True)
    period = models.CharField(max_length=10, blank=True, null=True)
    approver = models.CharField(max_length=100, blank=True, null=True)
    approverid = models.CharField(db_column='approverID', max_length=100, blank=True, null=True)  
    totalamount = models.DecimalField(db_column='totalAmount', max_digits=13, decimal_places=0, blank=True, null=True)  
    totalamountinside = models.DecimalField(db_column='totalAmountInside', max_digits=13, decimal_places=0)  
    totalamountoutside = models.DecimalField(db_column='totalAmountOutside', max_digits=13, decimal_places=0)  

    objects = EboaManager()

    class Meta:
        managed = False
        db_table = 'eb_cost_payment'


class EbCostPaymentList(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    day = models.CharField(max_length=10, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    number = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    amount = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    receipt = models.CharField(max_length=10, blank=True, null=True)
    refid = models.ForeignKey(EbCostPayment, db_column='REFID', blank=True, null=True)  
    type = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'eb_cost_payment_list'


class EbDependment(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=50, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=50, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    member = models.CharField(max_length=2000, blank=True, null=True)
    memberid = models.CharField(db_column='memberID', max_length=2000, blank=True, null=True)  
    owner = models.CharField(max_length=2000, blank=True, null=True)
    ownerid = models.CharField(db_column='ownerID', max_length=2000, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    specs_name = models.CharField(max_length=50, blank=True, null=True)
    specs_value = models.CharField(max_length=100, blank=True, null=True)
    refid = models.ForeignKey(EbDevice, db_column='REFID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'eb_device_specs'


class EbDuringMbCert(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  
    contract_date = models.DateTimeField(db_column='CONTRACT_DATE')  
    contract_no = models.CharField(db_column='CONTRACT_NO', max_length=100, blank=True, null=True)  
    employer_type = models.CharField(db_column='EMPLOYER_TYPE', max_length=100, blank=True, null=True)  
    employment_date = models.DateTimeField(db_column='EMPLOYMENT_DATE')  
    employment_period_en = models.DateTimeField(db_column='EMPLOYMENT_PERIOD_EN')  
    employment_period = models.CharField(db_column='EMPLOYMENT_PERIOD', max_length=1000, blank=True, null=True)  
    business_addr = models.CharField(db_column='BUSINESS_ADDR', max_length=100, blank=True, null=True)  
    business_type = models.CharField(db_column='BUSINESS_TYPE', max_length=100, blank=True, null=True)  
    business_other = models.CharField(db_column='BUSINESS_OTHER', max_length=1000, blank=True, null=True)  
    business_time = models.CharField(db_column='BUSINESS_TIME', max_length=1000, blank=True, null=True)  
    allowance_base = models.DecimalField(db_column='ALLOWANCE_BASE', max_digits=13, decimal_places=0, blank=True, null=True)  
    allowance_base_memo = models.CharField(db_column='ALLOWANCE_BASE_MEMO', max_length=1000, blank=True, null=True)  
    pay_site = models.DecimalField(db_column='PAY_SITE', max_digits=13, decimal_places=0, blank=True, null=True)  
    pay_site_memo = models.CharField(db_column='PAY_SITE_MEMO', max_length=1000, blank=True, null=True)  
    pay_position = models.DecimalField(db_column='PAY_POSITION', max_digits=13, decimal_places=0, blank=True, null=True)  
    pay_position_memo = models.CharField(db_column='PAY_POSITION_MEMO', max_length=1000, blank=True, null=True)  
    pay_duties = models.DecimalField(db_column='PAY_DUTIES', max_digits=13, decimal_places=0, blank=True, null=True)  
    pay_duties_memo = models.CharField(db_column='PAY_DUTIES_MEMO', max_length=1000, blank=True, null=True)  
    pay_diligence = models.DecimalField(db_column='PAY_DILIGENCE', max_digits=13, decimal_places=0, blank=True, null=True)  
    pay_safety = models.DecimalField(db_column='PAY_SAFETY', max_digits=13, decimal_places=0, blank=True, null=True)  
    pay_qual = models.DecimalField(db_column='PAY_QUAL', max_digits=13, decimal_places=0, blank=True, null=True)  
    pay_qual_memo = models.CharField(db_column='PAY_QUAL_MEMO', max_length=1000, blank=True, null=True)  
    pay_commute = models.DecimalField(db_column='PAY_COMMUTE', max_digits=13, decimal_places=0, blank=True, null=True)  
    pay_commute_memo = models.CharField(db_column='PAY_COMMUTE_MEMO', max_length=1000, blank=True, null=True)  
    pay_overtime = models.CharField(db_column='PAY_OVERTIME', max_length=100, blank=True, null=True)  
    pay_absence = models.CharField(db_column='PAY_ABSENCE', max_length=100, blank=True, null=True)  
    endowment_insurance = models.CharField(db_column='ENDOWMENT_INSURANCE', max_length=100, blank=True, null=True)  
    allowance_date = models.CharField(db_column='ALLOWANCE_DATE', max_length=1000, blank=True, null=True)  
    allowance_change = models.CharField(db_column='ALLOWANCE_CHANGE', max_length=1000, blank=True, null=True)  
    bonus = models.CharField(db_column='BONUS', max_length=1000, blank=True, null=True)  
    holiday = models.CharField(db_column='HOLIDAY', max_length=1000, blank=True, null=True)  
    paid_vacation = models.CharField(db_column='PAID_VACATION', max_length=1000, blank=True, null=True)  
    not_paid_vacation = models.CharField(db_column='NOT_PAID_VACATION', max_length=1000, blank=True, null=True)  
    about_discharge = models.CharField(db_column='ABOUT_DISCHARGE', max_length=1000, blank=True, null=True)  
    memo = models.CharField(db_column='MEMO', max_length=1000, blank=True, null=True)  
    cost = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_emp_contract'


class EbEmpEducation(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    start_ym = models.DateTimeField()
    end_ym = models.DateTimeField()
    school = models.CharField(max_length=100, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    undergraduate = models.CharField(max_length=100, blank=True, null=True)
    expert = models.CharField(max_length=100, blank=True, null=True)
    degree = models.CharField(max_length=2000, blank=True, null=True)
    refid = models.ForeignKey('EbEmployee', db_column='REFID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'eb_emp_education'


class EbEmpLanguage(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    type = models.CharField(max_length=2000, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    refid = models.ForeignKey('EbEmployee', db_column='REFID', blank=True, null=True)  
    code = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'eb_emp_language'


class EbEmpPjCareer(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    start_ymd = models.DateTimeField()
    end_ym = models.DateTimeField()
    pj_name = models.CharField(max_length=100, blank=True, null=True)
    pj_overview = models.CharField(max_length=500, blank=True, null=True)
    pj_duty = models.CharField(max_length=500, blank=True, null=True)
    pj_platform = models.CharField(max_length=200, blank=True, null=True)
    pj_platformid = models.CharField(db_column='pj_platformID', max_length=200, blank=True, null=True)  
    pj_framework = models.CharField(max_length=200, blank=True, null=True)
    pj_frameworkid = models.CharField(db_column='pj_frameworkID', max_length=200, blank=True, null=True)  
    pj_language = models.CharField(max_length=200, blank=True, null=True)
    pj_languageid = models.CharField(db_column='pj_languageID', max_length=200, blank=True, null=True)  
    pj_middleware = models.CharField(max_length=200, blank=True, null=True)
    pj_middlewareid = models.CharField(db_column='pj_middlewareID', max_length=200, blank=True, null=True)  
    refid = models.ForeignKey('EbEmployee', db_column='REFID', blank=True, null=True)  
    pj_database = models.CharField(max_length=20, blank=True, null=True)
    pj_databaseid = models.CharField(db_column='pj_databaseID', max_length=20, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    name = models.CharField(max_length=50, blank=True, null=True)
    get_date = models.DateTimeField()
    remark = models.CharField(max_length=2000, blank=True, null=True)
    refid = models.ForeignKey('EbEmployee', db_column='REFID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'eb_emp_qulification'


class EbEmployee(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
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
    user = models.OneToOneField(SysUser, to_field='userid', editable=False, blank=True, null=True)
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
    contractid = models.CharField(db_column='contractID', max_length=50, blank=True, null=True)  

    objects = EboaManager()

    class Meta:
        managed = False
        db_table = 'eb_employee'
        verbose_name = verbose_name_plural = u"社員"

    def __unicode__(self):
        return self.name


class EbInsureLossCert(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    device_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    refid = models.ForeignKey('EbMeetingRoom', db_column='REFID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'eb_m_room_device'


class EbMarriageContact(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    owner = models.CharField(max_length=2000, blank=True, null=True)
    ownerid = models.CharField(db_column='ownerID', max_length=2000, blank=True, null=True)  
    title = models.CharField(max_length=50, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    content = models.CharField(max_length=2000, blank=True, null=True)
    result = models.CharField(max_length=2000, blank=True, null=True)
    member = models.CharField(max_length=2000)
    memberid = models.CharField(db_column='memberID', max_length=2000)  
    writer = models.CharField(max_length=2000, blank=True, null=True)
    writerid = models.CharField(db_column='writerID', max_length=2000, blank=True, null=True)  
    room_id = models.CharField(max_length=50, blank=True, null=True)
    room = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_meeting'


class EbMeetingRoom(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    room_id = models.CharField(max_length=50, blank=True, null=True)
    room_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_meeting_room'


class EbNotice(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=100, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=100, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=100, blank=True, null=True)
    start_ym = models.DateTimeField()
    end_ym = models.DateTimeField()
    school = models.CharField(max_length=100, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    undergraduate = models.CharField(max_length=100, blank=True, null=True)
    expert = models.CharField(max_length=100, blank=True, null=True)
    degree = models.CharField(max_length=10, blank=True, null=True)
    refid = models.ForeignKey(EbResume, db_column='REFID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'eb_resume_education'


class EbResumeLanguage(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    level = models.CharField(max_length=100, blank=True, null=True)
    refid = models.ForeignKey(EbResume, db_column='REFID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'eb_resume_language'


class EbResumePjCareer(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=100, blank=True, null=True)
    no = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    start_ymd = models.DateTimeField()
    end_ymd = models.DateTimeField()
    pj_overview = models.CharField(max_length=100, blank=True, null=True)
    pj_duty = models.CharField(max_length=100, blank=True, null=True)
    pj_platform = models.CharField(max_length=20, blank=True, null=True)
    pj_platformid = models.CharField(db_column='pj_platformID', max_length=20, blank=True, null=True)  
    pj_language = models.CharField(max_length=20, blank=True, null=True)
    pj_languageid = models.CharField(db_column='pj_languageID', max_length=20, blank=True, null=True)  
    pj_middleware = models.CharField(max_length=20, blank=True, null=True)
    pj_middlewareid = models.CharField(db_column='pj_middlewareID', max_length=20, blank=True, null=True)  
    pj_database = models.CharField(max_length=20, blank=True, null=True)
    pj_databaseid = models.CharField(db_column='pj_databaseID', max_length=20, blank=True, null=True)  
    pj_role = models.CharField(max_length=20, blank=True, null=True)
    pj_scope_rd = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_bd = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_dd = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_pg = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_ut = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_si = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_st = models.CharField(max_length=1, blank=True, null=True)
    pj_scope_mt = models.CharField(max_length=1, blank=True, null=True)
    refid = models.ForeignKey(EbResume, db_column='REFID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'eb_resume_pj_career'


class EbResumeQualificat(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    get_date = models.DateTimeField()
    remark = models.CharField(max_length=100, blank=True, null=True)
    refid = models.ForeignKey(EbResume, db_column='REFID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'eb_resume_qualificat'


class EbRetireCert(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=10, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=10, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
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
    nameid = models.CharField(db_column='nameID', max_length=2000, blank=True, null=True)  
    start_ymd = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=5, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'eb_transit'


class EbTransitInterval(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    apply_no = models.CharField(max_length=10, blank=True, null=True)
    idx_no = models.CharField(max_length=100, blank=True, null=True)
    provider = models.CharField(max_length=50, blank=True, null=True)
    start_station = models.CharField(max_length=50, blank=True, null=True)
    arrive_station = models.CharField(max_length=50, blank=True, null=True)
    via_station = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    refid = models.ForeignKey(EbTransit, db_column='REFID', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'eb_transit_interval'


class EbVisaApplicaton(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)  
    change_date = models.DateTimeField()
    reason = models.CharField(max_length=2000, blank=True, null=True)
    reason_other = models.CharField(max_length=512, blank=True, null=True)
    new_name = models.CharField(max_length=100, blank=True, null=True)
    new_name_furigana = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'name_change_notify'


class RecruitManagement(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
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
    eb_resume_date = models.DateTimeField(db_column='EB_resume_date')  
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
    id = models.BigIntegerField(db_column='ID', primary_key=True)  
    test = models.CharField(max_length=50, blank=True, null=True)
    file1 = models.CharField(max_length=200, blank=True, null=True)
    file2 = models.CharField(max_length=200, blank=True, null=True)
    remarks = models.CharField(max_length=100, blank=True, null=True)
    xxxx = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test001'
