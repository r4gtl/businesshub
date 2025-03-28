# Generated by Django 5.1.7 on 2025-03-28 08:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('anagrafiche', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DichiarazioneIntento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_interno', models.PositiveIntegerField()),
                ('numero_dichiarazione', models.CharField(max_length=100)),
                ('tipo_operazione', models.CharField(blank=True, choices=[('A', 'Acquisto'), ('I', 'Importazione')], max_length=1, verbose_name='Tipo Operazione')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Note')),
                ('data_dichiarazione', models.DateField()),
                ('importosingolo', models.BooleanField(default=False, verbose_name='Importo Singolo')),
                ('plafond', models.DecimalField(decimal_places=2, max_digits=12)),
                ('anno_riferimento', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('fk_dogana', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='anagrafiche.dogana', verbose_name='Dogana')),
                ('fornitore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anagrafiche.fornitore')),
            ],
        ),
        migrations.CreateModel(
            name='FatturaFornitore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_fattura', models.CharField(max_length=100)),
                ('data_fattura', models.DateField()),
                ('importo', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('fornitore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fatture', to='anagrafiche.fornitore')),
            ],
        ),
    ]
