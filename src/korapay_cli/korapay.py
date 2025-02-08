from typer import Typer
from korapay_client import (
    Card,
    Currency,
    Authorization,
    PaymentChannel,
    Country,
    MobileMoneyOperator,
    PayoutOrder,
)

from korapay_cli.utils import (
    get_korapay_client,
    colorized_print,
    override_output,
    parse_cli_string,
)

root_app = Typer(
    name="Korapay", help="A command line utility for interacting with Korapay's API"
)


@root_app.command()
@colorized_print
@override_output
def charge_via_card(
    reference: str,
    customer_name: str,
    customer_email: str,
    card: str,
    amount: float,
    currency: Currency,
    redirect_url: str | None = None,
    metadata: str | None = None,
    json: bool = False,
):
    """Accept debit card payments."""
    card = parse_cli_string(
        raw_string=card,
        arg_or_option_name="card",
        expected_type=Card,
    )
    if metadata:
        metadata = parse_cli_string(
            raw_string=metadata, arg_or_option_name="metadata", expected_type=dict
        )
    return get_korapay_client().charge_via_card(
        reference,
        customer_name,
        customer_email,
        card,
        amount,
        currency,
        redirect_url,
        metadata,
    )


@root_app.command()
@colorized_print
@override_output
def authorize_card_charge(
    transaction_reference: str, authorization: str, json: bool = False
):
    """Authorize a pending charge on a debit card."""
    authorization = parse_cli_string(
        raw_string=authorization,
        arg_or_option_name="authorization",
        expected_type=Authorization,
    )
    return get_korapay_client().authorize_card_charge(
        transaction_reference, authorization
    )


@root_app.command()
@colorized_print
@override_output
def resend_card_otp(transaction_reference: str, json: bool = False):
    """Resend one time password/pin for pending transaction."""
    return get_korapay_client().resend_card_otp(transaction_reference)


@root_app.command()
@colorized_print
@override_output
def charge_via_bank_transfer(
    reference: str,
    customer_email: str,
    amount: float,
    currency: Currency,
    customer_name: str | None = None,
    account_name: str | None = None,
    narration: str | None = None,
    notification_url: str | None = None,
    merchant_bears_cost: bool = False,
    metadata: str | None = None,
    json: bool = False,
):
    """Accept payments via bank transfers."""
    if metadata:
        metadata = parse_cli_string(
            raw_string=metadata, arg_or_option_name="metadata", expected_type=dict
        )
    return get_korapay_client().charge_via_bank_transfer(
        reference,
        customer_email,
        amount,
        currency,
        customer_name,
        account_name,
        narration,
        notification_url,
        merchant_bears_cost,
        metadata,
    )


@root_app.command()
@colorized_print
@override_output
def create_virtual_bank_account(
    account_name: str,
    account_reference: str,
    bank_code: str,
    customer_name: str,
    bvn: str,
    customer_email: str | None = None,
    nin: str | None = None,
    json: bool = False,
):
    """Create a virtual bank account.

    Virtual Bank Accounts (or Virtual Accounts) are a special type of bank account that you can use
    to receive payments from your customers multiple times."""
    return get_korapay_client().create_virtual_bank_account(
        account_name,
        account_reference,
        bank_code,
        customer_name,
        bvn,
        customer_email,
        nin,
    )


@root_app.command()
@colorized_print
@override_output
def get_virtual_bank_account(account_reference: str, json: bool = False):
    """Retrieve a virtual bank account."""
    return get_korapay_client().get_virtual_bank_account(account_reference)


@root_app.command()
@colorized_print
@override_output
def get_virtual_bank_account_transactions(account_number: str, json: bool = False):
    """Retrieve transactions associated with a virtual bank account."""
    return get_korapay_client().get_virtual_bank_account_transactions(account_number)


@root_app.command()
@colorized_print
@override_output
def credit_sandbox_virtual_bank_account(
    account_number: str, amount: float, currency: Currency, json: bool = False
):
    """Create a virtual bank account for testing/development."""
    return get_korapay_client().credit_sandbox_virtual_bank_account(
        account_number, amount, currency
    )


@root_app.command()
@colorized_print
@override_output
def charge_via_mobile_money(
    reference: str,
    customer_email: str,
    amount: float,
    mobile_money_number: str,
    currency: Currency,
    notification_url: str | None = None,
    customer_name: str | None = None,
    redirect_url: str | None = None,
    merchant_bears_cost: bool = False,
    description: str | None = None,
    metadata: str | None = None,
    json: bool = False,
):
    """Accept payments via mobile money.

    Note:
        Korapay currently only supports payments in Kenyan Shillings and Ghanaian Cedis. For Kenya,
        they support the following wallets; Mpesa, Airtel, and Equitel. While in Ghana, they support
        MTN Momo and Airtel Tigo.
    """
    if metadata:
        metadata = parse_cli_string(
            raw_string=metadata, arg_or_option_name="metadata", expected_type=dict
        )
    return get_korapay_client().charge_via_mobile_money(
        reference,
        customer_email,
        amount,
        mobile_money_number,
        currency,
        notification_url,
        customer_name,
        redirect_url,
        merchant_bears_cost,
        description,
        metadata,
    )


