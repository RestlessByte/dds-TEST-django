from django.core.management.base import BaseCommand
from core.models import Status, Type, Category, Subcategory

class Command(BaseCommand):
    help = "Инициализирует базовые справочники"

    def handle(self, *args, **kwargs):
        statuses = ["Бизнес","Личное","Налог"]
        for s in statuses: Status.objects.get_or_create(name=s)

        t_pop, _ = Type.objects.get_or_create(name="Пополнение")
        t_exp, _ = Type.objects.get_or_create(name="Списание")

        # Примеры категорий/подкатегорий
        infra, _ = Category.objects.get_or_create(name="Инфраструктура", type=t_exp)
        marketing, _ = Category.objects.get_or_create(name="Маркетинг", type=t_exp)

        for n in ["VPS","Proxy"]: Subcategory.objects.get_or_create(name=n, category=infra)
        for n in ["Farpost","Avito"]: Subcategory.objects.get_or_create(name=n, category=marketing)

        self.stdout.write(self.style.SUCCESS("Справочники инициализированы."))
