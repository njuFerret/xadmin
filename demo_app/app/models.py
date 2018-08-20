from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

SERVER_STATUS = (
    (0, u"正常"),
    (1, u"宕机"),
    (2, u"无连接"),
    (3, u"错误"),
)
SERVICE_TYPES = (
    ('moniter', u"监视器"),
    ('lvs', u"LVS"),
    ('db', u"数据库"),
    ('analysis', u"分析"),
    ('admin', u"管理"),
    ('storge', u"存储"),
    ('web', u"WEB"),
    ('email', u"Email"),
    ('mix', u"Mix"),
)


@python_2_unicode_compatible
class IDC(models.Model):
    name = models.CharField(max_length=64, verbose_name="名称")
    description = models.TextField(verbose_name="描述")

    contact = models.CharField(max_length=32, verbose_name="联系人")
    telphone = models.CharField(max_length=32, verbose_name="联系电话")
    address = models.CharField(max_length=128, verbose_name="地址")
    customer_id = models.CharField(max_length=128, verbose_name="用户ID")
    groups = models.ManyToManyField(Group)  # many

    create_time = models.DateField(auto_now=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"IDC"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class Host(models.Model):
    idc = models.ForeignKey(IDC, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    nagios_name = models.CharField(
        u"Nagios Host ID", max_length=64, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    internal_ip = models.GenericIPAddressField(blank=True, null=True)
    user = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    ssh_port = models.IntegerField(blank=True, null=True)
    status = models.SmallIntegerField(choices=SERVER_STATUS)

    brand = models.CharField(max_length=64, choices=[
                             (i, i) for i in (u"DELL", u"HP", u"Other")])
    model = models.CharField(max_length=64)
    cpu = models.CharField(max_length=64)
    core_num = models.SmallIntegerField(
        choices=[(i * 2, "%s Cores" % (i * 2)) for i in range(1, 15)])
    hard_disk = models.IntegerField()
    memory = models.IntegerField()

    system = models.CharField(u"操作系统", max_length=32, choices=[
                              (i, i) for i in (u"CentOS", u"FreeBSD", u"Ubuntu")])
    system_version = models.CharField(max_length=32)
    system_arch = models.CharField(max_length=32, choices=[
                                   (i, i) for i in (u"x86_64", u"i386")])

    create_time = models.DateField()
    guarantee_date = models.DateField()
    service_type = models.CharField(max_length=32, choices=SERVICE_TYPES)
    description = models.TextField()

    administrator = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Admin")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"主机"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class MaintainLog(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    maintain_type = models.CharField(max_length=32)
    hard_type = models.CharField(max_length=16)
    time = models.DateTimeField()
    operator = models.CharField(max_length=16)
    note = models.TextField()

    def __str__(self):
        return '%s 维护日志 [%s] %s %s' % (self.host.name, self.time.strftime('%Y-%m-%d %H:%M:%S'),
                                       self.maintain_type, self.hard_type)

    class Meta:
        verbose_name = u"维护日志"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class HostGroup(models.Model):

    name = models.CharField(max_length=32)
    description = models.TextField()
    hosts = models.ManyToManyField(
        Host, verbose_name=u'主机', blank=True, related_name='groups')

    class Meta:
        verbose_name = u"主机分组"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AccessRecord(models.Model):
    date = models.DateField()
    user_count = models.IntegerField()
    view_count = models.IntegerField()

    class Meta:
        verbose_name = u"访问记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s 访问记录" % self.date.strftime('%Y-%m-%d')
