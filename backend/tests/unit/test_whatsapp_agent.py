"""
Unit tests for WhatsApp Agent

Tests the WhatsApp agent's core functionality including:
- Phone number validation
- Message sending logic
- Error handling
- Human behavior integration
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime

# Import the actual phone validation function
import sys
sys.path.insert(0, '/Users/admin/Desktop/Разработки/KUX/backend/src')
from agents.whatsapp_agent import validate_phone_number


class TestPhoneNumberValidation:
    """Test suite for phone number validation."""

    @pytest.mark.unit
    def test_valid_international_format(self):
        """Test valid international phone numbers."""
        valid_numbers = [
            "+66812345678",      # Thailand
            "+1234567890",       # 11 digits with +
            "+447911123456",     # UK
            "+819012345678",     # Japan
            "+12025551234",      # US
        ]

        for number in valid_numbers:
            assert validate_phone_number(number) is True, f"Expected {number} to be valid"

    @pytest.mark.unit
    def test_valid_format_with_spaces(self):
        """Test phone numbers with spaces are accepted."""
        valid_numbers = [
            "+66 81 234 5678",
            "+1 555 123 4567",
            "+44 20 1234 5678",
        ]

        for number in valid_numbers:
            assert validate_phone_number(number) is True, f"Expected {number} to be valid"

    @pytest.mark.unit
    def test_valid_format_with_dashes(self):
        """Test phone numbers with dashes are accepted."""
        valid_numbers = [
            "+66-81-234-5678",
            "+1-555-123-4567",
            "+44-20-1234-5678",
        ]

        for number in valid_numbers:
            assert validate_phone_number(number) is True, f"Expected {number} to be valid"

    @pytest.mark.unit
    def test_valid_format_with_parentheses(self):
        """Test phone numbers with parentheses are accepted."""
        valid_numbers = [
            "+1 (555) 123-4567",
            "+44 (20) 1234 5678",
        ]

        for number in valid_numbers:
            assert validate_phone_number(number) is True, f"Expected {number} to be valid"

    @pytest.mark.unit
    def test_valid_without_plus_prefix(self):
        """Test that numbers without + are accepted (will be added by system)."""
        # Note: The function accepts numbers without +, as they might be formatted elsewhere
        valid_numbers = [
            "66812345678",
            "1234567890",
        ]

        for number in valid_numbers:
            assert validate_phone_number(number) is True, f"Expected {number} to be valid"

    @pytest.mark.unit
    def test_invalid_too_short(self):
        """Test that phone numbers that are too short are rejected."""
        invalid_numbers = [
            "+123",         # Only 3 digits
            "+12345",       # Only 5 digits
            "+123456",      # Only 6 digits (minimum is 7)
        ]

        for number in invalid_numbers:
            assert validate_phone_number(number) is False, f"Expected {number} to be invalid (too short)"

    @pytest.mark.unit
    def test_invalid_too_long(self):
        """Test that phone numbers that are too long are rejected."""
        invalid_numbers = [
            "+1234567890123456",  # 16 digits (maximum is 15)
            "+12345678901234567", # 17 digits
        ]

        for number in invalid_numbers:
            assert validate_phone_number(number) is False, f"Expected {number} to be invalid (too long)"

    @pytest.mark.unit
    def test_invalid_contains_letters(self):
        """Test that phone numbers with letters are rejected."""
        invalid_numbers = [
            "+66abc123456",
            "+1-555-CALL-NOW",
            "+44-LONDON-123",
        ]

        for number in invalid_numbers:
            assert validate_phone_number(number) is False, f"Expected {number} to be invalid (contains letters)"

    @pytest.mark.unit
    def test_invalid_contains_special_chars(self):
        """Test that phone numbers with invalid special characters are rejected."""
        invalid_numbers = [
            "+66#81#234#5678",
            "+1*555*123*4567",
            "+44@20@1234@5678",
        ]

        for number in invalid_numbers:
            assert validate_phone_number(number) is False, f"Expected {number} to be invalid (special chars)"

    @pytest.mark.unit
    def test_invalid_empty_string(self):
        """Test that empty string is rejected."""
        assert validate_phone_number("") is False

    @pytest.mark.unit
    def test_invalid_only_plus(self):
        """Test that only + is rejected."""
        assert validate_phone_number("+") is False

    @pytest.mark.unit
    def test_boundary_minimum_length(self):
        """Test boundary case: exactly 7 digits (minimum valid length)."""
        assert validate_phone_number("+1234567") is True

    @pytest.mark.unit
    def test_boundary_maximum_length(self):
        """Test boundary case: exactly 15 digits (maximum valid length)."""
        assert validate_phone_number("+123456789012345") is True


class TestWhatsAppAgentInit:
    """Test suite for WhatsApp Agent initialization."""

    @pytest.mark.unit
    def test_agent_initialization_success(self, mock_adb_handler, mock_llm_client):
        """Test that WhatsApp agent initializes correctly with valid dependencies."""
        # This test would require importing WhatsAppAgent
        # Skipped for now as it requires more complex setup
        pytest.skip("WhatsApp Agent full initialization test - implement after E2E testing")


class TestWhatsAppMessageSending:
    """Test suite for WhatsApp message sending logic."""

    @pytest.mark.unit
    async def test_send_message_validates_phone_number(self):
        """Test that send_message validates phone number before processing."""
        # This would test the full send_message flow
        pytest.skip("Full send_message test - implement after E2E testing")

    @pytest.mark.unit
    async def test_send_message_uses_human_behavior(self):
        """Test that send_message integrates human behavior layer."""
        pytest.skip("Human behavior integration test - implement after E2E testing")


# ==================== Integration Test Placeholders ====================

class TestWhatsAppAgentIntegration:
    """Integration tests for WhatsApp Agent with real components."""

    @pytest.mark.integration
    @pytest.mark.adb
    async def test_send_message_with_real_adb(self):
        """Test message sending with real ADB connection (requires device)."""
        pytest.skip("Real ADB test - requires physical device setup")

    @pytest.mark.integration
    @pytest.mark.llm
    async def test_send_message_with_real_llm(self):
        """Test message sending with real Puter.js LLM API."""
        pytest.skip("Real LLM test - requires API key configuration")


# ==================== Run Tests ====================

if __name__ == "__main__":
    # Run this test file only
    pytest.main([__file__, "-v", "--tb=short"])
