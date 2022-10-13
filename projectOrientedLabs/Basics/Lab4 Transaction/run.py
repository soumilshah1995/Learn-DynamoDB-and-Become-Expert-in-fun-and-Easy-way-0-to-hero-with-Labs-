
import pynamodb.attributes as at
from pynamodb.models import Model
from pynamodb.attributes import *
import uuid
from dotenv import load_dotenv
from pynamodb.connection import Connection
from pynamodb.transactions import TransactWrite
from pynamodb.exceptions import TransactWriteError
load_dotenv(".env")


class BankStatement(Model):
    class Meta:
        table_name = 'BankStatement'

    user_id = UnicodeAttribute(hash_key=True)
    account_balance = NumberAttribute(default=0)
    is_active = BooleanAttribute()
    version = VersionAttribute()

def delete_tables():

    # On Demand mode
    BankStatement.delete_table()

    # provisioned Mode
    # BankStatement.create_table(
    #     read_capacity_units=4,
    #     write_capacity_units=4,
    #     billing_mode='PROVISIONED')

def create_tables():

    # On Demand mode
    BankStatement.create_table(billing_mode='PAY_PER_REQUEST')

    # provisioned Mode
    # BankStatement.create_table(
    #     read_capacity_units=4,
    #     write_capacity_units=4,
    #     billing_mode='PROVISIONED')


user1_statement = BankStatement('user1', account_balance=3000, is_active=False)

connection = Connection()
with TransactWrite(connection=connection) as transaction:
    transaction.update(
        BankStatement(user_id='user1'),
        actions=[
            BankStatement.account_balance.set(100),
        ],
        condition=(
            (BankStatement.is_active == True)
        )
    )



# user2_statement = BankStatement('user2', account_balance=0, is_active=True)


# user2_statement.save()
#
# connection = Connection()
#
# try:
#     with TransactWrite(connection=connection,
#                        client_request_token='another-super-unique-key') as transaction:
#
#         # attempting to transfer funds from user1's account to user2's
#         transfer_amount = 1000
#         transaction.update(
#             BankStatement(user_id='user1'),
#             actions=[BankStatement.account_balance.add(transfer_amount * -1)],
#             condition=(
#                     (BankStatement.account_balance >= transfer_amount) &
#                     (BankStatement.is_active == True)
#             )
#         )
#         transaction.update(
#             BankStatement(user_id='user2'),
#             actions=[BankStatement.account_balance.add(transfer_amount)],
#             condition=(
#                         BankStatement.is_active == True )
#         )
#
# except TransactWriteError as e:
#     # Because the condition check on the account balance failed,
#     # the entire transaction should be cancelled
#     print("Error : ", e)
#
#     assert e.cause_response_code == 'TransactionCanceledException'


