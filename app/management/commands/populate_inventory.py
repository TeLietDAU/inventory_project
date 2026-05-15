from django.core.management.base import BaseCommand
from app.models import Item
import random


class Command(BaseCommand):
    help = 'Populate inventory with 50 construction material products'

    def handle(self, *args, **options):
        if Item.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    'Database already contains items. Skipping population.'
                )
            )
            return

        random.seed(20260512)

        materials = [
            'Xi măng',
            'Gạch đỏ',
            'Gạch men',
            'Cát xây',
            'Đá 1x2',
            'Sắt thép',
            'Tôn lạnh',
            'Ống nhựa',
            'Sơn nước',
            'Ngói màu',
            'Keo dán gạch',
            'Bột trét tường',
            'Dây điện',
            'Công tắc điện',
            'Ổ cắm điện',
            'Giàn giáo',
            'Cốp pha',
            'Máy khoan',
            'Máy cắt sắt',
            'Máy trộn bê tông'
        ]

        brands = [
            'Hòa Phát',
            'Hoa Sen',
            'Viglacera',
            'Đồng Tâm',
            'Inax',
            'Dulux',
            'Jotun',
            'Cadivi',
            'Panasonic',
            'Bình Minh',
            'Tiền Phong',
            'Bosch',
            'Makita',
            'Weber',
            'Holcim'
        ]

        descriptions = {
            'Xi măng': 'Xi măng chất lượng cao dùng cho xây dựng dân dụng.',
            'Gạch đỏ': 'Gạch đỏ nung chịu lực tốt cho công trình.',
            'Gạch men': 'Gạch men lát nền chống trầy xước.',
            'Cát xây': 'Cát sạch dùng cho xây tô và bê tông.',
            'Đá 1x2': 'Đá xây dựng dùng để đổ bê tông.',
            'Sắt thép': 'Sắt thép chịu lực cho công trình.',
            'Tôn lạnh': 'Tôn lạnh chống nóng và chống gỉ.',
            'Ống nhựa': 'Ống nhựa PVC dùng cấp thoát nước.',
            'Sơn nước': 'Sơn nước nội ngoại thất cao cấp.',
            'Ngói màu': 'Ngói màu bền đẹp chống nóng.',
            'Keo dán gạch': 'Keo dán gạch độ bám dính cao.',
            'Bột trét tường': 'Bột trét giúp tường mịn đẹp.',
            'Dây điện': 'Dây điện lõi đồng an toàn.',
            'Công tắc điện': 'Công tắc điện thiết kế hiện đại.',
            'Ổ cắm điện': 'Ổ cắm điện an toàn cho gia đình.',
            'Giàn giáo': 'Giàn giáo thép chắc chắn.',
            'Cốp pha': 'Cốp pha dùng cho thi công bê tông.',
            'Máy khoan': 'Máy khoan công suất mạnh.',
            'Máy cắt sắt': 'Máy cắt sắt bền bỉ hiệu suất cao.',
            'Máy trộn bê tông': 'Máy trộn bê tông dùng cho công trình.'
        }

        products = []

        for i in range(1, 51):
            material = random.choice(materials)
            brand = random.choice(brands)

            name = f"{material} {brand} #{i}"
            sku = f"VLXD-{i:05d}"

            base_price = {
                'Xi măng': (85000, 120000),
                'Gạch đỏ': (1500, 3500),
                'Gạch men': (120000, 350000),
                'Cát xây': (250000, 500000),
                'Đá 1x2': (300000, 600000),
                'Sắt thép': (12000000, 18000000),
                'Tôn lạnh': (350000, 700000),
                'Ống nhựa': (50000, 250000),
                'Sơn nước': (500000, 1500000),
                'Ngói màu': (8000, 25000),
                'Keo dán gạch': (120000, 300000),
                'Bột trét tường': (100000, 250000),
                'Dây điện': (100000, 500000),
                'Công tắc điện': (50000, 150000),
                'Ổ cắm điện': (50000, 180000),
                'Giàn giáo': (1200000, 3500000),
                'Cốp pha': (500000, 1500000),
                'Máy khoan': (800000, 3500000),
                'Máy cắt sắt': (1500000, 5000000),
                'Máy trộn bê tông': (5000000, 15000000)
            }

            min_price, max_price = base_price[material]

            price = round(random.uniform(min_price, max_price), 2)
            stock_quantity = random.randint(10, 500)

            product = Item(
                name=name,
                sku=sku,
                description=descriptions[material],
                price=price,
                stock_quantity=stock_quantity
            )

            products.append(product)

        Item.objects.bulk_create(products)

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully created 50 construction material products'
            )
        )