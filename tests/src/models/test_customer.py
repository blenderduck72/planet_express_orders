from src.models.customer import Customer


class TestCustomer:
    def test_customer(
        self,
        customer_data_dict: dict,
    ) -> None:
        customer: Customer = Customer(**customer_data_dict)

        assert customer
        assert isinstance(customer, Customer)
        assert customer.email == customer_data_dict["email"]
        assert customer.first_name == customer_data_dict["first_name"]
        assert customer.last_name == customer_data_dict["last_name"]
