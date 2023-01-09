from typing import Optional, Type, List, Union, Dict, Any
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty

__all__ = [
    'Charge',
    'Charges',
    'Plan',
    'PlanResponse',
    'PlanRoute',
]


class Charge(BaseResource):
    id: Optional[str]
    lago_id: Optional[str]
    billable_metric_id: Optional[str]
    lago_billable_metric_id: Optional[str]
    charge_model: Optional[str]
    properties: Optional[Union[dict, list]]
    group_properties: Optional[Union[List[Any], Dict]]

class Charges(BaseResource):
    __root__: List[Charge] = []

class Plan(BaseResource):
    name: Optional[str]
    code: Optional[str]
    interval: Optional[str]
    description: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    trial_period: Optional[float]
    pay_in_advance: Optional[bool]
    bill_charges_monthly: Optional[bool]
    charges: Optional[Union[List[Charge], Charges]] = Charges()
    
    def add_charge_to_plan(self, charge: Charge):
        """
        Adds a charge to the plan's charges.
        """
        self.charges.__root__.append(charge)


class PlanResponse(BaseResource):
    lago_id: str
    name: str
    created_at: str
    code: str
    interval: Optional[str]
    description: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    trial_period: Optional[float]
    pay_in_advance: Optional[bool]
    bill_charges_monthly: Optional[bool]
    charges: Optional[Charges]

    def has_metric_id(self, metric_id: str) -> bool:
        """
        Checks to see whether a metric_id is present in the plan's charges.
        """
        return any(
            (charge.billable_metric_id and charge.billable_metric_id == metric_id) or 
            (charge.lago_billable_metric_id and charge.lago_billable_metric_id == metric_id) 
            for charge in self.charges.__root__
        )
    
    def remove_charge_from_plan(self, charge: Charge):
        """
        Removes a charge from the plan's charges.
        """
        for c in self.charges.__root__:
            if (c.billable_metric_id and c.billable_metric_id == charge.billable_metric_id) or (c.lago_billable_metric_id and c.lago_billable_metric_id == charge.lago_billable_metric_id):
                self.charges.__root__.remove(c)
                break

    
    def to_plan(self) -> Plan:
        """
        Converts a PlanResponse to a Plan.
        """
        return Plan(
            name = self.name,
            code = self.code,
            interval = self.interval,
            description = self.description,
            amount_cents = self.amount_cents,
            amount_currency = self.amount_currency,
            trial_period = self.trial_period,
            pay_in_advance = self.pay_in_advance,
            bill_charges_monthly = self.bill_charges_monthly,
            charges = self.charges
        )

    def add_charge_to_plan(self, charge: Charge):
        """
        Adds a charge to the plan's charges.
        """
        self.charges.__root__.append(charge)

class PlanRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = Plan
    response_model: Optional[Type[BaseResource]] = PlanResponse
    usage_model: Optional[Type[BaseResource]] = None

    @lazyproperty
    def api_resource(self):
        return 'plans'

    @lazyproperty
    def root_name(self):
        return 'plan'