@root_app.command()
@colorized_print
@override_output
def authorize_mobile_money_charge(reference: str, token: str, json: bool = False):
    """Authorize a payment via mobile money.

    After initiating a charge via mobile money, the next step is based on the auth model returned
    in the response to the charge initiation. There are two ways of authorizing a transaction
    `OTP` and `STK_PROMPT`.
    After making the request to charge the number, if the status of the transaction is processing and
    auth_model is OTP, this means an OTP has been sent to the wallet owner's phone. You would need to
    collect the OTP to authorize the transaction.
    Collect the OTP sent to the customer’s phone and call this method with the
    OTP and the transaction reference.
    If the OTP verification is successful, an STK prompt will be sent to the wallet owner's phone for
    him to enter his PIN."""
    return get_korapay_client().authorize_mobile_money_charge(reference, token)


@root_app.command()
@colorized_print
@override_output
def resend_mobile_money_otp(transaction_reference: str, json: bool = False):
    """Resend one time password/pin for a pending mobile money transaction.

    This command allows you to resend OTP in a situation where the initial OTP received had expired
    or was not received at all."""
    return get_korapay_client().resend_mobile_money_otp(transaction_reference)


@root_app.command()
@colorized_print
@override_output
def resend_stk(transaction_reference: str, json: bool = False):
    """Resend STK prompt."""
    return get_korapay_client().resend_stk(transaction_reference)


@root_app.command()
@colorized_print
@override_output
def authorize_stk(reference: str, pin: str, json: bool = False):
    """Authorize STK prompts in test/development."""
    return get_korapay_client().authorize_stk(reference, pin)


@root_app.command()
@colorized_print
@override_output
def initiate_charge(
    reference: str,
    amount: float,
    currency: Currency,
    narration: str,
    notification_url: str,
    customer_email: str,
    customer_name: str | None = None,
    channels: str | None = None,
    default_channel: PaymentChannel | None = None,
    redirect_url: str | None = None,
    json: bool = False,
):
    """Initiate a charge on your customer supporting multiple payment channels."""
    if channels:
        channels = parse_cli_string(
            raw_string=channels,
            arg_or_option_name="channels",
            expected_type=PaymentChannel,
            many=True,
        )
    return get_korapay_client().initiate_charge(
        reference,
        amount,
        currency,
        narration,
        notification_url,
        customer_email,
        customer_name,
        channels,
        default_channel,
        redirect_url,
    )


@root_app.command()
@colorized_print
@override_output
def get_charge(reference: str, json: bool = False):
    """Retrieve a charge."""
    return get_korapay_client().get_charge(reference)


@root_app.command()
@colorized_print
@override_output
def resolve_bank_account(bank_code: str, account_number: str, json: bool = False):
    """Resolves a bank account."""
    return get_korapay_client().resolve_bank_account(bank_code, account_number)


@root_app.command()
@colorized_print
@override_output
def get_balances(json: bool = False):
    """Retrieve all your pending and available balances."""
    return get_korapay_client().get_balances()


@root_app.command()
@colorized_print
@override_output
def get_banks(country: Country, json: bool = False):
    """Retrieve a list of all banks supported by Korapay and their properties."""
    return get_korapay_client().get_banks(country)


@root_app.command()
@colorized_print
@override_output
def get_mmo(country: Country, json: bool = False):
    """Retrieve a list of all mobile money operators supported by Korapay and their properties."""
    return get_korapay_client().get_mmo(country)


@root_app.command()
@colorized_print
@override_output
def payout_to_bank_account(
    reference: str,
    amount: float,
    currency: Currency,
    bank_code: str,
    account_number: str,
    customer_email: str,
    narration: str | None = None,
    customer_name: str | None = None,
    json: bool = False,
):
    """Initiate a single disbursement to a bank account."""
    return get_korapay_client().payout_to_bank_account(
        reference,
        amount,
        currency,
        bank_code,
        account_number,
        customer_email,
        narration,
        customer_name,
    )


@root_app.command()
@colorized_print
@override_output
def payout_to_mobile_money(
    reference: str,
    amount: float,
    currency: Currency,
    mobile_money_operator: MobileMoneyOperator,
    mobile_number: str,
    customer_email: str,
    customer_name: str | None = None,
    narration: str | None = None,
    json: bool = False,
):
    """Initiate a single disbursement to a mobile money account."""
    return get_korapay_client().payout_to_mobile_money(
        reference,
        amount,
        currency,
        mobile_money_operator,
        mobile_number,
        customer_email,
        customer_name,
        narration,
    )


@root_app.command()
@colorized_print
@override_output
def bulk_payout_to_bank_account(
    batch_reference: str,
    description: str,
    merchant_bears_cost: bool,
    currency: Currency,
    payouts: str,
    json: bool = False,
):
    """Initiate a bulk payout to bank accounts."""
    payouts = parse_cli_string(
        raw_string=payouts,
        arg_or_option_name="payouts",
        expected_type=PayoutOrder,
        many=True,
    )
    return get_korapay_client().bulk_payout_to_bank_account(
        batch_reference, description, merchant_bears_cost, currency, payouts
    )


@root_app.command()
@colorized_print
@override_output
def get_payouts(bulk_reference: str, json: bool = False):
    """Retrieve a bulk  payout."""
    return get_korapay_client().get_payouts(bulk_reference)


@root_app.command()
@colorized_print
@override_output
def get_bulk_transaction(bulk_reference: str, json: bool = False):
    """Retrieve the transactions in a bulk payout."""
    return get_korapay_client().get_bulk_transaction(bulk_reference)


@root_app.command()
@colorized_print
@override_output
def get_payout_transaction(transaction_reference: str, json: bool = False):
    """Retrieve the status and details of a disbursement through the reference.

    This command can be used to verify the status of a payout transaction.
    """
    return get_korapay_client().get_payout_transaction(transaction_reference)
