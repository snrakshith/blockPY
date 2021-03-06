from uuid import uuid4
from blockchain import Blockchain
from utilities.verification import Verification
from wallet import Wallet

class Node:
    def __init__(self):
        # self.wallet = str(uuid4())
        self.wallet = Wallet()
        self.blockchain = Blockchain(self.wallet.public_key)
   
   
    def get_transaction_value(self):
        """ Returns the input of the user (a new transaction amount) as a float. """
        # Get the user input, transform it from a string to a float and store it in user_input
        tx_recipient = input('Enter Account Holder of the transaction: ')
        tx_amount = float(input('Portfolio Allocation amount: '))
        return tx_recipient, tx_amount


    def get_user_choice(self):
        """Prompts the user for its choice and return it."""
        user_input = input('Your choice: ') 
        return user_input


    def print_blockchain_elements(self):
        """ Output all blocks of the blockchain. """
        # Output the blockchain list to the console
        for block in self.blockchain.get_chain():
            print('Outputting Block')
            print(" ")
            print(block)
            print(" ")
        else:
            print("------------------------------------- ")
    

    def listen_for_input(self):
        waiting_for_input = True
        # A while loop for the user input interface
        # It's a loop that exits once waiting_for_input becomes False or when break is called
        while waiting_for_input:
            """ Create an infite loop to run the blockchain cli """
            # print the user options
            print("------------------------------------- ")
            print(" ")
            print('Please choose an option?')
            print(" ")
            print('1: Allocate Portfolio Coin Value')
            print('2: Mine new block')
            print('3: Output the blockchain')
            print('4: Check blockchain validity')
            print('5: Create Client wallet')
            print('6: Load Client wallet')
            print('7: Save Client keys')
            print('q: Quit')
            print(" ")
            print("------------------------------------- ")
            print(" ")
            # save user input
            user_choice = self.get_user_choice()
            # Create a conditions to service the user input
            if user_choice == '1':
                tx_data = self.get_transaction_value() 
                recipient, amount = tx_data # I can destructure or unpack a tuple as such
                # create a transaction signature
                tx_signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                # Add the transaction amount to the blockchain
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, tx_signature, amount=amount): # add transactiont to open transactions
                    print('Added transaction!')
                else:
                    print('Transaction failed!')
                print("Open Txn: ",self.blockchain.get_open_transactions())
            elif user_choice == '2':
                try:
                    if not self.blockchain.mine_block():
                        print(" ")
                        print("Mining Failed, You need a Wallet")
                        print(" ")
                except:
                    print("Mining failed please establish a wallet and public key")
                    continue
            elif user_choice == '3':  # output existing blocks
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("All transactions are valid")
                else:
                    print("There are invalid transactions")
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                # This will lead to the loop to exist because it's running condition becomes False
                waiting_for_input = False
            else:
                print('Input was invalid, please pick a value from the list!')
            if not Verification.verify_chain(self.blockchain.get_chain()):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                # Break out of the loop
                break
            print("-------------------------------------")
            print(" ")
            print("Node Details:")
            print('Account Key: {}, Current Coin Value :{:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))
            print(" ")
        else:
            print('Session closed')

        print('Program secure, Logged Out!')
        print(" ")

if __name__ == '__main__':
    initial_node = Node()

    initial_node.listen_for_input()