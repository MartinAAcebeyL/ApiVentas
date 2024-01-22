from apps.sales.models import SaleDetail
from apps.users.models import User
from django.db.models import Sum, F, Max


class GetSalesByUser:
    def get_sales_by_seller(self, seller: User):
        total_sales_and_quantity_group_by_category = self.get_total_sales_and_quantuty(
            seller
        )
        last_sales_dates_by_category = self.get_last_sale_by_category(seller)

        sale_products_by_category_and_date = (
            self.get_sale_products_by_category_and_date(seller)
        )

        return self.__mix_sales_by_category_and_date(
            total_sales_and_quantity_group_by_category,
            last_sales_dates_by_category,
            sale_products_by_category_and_date,
        )

    def __mix_sales_by_category_and_date(
        self,
        total_sales_and_quantity_group_by_category: list,
        last_sales_dates_by_category: list,
        sale_products_by_category_and_date: list,
    ):
        for sales_and_quantity in total_sales_and_quantity_group_by_category:
            for last_sale_date in last_sales_dates_by_category:
                if (
                    sales_and_quantity["category_name"]
                    == last_sale_date["category_name"]
                ):
                    sales_and_quantity["last_sale_date"] = last_sale_date[
                        "last_sale_date"
                    ]
                    break
            all_products_dict = {}

            for products in sale_products_by_category_and_date:
                if sales_and_quantity["category_name"] == products["category_name"]:
                    product_name = products["product_name"]
                    if all_products_dict.get(product_name):
                        all_products_dict[product_name].append(
                            {
                                "sale_date": products["sale_date"],
                                "quantity_sold": products["quantity_sold"],
                            }
                        )

                    else:
                        all_products_dict[product_name] = [
                            {
                                "sale_date": products["sale_date"],
                                "quantity_sold": products["quantity_sold"],
                            }
                        ]
            sales_and_quantity["data_sales"] = all_products_dict

        return total_sales_and_quantity_group_by_category

    def get_last_sale_by_category(self, seller: User):
        return (
            SaleDetail.objects.filter(sale__seller=seller)
            .values(category_name=F("sale__product__category__name"))
            .annotate(last_sale_date=Max("created_at"))
        )

    def get_total_sales_and_quantuty(self, seller: User):
        return (
            SaleDetail.objects.filter(sale__seller=seller)
            .values(category_name=F("sale__product__category__name"))
            .annotate(sales=Sum("total"), quantity=Sum("quantity"))
        )

    def get_sale_products_by_category_and_date(self, seller: User):
        return SaleDetail.objects.filter(sale__seller=seller).values(
            category_name=F("sale__product__category__name"),
            product_name=F("sale__product__name"),
            sale_date=F("created_at"),
            quantity_sold=F("quantity"),
        )
