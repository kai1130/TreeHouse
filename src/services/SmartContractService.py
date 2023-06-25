from web3 import Web3

class ContractService():
    def __init__(self, w3_provider, contract_addr, contract_abi):
        self.provider = w3_provider
        self.w3 = Web3(Web3.HTTPProvider(w3_provider))
        self.contract_addr = contract_addr
        self.contract_abi = contract_abi

        self.controller = self.w3.eth.contract(
            address = self.contract_addr,
            abi = self.contract_abi
        )

    def grabAllRegisteredMaterials(self):
        aspect_count = self.controller.functions.getAspectCount().call()
        
        aspect_list = []

        for i in range(aspect_count):
            aspect_tuple = self.controller.functions.getAspect(i + 1).call()
            aspect_list.append(aspect_tuple)

        return tuple(aspect_list)

    def grabRegisteredMaterialsOnIndex(self, idx):
        aspect = self.controller.functions.getAspect(idx).call()
        return aspect


