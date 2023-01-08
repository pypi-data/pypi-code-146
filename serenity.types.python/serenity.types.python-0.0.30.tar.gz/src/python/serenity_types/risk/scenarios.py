from datetime import date, datetime
from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from serenity_types.portfolio.core import SimplePortfolio
from serenity_types.pricing.core import PricingContext
from serenity_types.utils.serialization import CamelModel


class ShockPnL(CamelModel):
    """
    Value object with information about a particular dimension's P&L impact from a single shock.
    """

    shock_id: UUID
    """
    Unique ID for the shock from the original ShockDefinition.
    """

    shock_pnl: float
    """
    The PnL, in base currency, from the shock, e.g. the portfolio would have lost an
    additional $2K if this shock had been applied.
    """


class PnL(CamelModel):
    """
    Value object with information about a particular dimension's P&L impact from all shocks.
    """

    base_pnl: float
    """
    The PnL, in base currency, over the period (default 1 day) absent all the shocks, e.g.
    portfolio lost $12K in the last 24 hours.
    """

    total_shock_pnl: float
    """
    The PnL, in base currency, from all shocks combined, e.g. the portfolio would have lost an additional
    $50K if all shocks had been applied.
    """

    pnl_by_shock: List[ShockPnL]
    """
    The PnL, in base currency, from applying each shock individually, e.g. the portfolio would have lost
    $4K from shocking ETH down 10% and $35K from shocking BTC down 10%.
    """


class AssetPnL(CamelModel):
    """
    A single entry representing an asset-level impact of this scenario's shocks.
    It supports both by-asset and by-sector views in Serenity UX.
    """

    asset_id: UUID
    """
    Unique asset identifier from the Asset Master.
    """

    sector_levels: List[str]
    """
    A list of sector level names that identifies a “path” to a particular
    level in the sector taxonomy, as defined above; note we only have the
    leaf level here; we don't need to show PnL at each level in the sector
    hierarchy above the assets, UX can do the aggregation since $ values
    are additive here.
    """

    asset_pnl: PnL
    """
    P&L impact in total and by shock for this asset.
    """


class FactorPnL(CamelModel):
    """
    A single entry representing a factor-level impact of this scenario's shocks.
    """

    factor: str
    """
    Factor name, e.g. MOMENTUM.
    """

    factor_exposure_base_ccy: float
    """
    Total factor exposure in the portfolio, in base currency.
    """

    factor_pnl: PnL
    """
    P&L impact in total and by shock for this factor.
    """


class ScenarioSource(Enum):
    """
    Enum classifying scenarios by whether they are user- or system-defined.
    """

    CUSTOM = 'CUSTOM'
    """
    A user-defined scenario.
    """

    PREDEFINED = 'PREDEFINED'
    """
    A canned scenario provided by the platform; typically these represent
    fitted historical events like the 2020 COVID Crash.
    """


class ShockTo(Enum):
    """
    Enum classifying what is being shocked, e.g. asset returns or factor returns.
    """

    ASSET = "ASSET"
    """
    Shock applied additively to the asset's returns at the close, per MarkTime.
    """

    FACTOR = "FACTOR"
    """
    Shock applied additively to the factor's returns at the close, per MarkTime.
    """


class Shock(CamelModel):
    """
    A discrete market shock that is being simulated in a scenario.
    """

    shock_id: UUID
    """
    Unique ID for the shock; this can be generated and stored with the ShockDefinition (and thus unchanging)
    or if the scenario is run on-the-fly, the UUID should be generate at request time so there is a clear
    linkage between Shock and ShockPnL.
    """

    target_type: ShockTo
    """
    What to shock: asset returns or factor returns?
    """

    shock_target: Union[UUID, str]
    """
    UUID for asset ID, or name of the factor to shock.
    """

    magnitude: float
    """
    Magnitude of the shock, + / - for up or down shock actions; note this is expressed as a fraction, not a percentage.
    """


