import json
import os
from solc import compile_files
from pathlib import Path


"""
Created by Kelvin Fichter. Code lifted from omisego/plasma-contracts by Paul Peregud and moved into separate package.
"""

class Builder(object):

    def __init__(self, contracts_dir, output_dir):
        self.contracts_dir = contracts_dir
        self.output_dir = output_dir


    def compile_all(self):
        """Compiles all of the contracts in the self.contracts_dir directory

        Creates {contract name}.json files in self.output_dir that contain
        the build output for each contract.
        """

        # Compile the contracts
        real_path = os.path.realpath(self.contracts_dir)
        owd = os.getcwd()
        try:
            os.chdir(real_path)

            compilation_result = compile_files(
                ["RootChain.sol", "MintableToken.sol", "PlasmaCoreTest.sol", "RLPTest.sol"],
                optimize=True,
                optimize_runs=1,
                allow_paths=real_path
            )

            # Write the contract ABI to output files
            for contract in compilation_result.keys():
                contract_data = compilation_result[contract]
                contract_name = contract.split('.')[0]

                contract_data_path = self.output_dir + '/{0}.json'.format(contract_name)
                with open(contract_data_path, "w+") as contract_data_file:
                    json.dump(contract_data, contract_data_file)
        finally:
            os.chdir(owd)


    def get_contract_data(self, contract_name):
        """Returns the contract data for a given contract

        Args:
            contract_name (str): Name of the contract to return.

        Returns:
            str, str: ABI and bytecode of the contract
        """

        contract_data_path = self.output_dir + '/{0}.json'.format(contract_name)
        with open(contract_data_path, 'r') as contract_data_file:
            contract_data = json.load(contract_data_file)

        abi = contract_data['abi']
        bytecode = contract_data['bin']

        return abi, bytecode

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Compiles solidity contracts. Can also be used as a library.')
    parser.add_argument('-o', '--out_dir', required=True,
                        help='output directory (will be created if needed)')
    parser.add_argument('-i', '--input_dir', required=True,
                        help='input directory (will be recursively crawled)')
    args = parser.parse_args()

    builder = Builder(args.input_dir, args.out_dir)
    builder.compile_all()
