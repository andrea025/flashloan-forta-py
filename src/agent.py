# This is a bot that will trigger an alert when a flashloan happens with Tether (USDT) on Ethereum Mainnet
from typing import List
from forta_agent import transaction_event, FindingSeverity, Finding, FindingType

AAVE_V3_ADDRESS: str = "0x87870bca3f3fd6335c3f4ce8392d69350b4fa4e2"
FLASH_LOAN_TOPIC: str = "0xefefaba5e921573100900a3ad9cf29f222d995fb3b6045797eaea7521bd8d6f0"

PROTOCOL = "0xdac17f958d2ee523a2206206994597c13d831ec7" # USDT address
INTERESTING_PROTOCOLS: List[str] = [PROTOCOL]
HIGH_GAS_THRESHOLD: int = 7000000
BALANCE_DIFF_THRESHOLD: int = 200_000_000_000_000_000_000  # 200 ETH

def handle_transaction(transaction_event: transaction_event.TransactionEvent) -> List[transaction_event.TransactionEvent]:
    """
    Takes transaction event and returns a list of findings that have a flash load in it.
    """
    findings: List[transaction_event.TransactionEvent] = []

    addresses_lowered = [key.lower() for key in transaction_event.addresses.keys()]

    if AAVE_V3_ADDRESS not in addresses_lowered:
        return findings

    flash_loan_events = []

    for log in transaction_event.logs:
        for topic in log["topics"]:
            if topic.lower() == FLASH_LOAN_TOPIC:
                flash_loan_events.append(log)
                
    if len(flash_loan_events) == 0:
        return findings

    for address in INTERESTING_PROTOCOLS:
        if address in addresses_lowered:
            findings.append(
                Finding(
                    {
                        "name": "Potential flash loan on our contract",
                        "description": f"Flash Loan detected in one of the interesting protocols on hash: {transaction_event.hash}",
                        "alert_id": "FORTA-5",
                        "protocol": "aave",
                        "type": FindingType.Suspicious,
                        "severity": FindingSeverity.Low,
                        "metadata": {
                            "protocolAddress": transaction_event.addresses,
                        },
                    }
                )
            )
    
    return findings
