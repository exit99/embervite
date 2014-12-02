# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('desc', models.CharField(max_length=255, null=True, blank=True)),
                ('occurance', models.CharField(max_length=8, choices=[(b'weekly', b'Weekly')])),
                ('days', models.CommaSeparatedIntegerField(max_length=1000)),
                ('follow_up_days', models.CommaSeparatedIntegerField(max_length=1000)),
                ('time', models.TimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invite_sent', models.BooleanField(default=False)),
                ('follow_up_sent', models.BooleanField(default=False)),
                ('attending', models.NullBooleanField()),
                ('event', models.ForeignKey(to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255, null=True, blank=True)),
                ('desc', models.CharField(max_length=555, null=True, blank=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=255, null=True, blank=True)),
                ('carrier', models.CharField(blank=True, max_length=4, null=True, choices=[(b'@sms', b'3 River Wireless'), (b'@pag', b'ACS Wireless'), (b'@txt', b'AT&T'), (b'@mes', b'Alltel'), (b'@bpl', b'BPL Mobile'), (b'@bel', b'Bell Canada'), (b'@txt', b'Bell Mobility'), (b'@txt', b'Bell Mobility (Canada)'), (b'@blu', b'Blue Sky Frog'), (b'@sms', b'Bluegrass Cellular'), (b'@myb', b'Boost Mobile'), (b'er@c', b'Carolina West Wireless'), (b'@mob', b'Cellular One'), (b'@cso', b'Cellular South'), (b'@cwe', b'Centennial Wireless'), (b'@mes', b'CenturyTel'), (b'@txt', b'Cingular (Now AT&T)'), (b'@msg', b'Clearnet'), (b'@com', b'Comcast'), (b'@cor', b'Corr Wireless Communications'), (b'@mob', b'Dobson'), (b'@sms', b'Edge Wireless'), (b'@fid', b'Fido'), (b'@sms', b'Golden Telecom'), (b'@mes', b'Helio'), (b'@tex', b'Houston Cellular'), (b'@ide', b'Idea Cellular'), (b'@ivc', b'Illinois Valley Cellular'), (b'@inl', b'Inland Cellular Telephone'), (b'@pag', b'MCI'), (b'@tex', b'MTS'), (b'@mym', b'Metro PCS'), (b'@pag', b'Metrocall'), (b'@my2', b'Metrocall 2-way'), (b'@fid', b'Microcell'), (b'@cle', b'Midwest Wireless'), (b'@mob', b'Mobilcomm'), (b'@mes', b'Nextel'), (b'@onl', b'OnlineBeep'), (b'@pcs', b'PCS One'), (b'@txt', b"President's Choice"), (b'@sms', b'Public Service Cellular'), (b'@qwe', b'Qwest'), (b'@pcs', b'Rogers AT&T Wireless'), (b'@pcs', b'Rogers Canada'), (b'.pag', b'Satellink'), (b'@txt', b'Solo Mobile'), (b'@ema', b'Southwestern Bell'), (b'@mes', b'Sprint'), (b'@tms', b'Sumcom'), (b'@mob', b'Surewest Communicaitons'), (b'@tmo', b'T-Mobile'), (b'@msg', b'Telus'), (b'@txt', b'Tracfone'), (b'@tms', b'Triton'), (b'@ema', b'US Cellular'), (b'@usw', b'US West'), (b'@ute', b'Unicel'), (b'@vte', b'Verizon'), (b'@vmo', b'Virgin Mobile'), (b'@vmo', b'Virgin Mobile Canada'), (b'@sms', b'West Central Wireless'), (b'@cel', b'Western Wireless')])),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True, choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VI', b'Virgin Islands'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming'), (b'AB', b'Alberta'), (b'BC', b'British Columbia'), (b'NB', b'New Brunswick'), (b'MB', b'Manitoba'), (b'NF', b'Newfoundland'), (b'NT', b'Northwest Territories'), (b'NS', b'Nova Scotia'), (b'ON', b'Ontario'), (b'PE', b'Prince Edward Island'), (b'QC', b'Quebec'), (b'SK', b'Saskatchewan'), (b'YT', b'Yukon')])),
                ('zip', models.IntegerField(null=True, blank=True)),
                ('preference', models.CharField(max_length=10, choices=[(b'email', b'Email'), (b'phone', b'Phone')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='eventmember',
            name='member',
            field=models.ForeignKey(to='events.Member'),
            preserve_default=True,
        ),
    ]
