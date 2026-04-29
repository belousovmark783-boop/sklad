from django.db import models


class Room(models.Model):
    name = models.CharField("Название", max_length=255)
    capacity = models.FloatField("Полезный объём (м³)")

    class Meta:
        verbose_name = "Помещение"
        verbose_name_plural = "Помещения"

    def __str__(self):
        return self.name


class Rack(models.Model):
    number = models.CharField("Номер стеллажа", max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Помещение", related_name="racks")
    slots_count = models.IntegerField("Количество мест")
    slot_height = models.FloatField("Высота места (м)")
    slot_width = models.FloatField("Ширина места (м)")
    slot_length = models.FloatField("Длина места (м)")
    max_load = models.FloatField("Макс. суммарная нагрузка (кг)")

    class Meta:
        verbose_name = "Стеллаж"
        verbose_name_plural = "Стеллажи"

    def __str__(self):
        return f"Стеллаж {self.number} ({self.room.name})"


class Client(models.Model):
    name = models.CharField("Наименование юридического лица", max_length=255)
    bank_details = models.TextField("Банковские реквизиты")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.name


class Item(models.Model):
    height = models.FloatField("Высота (м)")
    width = models.FloatField("Ширина (м)")
    length = models.FloatField("Длина (м)")
    weight = models.FloatField("Вес (кг)")
    arrival_date = models.DateField("Дата поступления")
    contract_number = models.CharField("Номер договора", max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент", related_name="items")
    contract_end_date = models.DateField("Дата окончания договора")
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, verbose_name="Стеллаж", related_name="items")
    position = models.IntegerField("Позиция размещения (номер)")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"Товар по договору {self.contract_number}"
