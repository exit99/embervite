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
                ('location', models.CharField(max_length=255, null=True, blank=True)),
                ('occurance', models.CharField(max_length=8, choices=[(b'weekly', b'Weekly')])),
                ('days', models.CommaSeparatedIntegerField(max_length=1000)),
                ('time', models.TimeField()),
                ('invite_day', models.CommaSeparatedIntegerField(max_length=1000)),
                ('invite_time', models.TimeField()),
                ('disabled', models.BooleanField(default=False)),
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
                ('unique_hash', models.TextField(null=True, blank=True)),
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
                ('carrier', models.CharField(blank=True, max_length=50, null=True, choices=[(b'@sms.3rivers.net', b'3 River Wireless'), (b'@paging.acswireless.com', b'ACS Wireless'), (b'@txt.att.net', b'AT&T'), (b'@message.alltel.com', b'Alltel'), (b'@bplmobile.com', b'BPL Mobile'), (b'@bellmobility.ca', b'Bell Canada'), (b'@txt.bellmobility.ca', b'Bell Mobility'), (b'@txt.bell.ca', b'Bell Mobility (Canada)'), (b'@blueskyfrog.com', b'Blue Sky Frog'), (b'@sms.bluecell.com', b'Bluegrass Cellular'), (b'@myboostmobile.com', b'Boost Mobile'), (b'er@cwwsms.com', b'Carolina West Wireless'), (b'@mobile.celloneusa.com', b'Cellular One'), (b'@csouth1.com', b'Cellular South'), (b'@cwemail.com', b'Centennial Wireless'), (b'@messaging.centurytel.net', b'CenturyTel'), (b'@txt.att.net', b'Cingular (Now AT&T)'), (b'@msg.clearnet.com', b'Clearnet'), (b'@comcastpcs.textmsg.com', b'Comcast'), (b'@corrwireless.net', b'Corr Wireless Communications'), (b'@mobile.dobson.net', b'Dobson'), (b'@sms.edgewireless.com', b'Edge Wireless'), (b'@fido.ca', b'Fido'), (b'@sms.goldentele.com', b'Golden Telecom'), (b'@messaging.sprintpcs.com', b'Helio'), (b'@text.houstoncellular.net', b'Houston Cellular'), (b'@ideacellular.net', b'Idea Cellular'), (b'@ivctext.com', b'Illinois Valley Cellular'), (b'@inlandlink.com', b'Inland Cellular Telephone'), (b'@pagemci.com', b'MCI'), (b'@text.mtsmobility.com', b'MTS'), (b'@mymetropcs.com', b'Metro PCS'), (b'@page.metrocall.com', b'Metrocall'), (b'@my2way.com', b'Metrocall 2-way'), (b'@fido.ca', b'Microcell'), (b'@clearlydigital.com', b'Midwest Wireless'), (b'@mobilecomm.net', b'Mobilcomm'), (b'@messaging.nextel.com', b'Nextel'), (b'@onlinebeep.net', b'OnlineBeep'), (b'@pcsone.net', b'PCS One'), (b'@txt.bell.ca', b"President's Choice"), (b'@sms.pscel.com', b'Public Service Cellular'), (b'@qwestmp.com', b'Qwest'), (b'@pcs.rogers.com', b'Rogers AT&T Wireless'), (b'@pcs.rogers.com', b'Rogers Canada'), (b'.pageme@satellink.net', b'Satellink'), (b'@txt.bell.ca', b'Solo Mobile'), (b'@email.swbw.com', b'Southwestern Bell'), (b'@messaging.sprintpcs.com', b'Sprint'), (b'@tms.suncom.com', b'Sumcom'), (b'@mobile.surewest.com', b'Surewest Communicaitons'), (b'@tmomail.net', b'T-Mobile'), (b'@msg.telus.com', b'Telus'), (b'@txt.att.net', b'Tracfone'), (b'@tms.suncom.com', b'Triton'), (b'@email.uscc.net', b'US Cellular'), (b'@uswestdatamail.com', b'US West'), (b'@utext.com', b'Unicel'), (b'@vtext.com', b'Verizon'), (b'@vmobl.com', b'Virgin Mobile'), (b'@vmobile.ca', b'Virgin Mobile Canada'), (b'@sms.wcc.net', b'West Central Wireless'), (b'@cellularonewest.com', b'Western Wireless')])),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True, choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VI', b'Virgin Islands'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming'), (b'AB', b'Alberta'), (b'BC', b'British Columbia'), (b'NB', b'New Brunswick'), (b'MB', b'Manitoba'), (b'NF', b'Newfoundland'), (b'NT', b'Northwest Territories'), (b'NS', b'Nova Scotia'), (b'ON', b'Ontario'), (b'PE', b'Prince Edward Island'), (b'QC', b'Quebec'), (b'SK', b'Saskatchewan'), (b'YT', b'Yukon')])),
                ('zip', models.IntegerField(null=True, blank=True)),
                ('preference', models.CharField(max_length=10, choices=[(b'email', b'Email'), (b'phone', b'Phone'), (b'both', b'Both')])),
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
