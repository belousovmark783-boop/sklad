from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование юридического лица')),
                ('bank_details', models.TextField(verbose_name='Банковские реквизиты')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('capacity', models.FloatField(verbose_name='Полезный объём (м³)')),
            ],
            options={
                'verbose_name': 'Помещение',
                'verbose_name_plural': 'Помещения',
            },
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50, verbose_name='Номер стеллажа')),
                ('slots_count', models.IntegerField(verbose_name='Количество мест')),
                ('slot_height', models.FloatField(verbose_name='Высота места (м)')),
                ('slot_width', models.FloatField(verbose_name='Ширина места (м)')),
                ('slot_length', models.FloatField(verbose_name='Длина места (м)')),
                ('max_load', models.FloatField(verbose_name='Макс. суммарная нагрузка (кг)')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='racks', to='wb.room', verbose_name='Помещение')),
            ],
            options={
                'verbose_name': 'Стеллаж',
                'verbose_name_plural': 'Стеллажи',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.FloatField(verbose_name='Высота (м)')),
                ('width', models.FloatField(verbose_name='Ширина (м)')),
                ('length', models.FloatField(verbose_name='Длина (м)')),
                ('weight', models.FloatField(verbose_name='Вес (кг)')),
                ('arrival_date', models.DateField(verbose_name='Дата поступления')),
                ('contract_number', models.CharField(max_length=100, verbose_name='Номер договора')),
                ('contract_end_date', models.DateField(verbose_name='Дата окончания договора')),
                ('position', models.IntegerField(verbose_name='Позиция размещения (номер)')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='wb.client', verbose_name='Клиент')),
                ('rack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='wb.rack', verbose_name='Стеллаж')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]