class ScenarioDefinition(CamelModel):
    """
    A complete definition of a stress test to perform for scenario analysis.
    """

    scenario_id: Optional[UUID]
    """
    Unique ID for this scenario, optional when creating or if we are dealing with a transient scenario to run.
    """

    scenario_version: Optional[int]
    """
    Monotonically increasing version number, optional when creating or if we are dealing
    with a transient scenario to run.
    """

    source: ScenarioSource
    """
    Whether this shock is user- or system-defined.
    """

    name: str
    """
    A descriptive name for this scenario.
    """

    shocks: List[Shock]
    """
    The discrete shocks to apply as part of this scenario.
    """

    deleted: Optional[bool] = False
    """
    If set, this definition was logically deleted in the database and is not current.
    """

    last_updated: Optional[datetime]
    """
    Last update timestamp, in UTC.
    """

    last_updated_by: str
    """
    Last update user.
    """


class ScenarioCloneRequest(CamelModel):
    """
    A request to clone an existing scenario; typically used to allow the client
    to customize a canned scenario.
    """

    scenario_id: UUID
    """
    Unique ID of the custom or predefined scenario to clone.
    """

    scenario_name: str
    """
    Name to use post-cloning to avoid ambiguity.
    """


class ScenarioRequest(CamelModel):
    """
    A request to run a scenario against a portfolio. This scenario may be stored or transient.
    """

    scenario_id: Optional[UUID]
    """
    Unique ID of the scenario to run; if not provided, user must provide a transient scenario instead.
    """

    scenario: Optional[ScenarioDefinition]
    """
    Transient scenario to run; if not provided, user must provide a scenario ID instead.
    """

    portfolio: SimplePortfolio
    """
    Portfolio to run the scenario on.
    """

    pricing_context: PricingContext
    """
    Common model inputs, e.g. mark time.
    """

    sector_taxonomy_id: Optional[UUID]
    """
    References a taxonomy UUID from the Refdata API, specifically the getSectorTaxonomies call.
    """

    model_config_id: UUID
    """
    Factor model configuration ID to use for risk purposes.
    """

    start_date: Optional[date]
    """
    Start of the shock period; in the instantaneous case, same as end_date.
    """

    end_date: Optional[date]
    """
    End of the shock period; in the instantaneous case, same as start_date.
    """

    schema_version: Optional[int]
    """
    Version number for the scenario schema.
    """


class ScenarioResult(CamelModel):
    """
    ScenarioResult provides the portfolio base & shock P&L and the breakdowns by asset, sector and by factor.
    """

    portfolio_pnl: PnL
    """
    The impact to the portfolio broken out by shocks.
    """

    asset_pnl: List[AssetPnL]
    """
    Report on P&L impact by asset & sector.
    """

    factor_pnl: List[FactorPnL]
    """
    Report on P&L impact by risk factor in the provided factor risk model.
    """

    start_date: date
    """
    Start of the shock period; in the instantaneous case, same as end_date.
    """

    end_date: date
    """
    End of the shock period; in the instantaneous case, same as start_date.
    """

    scenario_run_id: UUID
    """
    The run that this result is associated with.
    """

    warnings: List[str]
    """
    Any warnings generated at the time of the run.
    """

    schema_version: int
    """
    Version number for the scenario schema.
    """


class RunStatus(Enum):
    """
    Results of the scenario run at a high level.
    """

    RUNNING = 'RUNNING'
    """
    Job sent to the scenario engine and running, may be async / long-running.
    """

    COMPLETED = 'COMPLETED'
    """
    Job completed with no errors.
    """

    FAILED = 'FAILED'
    """
    Job failed with an error.
    """


class ScenarioRun(CamelModel):
    """
    A summary of the run. Note that to get the detail you need to call getScenarioRun with the runId;
    this just gives you the status, the base PnL absent all the shocks and the total shock PnL.
    """

    run_id: UUID
    """
    Unique ID of this run.
    """

    scenario_request: ScenarioRequest
    """
    The request that was run previously.
    """

    status: RunStatus
    """
    Current state of the run.
    """

    base_pnl: float
    """
    The PnL, in base currency, over the period (default 1 day) absent all the shocks,
    e.g. portfolio lost $12K in the last 24 hours.
    """

    total_shock_pnl: float
    """
    the PnL, in base currency, from all shocks combined, e.g. the portfolio would have
    lost an additional $50K if all shocks had been applied.
    """

    start_datetime: datetime
    """
    UTC datetime of the run start.
    """

    end_datetime: Optional[datetime]
    """
    UTC datetime of the run completion, if COMPLETED.
    """
