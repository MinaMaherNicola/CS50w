from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User

# Create your models here.
class Type(models.Model):
    description = models.CharField(max_length=20)
    order_on_menu = models.IntegerField(default=0)
    image_name  = models.CharField(max_length=32, null=True)

    def __str__(self):
        return f" {self.id}: {self.order_on_menu}, {self.description}"

    class Meta:
        ordering = ('order_on_menu',)


class Topping(models.Model):
    VALID_FOR_CHOICES =(
        ('P', 'Pizza Only'),
        ('S', 'Subs Only'),
        ('B', 'Both Pizza and Subs'),
    )

    name = models.CharField(max_length = 32)
    valid_for = models.CharField(max_length = 1, choices=VALID_FOR_CHOICES)
    price = models.DecimalField(decimal_places=2, max_digits=3, default= 0.00)


    def __str__(self):
        return f"{self.name}"

class MenuItem(models.Model):
    SIZE_CHOICES = (
        ('S', 'Small'),
        ('L', 'Large'),
        ('', ''),
    )
    TOPPING_CHOICES =(

        (0, 'No extra toppings'),
        (1, '1 topping'),
        (2, '2 toppings'),
        (3, '3 toppings'),
        (5, 'Special'),
    )
    OPTION_CHOICES =(
        ('Y', 'Yes'),
        ('N', 'No'),
        ('C', 'Cheese-only'),
    )
    CRUST_CHOICES = (
        ('S', 'Sicilian'),
        ('R', 'Italian'),
        ('', '')
    )

    type_new = models.ForeignKey(Type, on_delete=models.CASCADE, default=0, null=True)
    name = models.CharField(max_length = 32)
    options = models.CharField(max_length =1, choices= OPTION_CHOICES, default='N')
    size = models.CharField(max_length=1, blank=True, choices=SIZE_CHOICES)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    number_of_toppings = models.SmallIntegerField(choices=TOPPING_CHOICES, default=0)
    crust = models.CharField(max_length=1, blank=True, choices=CRUST_CHOICES, default='')
    class Meta:
        ordering = ('type_new', 'name', 'size', 'number_of_toppings')


    def __str__(self):
        if ((self.type_new.description == 'Sicilian' or  self.type_new.description == 'Regular') and
                self.number_of_toppings == 0):
            return f"{self.type_new.description}: {self.name}, {self.get_size_display()}, Cheese, Price: {self.price}"
        if self.number_of_toppings == 0 and self.options != 'C':
            return f"{self.type_new.description}: {self.name}, {self.get_size_display()}, Price: {self.price}"
        else:
            return f"{self.type_new.description}: {self.name}, {self.get_size_display()}, {self.get_number_of_toppings_display()}, Base Price: {self.price}"

class Address(models.Model):
    STATES = (
        ('MA', 'Massachusetts'),
        ('FL', 'Florida'),
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length =64)
    address_line2 = models.CharField(max_length = 64, blank=True)
    city = models.CharField(max_length = 64)
    state = models.CharField(max_length =2, choices=STATES)
    zip = models.CharField(max_length = 10)
    default = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.address_line1}, {self.address_line2}, {self.city}, {self.state}  {self.zip}  {self.default}"

class OrderHeader(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(decimal_places=2, max_digits=5, null=True, editable=False)

    def __str__(self):
        formattedDate = self.created.strftime("%Y-%m-%d %H:%M")
        #self.subtotal = self.calc_ticket_tot()
        #self.save()
        return f"{self.id} {self.user_id} {formattedDate} {self.subtotal} "


    def calc_ticket_tot(self):
        subtotal= Decimal(0)
        lines = OrderLines.objects.filter(order_id = self.id)
        for line in lines:
            #print(line.item.price)
            subtotal += Decimal(line.item.price)
        self.subtotal = subtotal
        return

    def print_detail(self):
        lines = OrderLines.objects.filter(order_id = self.id)
        print(self)
        for line in lines:
            print(line)


    def save(self, *args, **kwargs):
        self.calc_ticket_tot()
        super().save(*args, **kwargs)
        return


class OrderLines(models.Model):
    order_id = models.ForeignKey(OrderHeader, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    extra_cheese = models.BooleanField(default=False)
    options = models.ManyToManyField(Topping, blank=True, related_name="orders")
    unit_price = models.DecimalField(decimal_places=2, max_digits=5, default=0)

    def __str__(self):
        cheese=''
        if self.extra_cheese == True:
            cheese=', extra cheese, '
        if ((self.item.type_new.description == 'Sicilian' or  self.item.type_new.description == 'Regular') and
            self.item.number_of_toppings == 0):
                return f"{self.item.type_new.description}: {self.item.name}, {self.item.get_size_display()}, Cheese"
        if self.item.number_of_toppings == 0:
            return f"{self.item.type_new.description}: {self.item.name}, {self.item.get_size_display()} {cheese}"
        else:
            toppings = []
            for each in self.options.all():
                toppings.append(each.name)
            return f"{self.item.type_new.description}: {self.item.name}, {self.item.get_size_display()}, {cheese} {self.item.get_number_of_toppings_display()}, {toppings}"

    def update_price(self):
        unit_price= Decimal(0)
        unit_price += self.item.price
        print(self.extra_cheese)
        if self.extra_cheese == True:
            add_on_price = Topping.objects.get(name='Cheese').price
            unit_price += Decimal(add_on_price)
            print(unit_price)
        self.unit_price = unit_price

    def save(self, *args, **kwargs):
        self.update_price()
        super().save(*args, **kwargs)
        return
