from typing import List
from unittest.mock import Mock
from forta_agent import create_transaction_event
from forta_agent.transaction_event import TransactionEvent

from agent import AAVE_V3_ADDRESS, PROTOCOL, FLASH_LOAN_TOPIC, handle_transaction

mock_tx_event: TransactionEvent = create_transaction_event(
    {"transaction": {"hash": "0x123"}, "addresses": {"0x142": True}}
)
mock_tx_event.filter_log = Mock()


class TestFlashLoanDetector:
    def test_returns_empty_findings_if_no_aave_contract(self):
        findings: List[TransactionEvent] = handle_transaction(mock_tx_event)
        assert len(findings) == 0

    def test_returns_empty_if_no_flash_loan_events(self):
        mock_tx_event.addresses = {AAVE_V3_ADDRESS: True}
        findings: List[TransactionEvent] = handle_transaction(mock_tx_event)
        assert len(findings) == 0 

    def test_returns_finding_in_a_flash_loan(self):
        mock_tx_event.addresses = {AAVE_V3_ADDRESS: True, PROTOCOL: True}
        mock_tx_event.logs = [
            {"topics": [FLASH_LOAN_TOPIC], "address": AAVE_V3_ADDRESS}
        ]
        findings: List[TransactionEvent] = handle_transaction(mock_tx_event)
        assert len(findings) == 1
