from NEMO.models import Area, BaseModel, Consumable, Project, StaffCharge, Tool, User
from django.db import models


class CoreFacility(BaseModel):
    name = models.CharField(max_length=200, unique=True, help_text="The name of this core facility.")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Core facilities"


class CoreRelationship(BaseModel):
    core_facility = models.ForeignKey(CoreFacility, on_delete=models.CASCADE)
    tool = models.OneToOneField(Tool, related_name="core_rel", blank=True, null=True, on_delete=models.CASCADE)
    area = models.OneToOneField(Area, related_name="core_rel", blank=True, null=True, on_delete=models.CASCADE)
    staff_charge = models.OneToOneField(StaffCharge, related_name="core_rel", blank=True, null=True, on_delete=models.CASCADE)
    consumable = models.OneToOneField(
        Consumable, related_name="core_rel", blank=True, null=True, on_delete=models.CASCADE
    )

    def get_item(self):
        return self.area if self.area else self.tool if self.tool else self.consumable

    def __str__(self):
        return f"{self.get_item()} - {self.core_facility}"


class CustomCharge(BaseModel):
    name = models.CharField(max_length=255, help_text="The name of this custom charge.")
    additional_details = models.CharField(
        max_length=255, null=True, blank=True, help_text="Additional details for this charge."
    )
    customer = models.ForeignKey(
        User, related_name="custom_charge_customer", on_delete=models.CASCADE, help_text="The customer to charge."
    )
    creator = models.ForeignKey(
        User,
        related_name="custom_charge_creator",
        on_delete=models.CASCADE,
        help_text="The person who created this charge.",
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text="The project to bill for this charge.")
    date = models.DateTimeField(help_text="The date of the custom charge.")
    amount = models.DecimalField(decimal_places=2, max_digits=8, help_text="The amount of the charge. Use a negative amount for adjustments.")
    core_facility = models.ForeignKey(CoreFacility, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


# Create and add a shortcut function to get core_facility from Tool, Consumable, Area or Staff Charge
def get_core_facility(self):
    # Add an exception for tool children, whose core facility is the parent's core facility
    if isinstance(self, Tool) and self.is_child_tool():
        return self.parent_tool.core_facility
    if hasattr(self, "core_rel"):
        return self.core_rel.core_facility


setattr(Tool, "core_facility", property(get_core_facility))
setattr(Consumable, "core_facility", property(get_core_facility))
setattr(Area, "core_facility", property(get_core_facility))
setattr(StaffCharge, "core_facility", property(get_core_facility))
