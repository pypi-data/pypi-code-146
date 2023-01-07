from dataclasses import dataclass
from typing import List

__version__ = "0.0.1"


@dataclass
class Address:
    address1: str
    address2: str
    address3: str
    city: str
    postalCode: str
    country: str
    latitude: str
    longitude: str


@dataclass
class ContactInfo:
    email: str
    mobile: str


@dataclass
class Price:
    total: float
    energy: float
    tax: float
    startsAt: str
    currency: str
    level: str


@dataclass
class PriceRatingThresholdPercentages:
    high: float
    low: float


@dataclass
class PriceRatingEntry:
    time: str
    energy: float
    total: float
    tax: float
    difference: float
    level: str


@dataclass
class MeteringPointData:
    consumptionEan: str
    gridCompany: str
    gridAreaCode: str
    priceAreaCode: str
    productionEan: str
    energyTaxType: str
    vatType: str
    estimatedAnnualConsumption: int


@dataclass
class HomeConsumptionPageInfo:
    endCursor: str
    hasNextPage: bool
    hasPreviousPage: bool
    startCursor: str
    count: int
    currency: str
    totalCost: float
    totalConsumption: float
    filtered: int


@dataclass
class HomeFeatures:
    realTimeConsumptionEnabled: bool


@dataclass
class HomeProductionPageInfo:
    endCursor: str
    hasNextPage: bool
    hasPreviousPage: bool
    startCursor: str
    count: int
    currency: str
    totalProfit: float
    totalProduction: float
    filtered: int


@dataclass
class Consumption:
    from_: str
    to: str
    unitPrice: float
    unitPriceVAT: float
    consumption: float
    consumptionUnit: str
    cost: float
    currency: str


@dataclass
class Production:
    from_: str
    to: str
    unitPrice: float
    unitPriceVAT: float
    production: float
    productionUnit: str
    profit: float
    currency: str


@dataclass
class LegalEntity:
    id: str
    firstName: str
    isCompany: bool
    name: str
    middleName: str
    lastName: str
    organizationNo: str
    language: str
    contactInfo: ContactInfo
    address: Address


@dataclass
class PriceRatingType:
    minEnergy: float
    maxEnergy: float
    minTotal: float
    maxTotal: float
    currency: str
    entries: List[PriceRatingEntry]


@dataclass
class PriceRating:
    thresholdPercentages: PriceRatingThresholdPercentages
    hourly: PriceRatingType
    daily: PriceRatingType
    monthly: PriceRatingType


@dataclass
class PriceInfo:
    current: Price
    today: List[Price]
    tomorrow: List[Price]


@dataclass
class Subscription:
    id: str
    subscriber: LegalEntity
    validFrom: str
    validTo: str
    status: str
    priceInfo: PriceInfo
    priceRating: PriceRating


@dataclass
class Home:
    id: str
    timeZone: str
    appNickname: str
    appAvatar: str
    size: int
    type: str
    numberOfResidents: int
    primaryHeatingSource: str
    hasVentilationSystem: bool
    mainFuseSize: int
    address: Address
    owner: LegalEntity
    meteringPointData: MeteringPointData
    currentSubscription: Subscription
    subscriptions: List[Subscription]
    features: HomeFeatures


@dataclass
class Viewer:
    login: str
    userId: str
    name: str
    accountType: List[str]
    homes: List[Home]
    websocketSubscriptionUrl: str


@dataclass
class RootQuery:
    viewer: Viewer


# Method return types
@dataclass
class HomeConsumptionEdge:
    cursor: str
    node: Consumption


@dataclass
class HomeProductionEdge:
    cursor: str
    node: Production


@dataclass
class HomeConsumptionConnection:
    pageInfo: HomeConsumptionPageInfo
    nodes: List[Consumption]
    edges: List[HomeConsumptionEdge]


@dataclass
class HomeProductionConnection:
    pageInfo: HomeProductionPageInfo
    nodes: List[Production]
    edges: List[HomeProductionEdge]


# Mutations
@dataclass
class MeterReadingResponse:
    homeId: str
    time: str
    reading: int


@dataclass
class MeterReadingInput:
    homeId: str
    time: str
    reading: int


@dataclass
class UpdateHomeInput:
    homeId: str
    appNickname: str
    appAvatar: str
    size: int
    type: str
    numberOfResidents: int
    primaryHeatingSource: str
    hasVentilationSystem: bool
    mainFuseSize: int


@dataclass
class PushNotificationInput:
    title: str
    message: str
    screenToOpen: str


@dataclass
class PushNotificationResponse:
    successful: bool
    pushedToNumberOfDevices: int


@dataclass
class RootMutation:
    sendMeterReading: MeterReadingResponse
    updateHome: Home
    sendPushNotification: PushNotificationResponse


# Subscriptions
@dataclass
class LiveMeasurement:
    timestamp: str
    power: float
    lastMeterConsumption: float
    accumulatedConsumption: float
    accumulatedProduction: float
    accumulatedConsumptionLastHour: float
    accumulatedProductionLastHour: float
    accumulatedCost: float
    accumulatedReward: float
    currency: str
    minPower: float
    averagePower: float
    maxPower: float
    powerProduction: float
    powerProductionReactive: float
    minPowerProduction: float
    maxPowerProduction: float
    lastMeterProduction: float
    powerFactor: float
    voltagePhase1: float
    voltagePhase2: float
    voltagePhase3: float
    currentL1: float
    currentL2: float
    currentL3: float
    signalStrength: int


@dataclass
class RootSubscription:
    liveMeasurement: LiveMeasurement
    testMeasurement: LiveMeasurement
