# Generated by Django 2.1.4 on 2018-12-06 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produtos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstoqueEntrada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField(auto_created=True)),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('quantidade', models.IntegerField(default=0)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='produtos.Produto')),
            ],
            options={
                'verbose_name': 'entrada no estoque',
                'verbose_name_plural': 'entrada no estoque',
            },
        ),
        migrations.CreateModel(
            name='EstoqueSaida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField(auto_created=True)),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('quantidade', models.IntegerField(default=0)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='produtos.Produto')),
            ],
            options={
                'verbose_name': 'Saída do estoque',
                'verbose_name_plural': 'saída do estoque',
            },
        ),
    ]
