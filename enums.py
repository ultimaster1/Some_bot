from enum import Enum

class HttpMethod(Enum):
    GET = 1
    POST = 2
    PUT = 3

class OrderSide(Enum):
    Bid = 0
    Ask = 1

class AccountType(Enum):
    Trade = 1
    Investment = 2
    PAMM = 3

class CurrencyType(Enum):
    Fiat = 0
    Crypto = 1
    Token = 2

class ExecutionType(Enum):
    Limit = 0
    Market = 1
    StopLimit = 2

class InvestmentStatus(Enum):
    Active = 0
    Withdrawn = 1

class OrderStatus(Enum):
    New = 0
    PartiallyFilled = 1
    Filled = 2
    Cancelled = 3
    Inactive = 4

class OrderType(Enum):
    Limit = 0
    Market = 1
    Stop = 2
    StopLimit = 3
    TrailingStop = 4
    FillOrKill = 5

class CodeStatus(Enum):
    Active = 0
    Expired = 1
    Redeemed = 2
    Unconfirmed = 3
    Canceled = 4
    Merged = 5
    Blocked = 6

class CodeAction(Enum):
    Unblock = 0
    Block = 1
    Redeem = 2
    Cancel = 3

class TransactionMethodType(Enum):
    BitqiCode = 12
    FullManualProcessing = 23
    Blockchain = 24
    Admin = 25

class TransactionStatus(Enum):
    AwaitingConfirmation = 0
    Processing = 1
    Completed = 2
    Cancelled = 3
    Declined = 4
    AdminCheck = 5
    AdminProcessing = 6
    New = 7
    AwaitingManualCheck = 8
    AwaitingUserConfirmation = 9

class TransactionType(Enum):
    Deposit = 0
    Withdrawal = 1

class LayoutTheme(Enum):
    Light = 0
    Dark = 1

class ClientClaimType(Enum):
    Deposit = (1 << 1)
    Withdrawal = (1 << 2)
    Trade = (1 << 3)
    Data = (1 << 4)

class WidgetType(Enum):
    Chart = 0
    Chat = 1
    OrderTool = 2
    Trades = 3
    Markets = 4
    OrderBook = 5
    ActiveOrders = 6

class VerificationStatus(Enum):
    Unverified = 0
    InProcess = 1
    RequiresData = 2
    Verified = 3
    VerificationRequest = 4

class TwoFactorSectionType(Enum):
    SignIn = (1<<0)
    Transaction= (1 << 1)
    ApiKeys = (1 << 2)
    IpWhiteList = (1 << 3)


